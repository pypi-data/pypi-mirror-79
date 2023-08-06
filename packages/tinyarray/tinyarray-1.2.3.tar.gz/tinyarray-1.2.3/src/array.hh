// Copyright 2012-2013 Tinyarray authors.
//
// This file is part of Tinyarray.  It is subject to the license terms in the
// file LICENSE.rst found in the top-level directory of this distribution and
// at https://gitlab.kwant-project.org/kwant/tinyarray/blob/master/LICENSE.rst.
// A list of Tinyarray authors can be found in the README.rst file at the
// top-level directory of this distribution and at
// https://gitlab.kwant-project.org/kwant/tinyarray.

#ifndef ARRAY_HH
#define ARRAY_HH

#include <complex>
typedef std::complex<double> Complex;

const int max_ndim = 16;

// First constant must be 0, the last one must be `NONE'.
enum Dtype {LONG = 0, DOUBLE, COMPLEX, NONE};
const Dtype default_dtype = DOUBLE;
#define DEFAULT_DTYPE "float"

extern const char *dtype_names[];

#define DTYPE_DISPATCH(func) {func<long>, func<double>, func<Complex>}

// First constant must be 0, the last one must be `UNKNOWN'.
enum Format {INT32_LE = 0, INT32_BE, INT64_LE, INT64_BE,
             FLOAT64_LE, FLOAT64_BE, COMPLEX128_LE, COMPLEX128_BE,
             UNKNOWN};

extern const char *format_names[];

extern Format format_by_dtype[];

// We use the ob_size field in a clever way to encode either the length of a
// 1-d array, or the number of dimensions for multi-dimensional arrays.  The
// following code codifies the conventions.
class Array_base {
public:
    void ndim_shape(int *ndim, size_t **shape) const {
        const Py_ssize_t ob_size = ob_base.ob_size;
        if (ob_size >= 0) {
            if (ndim) *ndim = 1;
            if (shape) *shape = (size_t*)&ob_base.ob_size;
        } else if (ob_size < -1) {
            if (ndim) *ndim = static_cast<int>(-ob_size);
            if (shape) *shape = (size_t*)((char*)this + sizeof(Array_base));
        } else {
            if (ndim) *ndim = 0;
            if (shape) *shape = 0;
        }
    }

protected:
    PyVarObject ob_base;
};

// Python 3 support macros for module creation
#if PY_MAJOR_VERSION >= 3
    // module creation
    #define MOD_DEF(ob, name, methods, doc) \
    static struct PyModuleDef moduledef = { \
        PyModuleDef_HEAD_INIT, \
        name, \
        doc, \
        -1, \
        methods, \
    }; \
    ob = PyModule_Create(&moduledef);
    // init function declaration
    #define MOD_INIT_FUNC(name) PyMODINIT_FUNC PyInit_##name()
    // init function declaration for use in Array class def
    #define MOD_INIT_FRIEND(name) PyObject* PyInit_##name()
    // init function return values
    #define MOD_ERROR_VAL NULL
    #define MOD_SUCCESS_VAL(val) val
// Python 2
#else
    // module creation
    #define MOD_DEF(ob, name, methods, doc) \
    ob = Py_InitModule3(name, methods, doc);
    // init function declaration
    #define MOD_INIT_FUNC(name) PyMODINIT_FUNC init##name()
    // init function declaration for use in Array class def
    #define MOD_INIT_FRIEND(name) void init##name()
    // init function return values
    #define MOD_ERROR_VAL
    #define MOD_SUCCESS_VAL(val)
#endif

MOD_INIT_FUNC(tinyarray);

template <typename T>
class Array : public Array_base {
public:
    T *data() {
        if (ob_base.ob_size >= -1) {
            // ndim == 0 or 1
            return ob_item;
        } else {
            // ndim > 1
            return ob_item + (-ob_base.ob_size * sizeof(size_t) +
                              sizeof(T) - 1) / sizeof(T);
        }
    }

    ssize_t object_size() const;

    static bool check_exact(PyObject *candidate) {
        return (Py_TYPE(candidate) == &pytype);
    }

    static Array<T> *make(int ndim, size_t size);
    static Array<T> *make(int ndim, const size_t *shape, size_t *size = 0);

    static const char *pyname, *pyformat;
private:
    T ob_item[1];

    static PyMethodDef methods[];
    static PySequenceMethods as_sequence;
    static PyMappingMethods as_mapping;
    static PyBufferProcs as_buffer;
    static PyNumberMethods as_number;
    static PyTypeObject pytype;

    friend Dtype get_dtype(PyObject *obj);
    friend MOD_INIT_FRIEND(tinyarray);
};

int load_index_seq_as_long(PyObject *obj, long *out, int maxlen);
int load_index_seq_as_ulong(PyObject *obj, unsigned long *uout,
                            int maxlen, const char *errmsg = 0);

inline size_t calc_size(int ndim, const size_t *shape)
{
    if (ndim == 0) return 1;
    size_t result = shape[0];
    for (int d = 1; d < ndim; ++d) result *= shape[d];
    return result;
}

inline Dtype get_dtype(PyObject *obj)
{
    PyTypeObject *pytype = Py_TYPE(obj);
    if (pytype == &Array<long>::pytype) return LONG;
    if (pytype == &Array<double>::pytype) return DOUBLE;
    if (pytype == &Array<Complex>::pytype) return COMPLEX;
    return NONE;
}

PyObject *array_from_arraylike(PyObject *in, Dtype *dtype,
                               Dtype dtype_min = Dtype(0),
                               bool as_matrix = false);

// Coerced_dtype will contain the common dtype of the coerced arrays.
int coerce_to_arrays(PyObject **a, PyObject **b, Dtype *coerced_dtype);

template <typename T> PyObject *transpose(PyObject *in, PyObject *dummy);

template <typename T>
ssize_t Array<T>::object_size() const
{
    int ndim;
    size_t *shape;
    ndim_shape(&ndim, &shape);

    // this does the same calculation as in Array<T>::make
    Py_ssize_t size = calc_size(ndim, shape);
    if (ndim > 1)
        // if array is > 1D then the shape is stored in
        // the start of the data buffer
        size += (ndim * sizeof(size_t) + sizeof(T) - 1) / sizeof(T);
    size = size * sizeof(T);  // element count -> byte count
    size += Array<T>::pytype.tp_basicsize;  // add Python object overhead

    return size;
}

#endif // !ARRAY_HH
