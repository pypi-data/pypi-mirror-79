# -*- coding: utf-8 -*-
"""This module is used to check if an excel input file has no inconsistancy in
its supply/use tables.

The module uses 2 or 3 arguments :
    - "--input_file" : specifies the name of the (excel) input file to check
      (usualy data/tuto_fr.xlsx).
    - "--tab_list" : specifies the list of sheets for products, sectors and
      existing fluxes (typically ['Dim products', 'Dim sectors', 'Existing
      fluxes'])
    - "--merge_with" : second excel input file, the two ter1 will be merged
      into a new one. It is assumed that tab names are the same as the first
      file."
"""

import io

import pandas as pd
import numpy as np
from numpy import ndarray
from scipy.sparse import csc_matrix

from contextlib import redirect_stdout

try:
    from . import su_trace
except Exception:
    import su_trace
try:
    from . import mfa_problem_format_io
except Exception:
    import mfa_problem_format_io


def table(table_id: str):
    if table_id in ['s', 'S', 'r', 'R']:  # supply, ressources
        return 's'
    elif table_id in ['u', 'U', 'e', 'E']:  # use, emplois
        return 'u'
    else:
        raise ValueError('Error : wrong table name', table_id)


def check_if_flows_exist(
    tod,  # np.array
    ter1: list,
    tab: str,
    unknown_flows: list
):
    for i, r in enumerate(tod):
        t = table(r[0])
        o = r[1]
        d = r[2]
        if t == 's':
            p = d
            s = o
        elif t == 'u':
            p = o
            s = d
        try:
            if ter1[t][p][s] != 1:
                unknown_flows.append([tab, i, t, o, d])
        except KeyError as err:
            su_trace.logger.error(
                'Origine or Destination not found in list of products or sectors. ' +
                'Check spelling of ' + str(err)
            )
            unknown_flows.append([tab, i, t, o, d])
            return unknown_flows

    return unknown_flows


def check_input_file(
    mfa_problem_input: dict,
):
    dimp = mfa_problem_format_io.extract_dimension('dim_products', mfa_problem_input)
    dims = mfa_problem_format_io.extract_dimension('dim_sectors', mfa_problem_input)

    products_desc = mfa_problem_format_io.extract_columns(
        mfa_problem_input, 'dim_products', [0,1],[int,str])
    sectors_desc = mfa_problem_format_io.extract_columns(
        mfa_problem_input, 'dim_sectors', [0,1],[int,str])

    _,idx = np.unique(products_desc[:,1], return_index=True)
    products_names = products_desc[:,1][np.sort(idx)]
    _,idx = np.unique(sectors_desc[:,1], return_index=True)
    sectors_names = sectors_desc[:,1][np.sort(idx)] 

    non_positive_sectors = []
    for s, coefs in dims['consolidation_weight'].items():
        for e in coefs:
            if e < 0:
                non_positive_sectors.append(s)
                break

    input_ter, ter1_dict = \
        mfa_problem_format_io.load_input_ter(
            mfa_problem_input, 'ter_base', dimp, dims, non_positive_sectors,
             products_names, sectors_names,
            auto_fill_all_children=True
        )

    file_returned = input_ter is not None

    if ter1_dict is None:
        su_trace.logger.error('Need for manual ter check')
    else:
        if input_ter is None:
            su_trace.logger.info('No need to rewrite Excel sheet.')

    reg = None

    unknown_flows = []
    # 2. CHECK DATA
    tab = 'data'
    if not reg:
        # table, orig, dest, value, uncertainty
        check_if_flows_exist(
            mfa_problem_format_io.extract_columns(
                mfa_problem_input, 'data', [2, 3, 4], ['object', 'object', 'object']
            ),
            ter1_dict, tab, unknown_flows
        )
    else:
        su_trace.logger.error('Data, Case reg to be implemented')
        return [file_returned, None, None]
    # 3. CHECK min max bounds
    tab = 'min_max'
    if not reg:
        # table, orig, dest, min, Max
        check_if_flows_exist(
            mfa_problem_format_io.extract_columns(
                mfa_problem_input, 'min_max', [2, 3, 4], ['object', 'object', 'object']
            ),
            ter1_dict, tab, unknown_flows
        )
    else:
        su_trace.logger.error('Min_max, Case reg to be implemented')
        return [file_returned, None, None]
    # 4. CHECK OTHER CONSTRAINTS
    tab = 'constraints'
    check_if_flows_exist(
        mfa_problem_format_io.extract_columns(
            mfa_problem_input, 'constraints', [3, 4, 5], ['object', 'object', 'object']
        ),
        ter1_dict, tab, unknown_flows
    )

    if len(unknown_flows) > 0:
        su_trace.logger.info('The following flows were not found in ter1')
        for e in unknown_flows:
            su_trace.logger.error(
                '{}, row #{}, table {}, orig. {}, dest. {}'.format(
                    e[0], str(e[1]+2), e[2], e[3], e[4]
                )
            )
        su_trace.logger.error('Problem with file.')
        return [input_ter, None, None]
    else:
        su_trace.logger.info('No issues with input data')
        return [input_ter, ter1_dict, mfa_problem_input]


def name_of(
    index2name: list,
    id: int,
    downscale: bool
):
    if not downscale:
        return index2name[id]['o'] + ' -> ' + index2name[id]['d']
    else:
        return index2name[id]['r'] + ' - ' + index2name[id]['o'] + ' -> ' + index2name[id]['d']


def constraint_type(
    constraint_id: int,
    constraints_types_cum_idx: list
):
    types = ['aggregation', 'products', 'sectors', 'other', 'geographical']
    for i, cum_idx in enumerate(constraints_types_cum_idx):
        if constraint_id < cum_idx:
            return types[i]
    return 'ineq'


def check_constraints(
    index2name: list,
    solved_vector: ndarray,
    ter_vectors: ndarray,
    AConstraint: csc_matrix,
    Ai_vars: list,
    Ai_signs: list,
    downscale: bool,
    vars_type: ndarray,
    constraints_types_cum_idx
):
    DATA, LB, UB = 0, 2, 3

    ter_size = len(solved_vector)
    ui = AConstraint.tocsr()[:, ter_size+1].toarray()[:, 0]
    li = AConstraint[:, ter_size].toarray()[:, 0]
    tol = 0.1
    bound_issues = pd.DataFrame(
        {'var index': [], 'var name': [], 'output value': [], 'type': [], 'Bound': [], 'var type': []}, index=None
    )
    # check min/max bounds
    for idx in range(ter_size):
        # idx = col_non_zero_idx[i]
        if solved_vector[idx] > ter_vectors[UB][idx] + tol:
            bound_issues = bound_issues.append({
                'var index': idx,
                'var name': name_of(index2name, idx, downscale),
                'output value': solved_vector[idx],
                'type': 'above max',
                'Bound': ter_vectors[UB][idx],
                'var type': vars_type[idx]
            }, ignore_index=True)
        if solved_vector[idx] < ter_vectors[LB][idx] - tol:
            bound_issues = bound_issues.append({
                'var index': idx,
                'var name': name_of(index2name, idx, downscale),
                'output value': solved_vector[idx],
                'type': 'below min',
                'Bound': ter_vectors[LB][idx],
                'var type': vars_type[idx]
            }, ignore_index=True)

    y = AConstraint[:, :-2] * solved_vector
    contraints_issues = pd.DataFrame(
        {'constraint': [], 'value': [], 'contraint_value': [], 'abs_value': [], 'type': []}, index=None
    )
    for i in range(len(y)):
        if float(y[i]) > ui[i] + tol:
            contraints_issues = contraints_issues.append(
                {'constraint': i, 'value': round(y[i], 3),
                    'contraint_value': abs(round(ui[i], 3)),
                    'abs_value': abs(round(y[i]-ui[i], 3)),
                    'type': 'above max'}, ignore_index=True
            )
        if float(y[i]) < li[i] - tol:
            contraints_issues = contraints_issues.append(
                {'constraint': i, 'value': round(y[i], 3),
                    'contraint_value': abs(round(li[i], 3)),
                    'abs_value': abs(round(y[i]-li[i], 3)),
                    'type': 'below min'}, ignore_index=True
            )
    with io.StringIO() as buf, redirect_stdout(buf):
        if len(bound_issues) != 0:
            print(bound_issues.to_string(index=False))
        else:
            print('All bound constraints are honored')
        su_trace.logger.info(buf.getvalue())

    with io.StringIO() as buf, redirect_stdout(buf):
        contraints_issues.sort_values(by='abs_value', ascending=False, inplace=True)
        contraints_issues = contraints_issues[:10]
        contraints_issues = contraints_issues.drop(columns=['abs_value'])
        if len(contraints_issues) != 0:
            print(contraints_issues.to_string(index=False))
        else:
            print('All linear constraints are honored')
        for i in contraints_issues['constraint']:
            print('--- Contrainte ', int(i), ' ', constraint_type(i, constraints_types_cum_idx))
            for k, var in enumerate(Ai_vars[int(i)]):
                print(
                    Ai_signs[int(i)][k],
                    '('+name_of(index2name, var, downscale)+')',
                    round(ter_vectors[DATA][var], 1),
                    round(solved_vector[var], 1),
                    vars_type[var]
                )
        for str_info in buf.getvalue().splitlines(True):
            su_trace.logger.info(str_info)

    return bound_issues, contraints_issues
