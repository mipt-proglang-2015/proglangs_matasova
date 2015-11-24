#include <iostream>
#include <vector>

extern "C" {
#include <Python.h>
}

typedef std::vector<double>  row_t;
typedef std::vector<row_t>   matrix_t;

static matrix_t pyobject_to_cxx(PyObject * py_matrix)
{
	matrix_t result;
	result.resize(PyObject_Length(py_matrix));
	for (size_t i=0; i<result.size(); ++i) {
		PyObject * py_row = PyList_GetItem(py_matrix, i);
		row_t & row = result[i];
		row.resize(PyObject_Length(py_row));
		for (size_t j=0; j<row.size(); ++j) {
			PyObject * py_elem = PyList_GetItem(py_row, j);
			const double elem = PyFloat_AsDouble(py_elem);
			row[j] = elem;
		}
	}
	return result;
}

static PyObject * cxx_to_pyobject(matrix_t &matrix)
{
	PyObject * result = PyList_New(matrix.size());
	for (size_t i=0; i<matrix.size(); ++i) {
		const row_t & row = matrix[i];
		PyObject * py_row = PyList_New(row.size());
		PyList_SetItem(result, i, py_row);
		for (size_t j=0; j<row.size(); ++j) {
			const double elem = row[j];
			PyObject * py_elem = PyFloat_FromDouble(elem);
			PyList_SetItem(py_row, j, py_elem);
		}
	}
	return result;
}


static PyObject * FloydWarshellBasedAlgo(PyObject* module, PyObject* args)
{ 
	matrix_t matrix = pyobject_to_cxx(PyTuple_GetItem(args, 0));

	for (size_t k = 0; k < matrix.size(); k++) 
		for (size_t i = 0; i < matrix.size(); i++) 
			for (size_t j = 0; j < matrix.size(); j++) 
				if ( i != j && matrix[i][k]+matrix[k][j] != 0)
				{
					double r = matrix[i][k]+matrix[k][j];
					matrix[i][j] = r*matrix[i][j]/(r+matrix[i][j]);
				}

	return cxx_to_pyobject(matrix);
}

PyMODINIT_FUNC PyInit_algolib()
{
	static PyMethodDef ModuleMethods[] = {
		{ "FloydWarshellBasedAlgo", (PyCFunction)FloydWarshellBasedAlgo, METH_VARARGS, NULL },
		{ NULL }
	};
	static PyModuleDef ModuleDef = {
		PyModuleDef_HEAD_INIT,
		"algoLib",
		"algos",
		-1, ModuleMethods, 
		NULL, NULL, NULL, NULL
	};
	PyObject * module = PyModule_Create(&ModuleDef);
	return module;
}

