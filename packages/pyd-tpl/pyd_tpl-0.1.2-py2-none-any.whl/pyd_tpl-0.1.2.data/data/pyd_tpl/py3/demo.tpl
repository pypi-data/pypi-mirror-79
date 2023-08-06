#include <Python.h>


PyObject* test(PyObject* self, PyObject* args) {
	return Py_BuildValue("");
}

static PyMethodDef {{ module_name }}ModuleMethods[] = {
	{"test",test,METH_VARARGS,"test function"},
	{NULL, NULL, 0, NULL}
};

static PyModuleDef {{ module_name }}Module = {
	PyModuleDef_HEAD_INIT,
	"{{ module_name }}",
	"{{ module_name }} Module",
	0,
	{{ module_name }}ModuleMethods
};

PyMODINIT_FUNC PyInit_{{ module_name }}() {
	return PyModule_Create(&{{ module_name }}Module);
}