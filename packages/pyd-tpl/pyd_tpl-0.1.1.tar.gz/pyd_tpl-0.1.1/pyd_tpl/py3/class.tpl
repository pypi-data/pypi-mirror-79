#include <Python.h>
#include <structmember.h>
#include <stdbool.h>

#if(defined _WIN32)||(defined _WIN64)
    #define ENCODING "gbk"
#else
    #define ENCODING "utf8"
#endif

typedef struct {
    PyObject_HEAD
    PyObject* name;
} {{ class_name }};

static void {{ class_name|lower }}_dealloc({{ class_name }}* self){
    Py_XDECREF(self->name);
    Py_TYPE(self)->tp_free((PyObject*)self);
}

PyObject* say(PyObject* self,PyObject* args){
    PyObject* val = Py_BuildValue("s","hello,world!");
    return val;
}

static PyObject *
{{ class_name|lower }}_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    {{ class_name }} *self;
    self = ({{ class_name }} *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->name = PyUnicode_FromString("");
        if (self->name == NULL) {
            Py_DECREF(self);
            return NULL;
        }
    }
    return (PyObject *)self;
}

static PyMemberDef {{ class_name|lower }}_members[] = {
    {"name",T_OBJECT_EX, offsetof({{ class_name }}, name), 0, ""},
    {NULL,NULL, 0, NULL, NULL}
};

PyObject* test(PyObject* self, PyObject* args) {
    return Py_BuildValue("");
}

static PyMethodDef {{ class_name|lower }}_methods[] = {
    {"say", say, METH_VARARGS, "say function"},
	{NULL, NULL, 0, NULL}
};

static int {{ class_name|lower }}_init({{ class_name }} *self, PyObject *args, PyObject *kwds)
{
    PyObject *name=NULL,*tmp;
    static char *kwlist[] = {"name", NULL};
    if (!PyArg_ParseTupleAndKeywords(args, kwds, "|O", kwlist, &name))
        return -1;
    if (name) {
        tmp = self->name;
        Py_XINCREF(name);
        self->name = name;
        Py_XDECREF(tmp);
    }else{
        self->name = Py_None;
    }
    return 0;
}

static PyObject * {{ class_name|lower }}_getname({{ class_name }} *self, void *closure)
{
    Py_XINCREF(self->name);
    return self->name;
}

static int {{ class_name|lower }}_setname({{ class_name }} *self, PyObject *value, void *closure)
{
    if (value == NULL) {
        PyErr_SetString(PyExc_TypeError, "Cannot delete the name attribute");
        return -1;
    }
    if (!PyUnicode_Check(value)) {
        PyErr_SetString(PyExc_TypeError, "The first attribute value must be a string");
        return -1;
    }
    Py_XDECREF(self->name);
    Py_XINCREF(value);
    self->name = value;
    return 0;
}

static PyGetSetDef {{ class_name|lower }}_getseters[] = {
    {"name", (getter){{ class_name|lower }}_getname, (setter){{ class_name|lower }}_setname, "name", NULL},
    {NULL}  /* Sentinel */
};

static PyTypeObject {{ class_name|lower }}_type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    "_{{ class_name|lower }}._{{ class_name }}",
    sizeof({{ class_name }}),
    0,
    (destructor){{ class_name|lower }}_dealloc,/* tp_dealloc */
    0,                         /* tp_print */
    0,                         /* tp_getattr */
    0,                         /* tp_setattr */
    0,                         /* tp_compare */
    0,                         /* tp_repr */
    0,                         /* tp_as_number */
    0,                         /* tp_as_sequence */
    0,                         /* tp_as_mapping */
    0,                         /* tp_hash */
    0,                         /* tp_call */
    0,                         /* tp_str */
    0,                         /* tp_getattro */
    0,                         /* tp_setattro */
    0,                         /* tp_as_buffer */
    Py_TPFLAGS_DEFAULT |Py_TPFLAGS_BASETYPE,   /* tp_flags */
    "{{ class_name }} objects",           /* tp_doc */
    0,                         /* tp_traverse */
    0,                         /* tp_clear */
    0,                         /* tp_richcompare */
    0,                         /* tp_weaklistoffset */
    0,                         /* tp_iter */
    0,                         /* tp_iternext */
    {{ class_name|lower }}_methods,             /* tp_methods */
    {{ class_name|lower }}_members,             /* tp_members */
    {{ class_name|lower }}_getseters,           /* tp_getset */
    0,                         /* tp_base */
    0,                         /* tp_dict */
    0,                         /* tp_descr_get */
    0,                         /* tp_descr_set */
    0,                         /* tp_dictoffset */
    (initproc){{ class_name|lower }}_init,      /* tp_init */
    0,                         /* tp_alloc */
    {{ class_name|lower }}_new,          /* tp_new */
};

static PyMethodDef module_methods[] = {
    {"test",test,METH_VARARGS,"test function"},
    {NULL}  /* Sentinel */
};

static PyModuleDef {{ module_name }}_module = {
    PyModuleDef_HEAD_INIT,
    "{{ module_name }}",
    "{{ module_name }} module",
    -1,
    module_methods, NULL, NULL, NULL, NULL
};

PyMODINIT_FUNC PyInit_{{ module_name }}(void) {
    PyObject* m;
    {{ class_name|lower }}_type.tp_new = PyType_GenericNew;
    if (PyType_Ready(&{{ class_name|lower }}_type) < 0)
        return NULL;
    m = PyModule_Create(&{{ module_name }}_module);
    if (m == NULL)
        return NULL;
    Py_INCREF(&{{ class_name|lower }}_type);
    PyModule_AddObject(m, "__version__", Py_BuildValue("s", "0.1"));
    PyModule_AddObject(m, "_{{ class_name }}", (PyObject *)&{{ class_name|lower }}_type);
    return m;
}