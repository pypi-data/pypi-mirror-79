#include <Python.h>


PyObject* test(PyObject* self, PyObject* args) {
	return Py_BuildValue("");
}

static PyMethodDef {{ module_name }}_methods[] = {
	{"test",test,METH_VARARGS,"test function"},
	{NULL, NULL, 0, NULL}
};

PyMODINIT_FUNC init{{ module_name }}() {
	return Py_InitModule("{{ module_name }}", {{ module_name }}_methods);
}