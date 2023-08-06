
import unittest
import sys
import os
import numpy as np
from scipy import sparse
import mfa_problem_matrices
try:
    import mfa_problem.mfa_problem_check_io as mfa_problem_check_io
except ImportError:
    sys.path.append(os.getcwd())
    from mfa_problem import mfa_problem_check_io as mfa_problem_check_io


class MFAProblemsCheckConstraintsTests(unittest.TestCase):
    def test_check_constraint_simple(self):
        index2name = [
            {'t': 's', 'o': 'S1', 'd': 'P1', 'p': 'P1', 's': 'S1'},
            {'t': 'u', 'o': 'P1', 'd': 'S2', 'p': 'P1', 's': 'S2'}
        ]
        ter_vectors = [
            [10, 10],  # data
            [2, 2],    # sigma
            [0, 0],    # LB
            [50, 50]   # UB
        ]
        solved_vector = np.array([10, 10])
        AConstraint = [[1, -1, 0, 0]]
        AConstraint = sparse.csc_matrix(AConstraint, dtype=float)
        Ai_vars, Ai_coefs, Ai_signs, vars_occ_Ai = mfa_problem_matrices.define_constraints_properties(
            AConstraint.tocsc()[:, :22].tocsr()
        )
        vars_type = np.array(['redundant', 'redundant'])
        downscale = False
        constraints_types_cum_idx = [0, 1, 1, 1, 1]
        bound_issues, contraints_issues = mfa_problem_check_io.check_constraints(
            index2name,
            solved_vector,
            ter_vectors,
            AConstraint,
            Ai_vars,
            Ai_signs,
            downscale,
            vars_type,
            constraints_types_cum_idx
        )
        self.assertEqual(len(bound_issues), 0)
        self.assertEqual(len(contraints_issues), 0)
        solved_vector = np.array([10, 11])
        bound_issues, contraints_issues = mfa_problem_check_io.check_constraints(
            index2name,
            solved_vector,
            ter_vectors,
            AConstraint,
            Ai_vars,
            Ai_signs,
            downscale,
            vars_type,
            constraints_types_cum_idx
        )
        self.assertEqual(len(contraints_issues), 1)
        self.assertEqual(
            contraints_issues.to_string(index=False),
            ' constraint  value  contraint_value       type\n' +
            '        0.0   -1.0              0.0  below min'
        )
        AConstraint = sparse.csc_matrix([[1, -1, -10, -2]], dtype=float)
        bound_issues, contraints_issues = mfa_problem_check_io.check_constraints(
            index2name,
            solved_vector,
            ter_vectors,
            AConstraint,
            Ai_vars,
            Ai_signs,
            downscale,
            vars_type,
            constraints_types_cum_idx
        )
        self.assertEqual(len(contraints_issues), 1)
        self.assertEqual(
            contraints_issues.to_string(index=False),
            ' constraint  value  contraint_value       type\n' +
            '        0.0   -1.0              2.0  above max'
        )

    def test_check_constraint(self):
        index2name = [
            {'t': 's', 'o': 'S1', 'd': 'P1', 'p': 'P1', 's': 'S1'},
            {'t': 's', 'o': 'S2', 'd': 'P2', 'p': 'P2', 's': 'S2'},
            {'t': 's', 'o': 'International', 'd': 'P2', 'p': 'P2', 's': 'International'},
            {'t': 's', 'o': 'S3', 'd': 'P3', 'p': 'P3', 's': 'S3'},
            {'t': 's', 'o': 'International', 'd': 'P3', 'p': 'P3', 's': 'International'},
            {'t': 's', 'o': 'S4', 'd': 'P4', 'p': 'P4', 's': 'S4'},
            {'t': 's', 'o': 'S5', 'd': 'P4', 'p': 'P4', 's': 'S5'},
            {'t': 's', 'o': 'International', 'd': 'P4', 'p': 'P4', 's': 'International'},
            {'t': 's', 'o': 'S5', 'd': 'P5', 'p': 'P5', 's': 'S5'},
            {'t': 's', 'o': 'International', 'd': 'P5', 'p': 'P5', 's': 'International'},
            {'t': 'u', 'o': 'P1', 'd': 'S2', 'p': 'P1', 's': 'S2'},
            {'t': 'u', 'o': 'P1', 'd': 'S3', 'p': 'P1', 's': 'S3'},
            {'t': 'u', 'o': 'P2', 'd': 'S3', 'p': 'P2', 's': 'S3'},
            {'t': 'u', 'o': 'P2', 'd': 'S4', 'p': 'P2', 's': 'S4'},
            {'t': 'u', 'o': 'P2', 'd': 'International', 'p': 'P2', 's': 'International'},
            {'t': 'u', 'o': 'P3', 'd': 'S4', 'p': 'P3', 's': 'S4'},
            {'t': 'u', 'o': 'P3', 'd': 'S5', 'p': 'P3', 's': 'S5'},
            {'t': 'u', 'o': 'P3', 'd': 'International', 'p': 'P3', 's': 'International'},
            {'t': 'u', 'o': 'P4', 'd': 'S6', 'p': 'P4', 's': 'S6'},
            {'t': 'u', 'o': 'P4', 'd': 'International', 'p': 'P4', 's': 'International'},
            {'t': 'u', 'o': 'P5', 'd': 'S6', 'p': 'P5', 's': 'S6'},
            {'t': 'u', 'o': 'P5', 'd': 'International', 'p': 'P5', 's': 'International'}
        ]
        ter_vectors = [
            [100, 1, 20, 70, 5, 6.5, 10, 5, 10, 5, 1, 1, 1, 1, 5, 1, 1, 10, 80, 10, 20, 15],
            [50e-01, 0, 1, 1.75e+00, 2.5e-01, 3.25e+00, 50e-01, 2.5e-01, 50e-01,
             2.5e-01, 0, 0, 0, 0, 2.5e-01, 0, 0, 50e-01,
             20e+00, 50e-01, 50e-01, 7.5e-01],
            [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
            [50e+08, 50e+08, 50e+08, 50e+08, 50e+08, 50e+08, 50e+08, 50e+08, 50e+08,
             50e+08, 50e+08, 50e+08, 50e+08, 50e+08, 50e+08, 50e+08, 50e+08, 50e+08,
             50e+08, 50e+08, 50e+08, 50e+08]
            ]
        solved_vector = np.array([
            31.702586206896548,
            31.702586206896548,
            66.70258620689656,
            3.297413793103461,
            39.41810344827583,
            34.967672413793125,
            27.640086206896555,
            98.40517241379311,
            16.810344827586206,
            70.00000000000001,
            4.202586206896552,
            74.38577586206895,
            11.443965517241384,
            4.924568965517242,
            16.19612068965517,
            7.300646551724137,
            5.797413793103447,
            11.594827586206895,
            80.60344827586206,
            10.150862068965514,
            15.39870689655172,
            8.098060344827589
        ])

        Arref = [
            # 0  1  2   3  4  5  6  7  8   9  10 11  12 13 14  15  16  17  18  19  20  21 22 23
            [1, 0, 0, -1, 0, 0, 0, 0, 1,  1,  1, 0,  0, 1, 0,  1, -1, -1, -1, -1, -1, -1, 0, 0],
            [0, 1, 0, -1, 0, 0, 0, 0, 1,  1,  1, 0,  0, 1, 0,  1, -1, -1, -1, -1, -1, -1, 0, 0],
            [0, 0, 1,  1, 0, 0, 0, 0, 0, -1,  0, 0,  0, 0, 0,  0,  0,  0,  0,  0,  0,  0, 0, 0],
            [0, 0, 0,  0, 1, 0, 0, 0, 0,  1,  1, 0,  0, 1, 0,  1,  0, -1, -1, -1, -1, -1, 0, 0],
            [0, 0, 0,  0, 0, 1, 0, 0, 0, -1, -1, 0,  1, 0, 0, -1,  0,  1,  0,  0,  1,  1, 0, 0],
            [0, 0, 0,  0, 0, 0, 1, 0, 0,  0,  0, 0, -1, 0, 0,  1,  0,  0,  0,  0, -1, -1, 0, 0],
            [0, 0, 0,  0, 0, 0, 0, 1, 1,  0,  1, 0,  0, 1, 0,  1, -1, -1, -1, -1, -1, -1, 0, 0],
            [0, 0, 0,  0, 0, 0, 0, 0, 0,  0,  0, 1,  1, 1, 0,  0,  0,  0, -1, -1,  0,  0, 0, 0],
            [0, 0, 0,  0, 0, 0, 0, 0, 0,  0,  0, 0,  0, 0, 1,  1,  0,  0,  0,  0, -1, -1, 0, 0]
        ]
        # the free matrix is
        # 1, 0, 0, -1
        # 0, 1, 0, -1
        # 0, 0, 1,  1

        Arref = sparse.csc_matrix(Arref, dtype=float)
        Ai_vars, Ai_coefs, Ai_signs, vars_occ_Ai = mfa_problem_matrices.define_constraints_properties(
            Arref.tocsc()[:, :22].tocsr()
        )

        vars_type = np.array([
            'redondant',
            'libre',
            'redondant',
            'mesuré',
            'redondant',
            'redondant',
            'redondant',
            'redondant',
            'redondant',
            'redondant',
            'libre',
            'libre',
            'libre',
            'déterminé',
            'redondant',
            'déterminé',
            'déterminé',
            'redondant',
            'redondant',
            'redondant',
            'redondant',
            'redondant'
        ])

        downscale = False
        constraints_types_cum_idx = [0, 5, 9, 9, 9]

        bound_issues, contraints_issues = mfa_problem_check_io.check_constraints(
            index2name,
            solved_vector,
            ter_vectors,
            Arref,
            Ai_vars,
            Ai_signs,
            downscale,
            vars_type,
            constraints_types_cum_idx
        )
        self.assertEqual(len(bound_issues), 0)
        self.assertEqual(len(contraints_issues), 0)
        solved_vector[0] = -10
        bound_issues, contraints_issues = mfa_problem_check_io.check_constraints(
            index2name,
            solved_vector,
            ter_vectors,
            Arref,
            Ai_vars,
            Ai_signs,
            downscale,
            vars_type,
            constraints_types_cum_idx
        )
        bound_issue_str = \
            ' var index  var name  output value       type  Bound   var type\n' + \
            '       0.0  S1 -> P1         -10.0  below min    0.0  redondant'
        self.assertEqual(bound_issues.to_string(index=False), bound_issue_str)
        solved_vector[0] = 31.702586206896548
        ter_vectors[3][0] = 10
        bound_issues, contraints_issues = mfa_problem_check_io.check_constraints(
            index2name,
            solved_vector,
            ter_vectors,
            Arref,
            Ai_vars,
            Ai_signs,
            downscale,
            vars_type,
            constraints_types_cum_idx
        )
        bound_issue_str = \
            ' var index  var name  output value       type  Bound   var type\n' + \
            '       0.0  S1 -> P1     31.702586  above max   10.0  redondant'
        self.assertEqual(bound_issues.to_string(index=False), bound_issue_str)


if __name__ == '__main__':
    unittest.main()
