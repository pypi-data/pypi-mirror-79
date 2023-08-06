import time
import numpy as np
import scipy

try:
    from . import mfa_problem_solver
except Exception:
    import mfa_problem_solver
try:
    from . import mfa_problem_format_io
except Exception:
    import mfa_problem_format_io
try:
    from . import mfa_problem_check_io
except Exception:
    import mfa_problem_check_io
try:
    from . import su_trace
except Exception:
    import su_trace

import mfa_problem_matrices

le_max = 5e8  # some maïs data are as high as 15 000 000
sigmas_floor = 1
regions_key = None
DATA, SIGMA, LB, UB = 0, 1, 2, 3


def optimisation(
    model_name: str,
    js_dict: dict,
    uncertainty_analysis: bool,
    nb_realisations: int,
    downscale: bool,
    upper_level_index2name: dict,
    upper_level_solved_vector: list,
    upper_level_classification: list,
    montecarlo_upper_level: dict,
    main_problem: bool = True,
    record_simulations: bool = False,
    performance: bool = False
):
    global le_max, sigmas_floor, regions_key

    t0 = time.time()

    # Extracts parameter values from entry 'param'
    if 'param' in js_dict:
        if 'le_max' in js_dict['param']:
            le_max = js_dict['param']['le_max']
        if 'sigmas_floor' in js_dict['param']:
            sigmas_floor = js_dict['param']['sigmas_floor']
        if downscale:
            regions_key = 'Autres régions françaises'
            if 'reg' in js_dict['param']:
                regions_key = js_dict['param']['reg']

    if main_problem:
        tk0 = time.time()
        su_trace.logger.info('---- Main Problem : ' + model_name + ' ----')

        # 1 Creation of MFA extended matrice
        res = mfa_problem_format_io.extract_intermediary_structures(js_dict, downscale, regions_key)
        if res is None:
            return None
        [
            dim_p, dim_s, products_desc, sectors_desc, regions_names, non_positive_sectors,
            index2name, name2index, post_process
        ] = res

        _, idx = np.unique(products_desc[:, 1], return_index=True)
        products_names = products_desc[:, 1][np.sort(idx)]
        _, idx = np.unique(sectors_desc[:, 1], return_index=True)
        sectors_names = sectors_desc[:, 1][np.sort(idx)]
        full_ter_vectors, AConstraintEq, AConstraintIneq, constraints_types_cum_idx = \
            mfa_problem_format_io.creates_mfa_system(
                js_dict,
                products_names,
                sectors_names,
                regions_names,
                dim_p,
                dim_s,
                non_positive_sectors,
                index2name, name2index, post_process,
                downscale,
                upper_level_index2name,
                upper_level_solved_vector,
                upper_level_classification,
                regions_key,
                le_max,
                sigmas_floor
            )
        if AConstraintEq is None:
            return None
        mask_is_measured = np.where(
            full_ter_vectors[mfa_problem_format_io.DATA] != mfa_problem_format_io.default_initial_value,
            True,
            False
        )
        mask_is_not_measured = np.invert(mask_is_measured).nonzero()[0]
        post_process = np.array(post_process)

        full_ter_size = len(index2name)
        nb_measured = sum(mask_is_measured)
        nb_unmeasured = full_ter_size-nb_measured

        mask_is_not_measured_non_pp = np.setdiff1d(
            mask_is_not_measured,
            post_process.nonzero()[0]
        )

        AConstraintEq = AConstraintEq.tocsc()
        B = AConstraintEq[:, mask_is_not_measured_non_pp]
        rows_non_pp = (AConstraintEq[:, post_process].getnnz(1) == 0).nonzero()[0]
        B = B[rows_non_pp, :]

        A = AConstraintEq[:, mask_is_measured]
        A = A[rows_non_pp, :]
        li = AConstraintEq[rows_non_pp, full_ter_size]
        ui = AConstraintEq[rows_non_pp, full_ter_size+1]
        AConstraintEqReorderedReduced = scipy.sparse.hstack((B, A, li, ui), format='csr')

        AConstraintEqReordered = scipy.sparse.hstack(
            (AConstraintEq[:, mask_is_not_measured],
             AConstraintEq[:, mask_is_measured],
             AConstraintEq[:, full_ter_size],
             AConstraintEq[:, full_ter_size+1]),
            format='csr'
        )
        AIneqReordered = scipy.sparse.hstack(
            (AConstraintIneq[:, mask_is_not_measured],
             AConstraintIneq[:, mask_is_measured],
             AConstraintIneq[:, full_ter_size],
             AConstraintIneq[:, full_ter_size+1]),
            format='csr'
        )
        AIneqReorderedReduced = scipy.sparse.hstack(
            (AConstraintIneq[:, mask_is_not_measured_non_pp],
             AConstraintIneq[:, mask_is_measured],
             AConstraintIneq[:, full_ter_size],
             AConstraintIneq[:, full_ter_size+1]),
            format='csr'
        )

        ter_vectors_reordered = np.hstack((
            full_ter_vectors[:, mask_is_not_measured],
            full_ter_vectors[:, mask_is_measured]
        ))
        post_process_reordered = np.hstack((
            post_process[mask_is_not_measured],
            post_process[mask_is_measured]
        ))

        su_trace.logger.info('MFA model created, size ' + str(len(index2name)))

        tk1 = time.time()
        su_trace.logger.info('------ MFA created, took ' + str(round((tk1-tk0), 2)) + ' s ------')

        # 2 Puts MFA extended matrice in canonical form
        su_trace.logger.info('Entering variables classification at ' +
                             str(time.strftime("%T", time.localtime(tk1))))
        AEqReorderedRef, determinable_col2row, _, reordered_vars_type, _ = \
            mfa_problem_solver.classify_with_matrix_reduction(
                AConstraintEqReordered, nb_measured
            )
        if AEqReorderedRef is None:
            su_trace.logger.critical('Creation of MFA extended matrice in canonical form failed')
            return None
        # reduced_mfa_indices = np.logical_not(post_process_reordered)
        # reduced_mfa_indices_ext = np.append(reduced_mfa_indices, [True, True])  # li ui
        # rows_non_pp = (AEqReorderedRef[:, post_process_reordered].getnnz(1) == 0).nonzero()[0]
        # AEqReorderedRefReduced = AEqReorderedRef[:, reduced_mfa_indices_ext][rows_non_pp, :]
        AEqReorderedRefReduced, reduced_determinable_col2row, _, _, rank_unmeasured_reduced = \
            mfa_problem_solver.classify_with_matrix_reduction(
                AConstraintEqReorderedReduced, nb_measured
            )

        su_trace.logger.info('Took ' + str(round(time.time()-t0, 2)) + ' sec to classify variables')

        tk3 = time.time()
        su_trace.logger.info('------ Creation of MFA extended matrice, took ' +
                             str(round((tk3-tk1), 2)) + ' / ' + str(round((tk3-tk0), 2)) + ' s ------')

        solved_vector_reordered, intervals_reordered = mfa_problem_solver.resolve_mfa_problem(
            rank_unmeasured_reduced,
            AEqReorderedRef,
            AEqReorderedRefReduced,
            AIneqReordered,
            AIneqReorderedReduced,
            nb_measured,
            ter_vectors_reordered,
            determinable_col2row,
            reduced_determinable_col2row,
            reordered_vars_type,
            post_process_reordered
        )
        solved_vector = np.empty(full_ter_size)
        solved_vector[mask_is_not_measured] = solved_vector_reordered[0:nb_unmeasured]
        solved_vector[mask_is_measured] = solved_vector_reordered[nb_unmeasured:]
        intervals = np.empty((full_ter_size, 2))
        intervals[mask_is_not_measured, :] = intervals_reordered[0:nb_unmeasured, :]
        intervals[mask_is_measured, :] = intervals_reordered[nb_unmeasured:, :]
        vars_type = np.empty(full_ter_size, dtype=object)
        vars_type[mask_is_not_measured] = reordered_vars_type[0:nb_unmeasured]
        vars_type[mask_is_measured] = reordered_vars_type[nb_unmeasured:]
        vars_type[post_process] = vars_type[post_process] + ' pp'
        t1 = time.time()
        su_trace.logger.info('---- Main Problem Completed, took ' + str(round((t1-t0), 2)) + ' s ----')

    montecarlo_results = None
    if uncertainty_analysis:
        su_trace.logger.info('---- Uncertainty Analysis {} Starts ----'.format('model_name'))
        np.random.seed(101)
        montecarlo_results = mfa_problem_solver.montecarlo(
            rank_unmeasured_reduced,
            AEqReorderedRef,
            AEqReorderedRefReduced,
            AIneqReordered,
            AIneqReorderedReduced,
            nb_measured,
            ter_vectors_reordered,
            determinable_col2row,
            reduced_determinable_col2row,
            reordered_vars_type,
            post_process_reordered,
            mask_is_measured,
            nb_realisations,
            sigmas_floor,
            downscale,  # parameters
            None
        )

        if montecarlo_results is None:
            su_trace.logger.critical('Uncertainty Analysis failed')
            return None
        t2 = time.time()
        su_trace.logger.info('---- Uncertainty Analysis Completed, Took ' +
                             str(round(t2-t1, 2)) + '/' + str(round(t2-t0, 2)) + ' s ----')

    AAllConstraints = scipy.sparse.vstack((AConstraintEq, AConstraintIneq)).tocsc()

    Ai_vars, _, Ai_signs, vars_occ_Ai = \
        mfa_problem_matrices.define_constraints_properties(AAllConstraints[:, :full_ter_size].tocsr())
    # write ter in json format
    mfa_problem_output = mfa_problem_format_io.mfa_problem_output(
        index2name, name2index,  # ter
        products_desc, sectors_desc, regions_names,  # desc
        full_ter_vectors,  # input
        AAllConstraints, constraints_types_cum_idx, vars_occ_Ai,
        vars_type,  # intermediate
        solved_vector, intervals, montecarlo_results,  # solved
        downscale, uncertainty_analysis, record_simulations=record_simulations  # parameters
    )
    mfa_problem_check_io.check_constraints(
        index2name,
        solved_vector,
        full_ter_vectors, AAllConstraints,
        Ai_vars,
        Ai_signs,
        downscale,
        vars_type,
        constraints_types_cum_idx
    )
    t2 = time.time()
    su_trace.logger.info(
        '---- Constraints Checked, Took ' +
        str(round((t2-t1), 2)) + ' / ' + str(round((t2-t0), 2)) + ' s ----'
    )
    return mfa_problem_output
