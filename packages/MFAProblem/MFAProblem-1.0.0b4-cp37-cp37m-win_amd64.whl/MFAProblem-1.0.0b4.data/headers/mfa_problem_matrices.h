#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <Eigen/SparseCore>
#include <vector>

#ifdef _WIN32
#define export_dll __declspec (dllexport)
#else
#define export_dll
#endif

using namespace Eigen;
using namespace std;
using arr_int = pybind11::array_t<int, pybind11::array::c_style | pybind11::array::forcecast>;
using arr_float = pybind11::array_t<float, pybind11::array::c_style | pybind11::array::forcecast>;

namespace MFAProblemMatrices {
	export_dll  arr_float ineq_red_old(
		arr_float intervals, 
		arr_float li_pybind, 
		arr_float ui_pybind,
		arr_int ai_vars_free, 
		arr_float ai_coefs_free, 
		arr_float ai_signs_free, 
		arr_int var_occ_Ai
	);

	export_dll vector<pair<vector<size_t>, vector<size_t>>> get_free_variables_groups(
		SparseMatrix<float, RowMajor> M
	);

	export_dll MatrixXf ineq_red(
		MatrixXf intervals,
		SparseMatrix<float, RowMajor> M,
		SparseVector<float>& li,
		SparseVector<float>& ui
	);

	export_dll SparseMatrix<double, RowMajor> to_reduced_row_echelon_form(
		SparseMatrix<double, RowMajor>& M
	);

	export_dll tuple<vector<ssize_t>, vector<ssize_t>> extract_determinable_variables(
		SparseMatrix<float, RowMajor> M, float tol, bool
	);

	export_dll tuple<vector<vector<size_t>>, vector<vector<float>>, vector<vector<short>>, map<size_t, map<size_t, size_t>>>
		define_constraints_properties(
			SparseMatrix<float, RowMajor> M
		);
}

/* --------------------------------------------------
This part is mandatory. "mfa_problem_matrices" corresponds to
the name you will use in your python file. m.def
creates the python function with the name in the
string. You can check here the basic use:
https://pybind11.readthedocs.io/en/stable/basics.html
----------------------------------------------------- */
PYBIND11_MODULE(mfa_problem_matrices, m) {
	//Eigen::initParallel();
	m.def("get_free_variables_groups", &MFAProblemMatrices::get_free_variables_groups);
	m.def("ineq_red_old", &MFAProblemMatrices::ineq_red_old);
	m.def("ineq_red", &MFAProblemMatrices::ineq_red);
	m.def("to_reduced_row_echelon_form", &MFAProblemMatrices::to_reduced_row_echelon_form);
	m.def("extract_determinable_variables", &MFAProblemMatrices::extract_determinable_variables);
	m.def("define_constraints_properties", &MFAProblemMatrices::define_constraints_properties);
}