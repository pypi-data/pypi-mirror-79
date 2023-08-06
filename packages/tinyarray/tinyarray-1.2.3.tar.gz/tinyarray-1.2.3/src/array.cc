// Copyright 2012-2016 Tinyarray authors.
//
// This file is part of Tinyarray.  It is subject to the license terms in the
// file LICENSE.rst found in the top-level directory of this distribution and
// at https://gitlab.kwant-project.org/kwant/tinyarray/blob/master/LICENSE.rst.
// A list of Tinyarray authors can be found in the README.rst file at the
// top-level directory of this distribution and at
// https://gitlab.kwant-project.org/kwant/tinyarray.

#include <Python.h>
#include <cstddef>
#include <sstream>
#include <limits>
#include <algorithm>
#include "array.hh"
#include "arithmetic.hh"
#include "functions.hh"
#include "conversion.hh"
#include "version.hh"

template <>
const char *Array<long>::pyformat = "l";
template <>
const char *Array<double>::pyformat = "d";
template <>
const char *Array<Complex>::pyformat = "Zd";

const char *dtype_names[] = {"int", "float", "complex"};

const char *format_names[] = {
    "int32 little endian", "int32 big endian",
    "int64 little endian", "int64 big endian",
    "float64 little endian", "float64 big endian",
    "complex128 little endian", "complex128 big endian",
    "unknown"};

Format format_by_dtype[NONE];

namespace {

bool is_big_endian()
{
    union {
        unsigned int i;
        char c[4];
    } bint = {0x0a0b0c0d};

    if (bint.c[0] == 0x0a) {
        assert(bint.c[1] == 0x0b);
        assert(bint.c[2] == 0x0c);
        assert(bint.c[3] == 0x0d);
        return true;
    } else {
        assert(bint.c[0] == 0x0d);
        assert(bint.c[1] == 0x0c);
        assert(bint.c[2] == 0x0b);
        assert(bint.c[3] == 0x0a);
        return false;
    }
}

PyObject *int_str, *long_str, *float_str, *complex_str, *index_str,
    *reconstruct;

Dtype dtype_of_scalar(PyObject *obj)
{
    if (PyComplex_Check(obj)) return COMPLEX;
    if (PyFloat_Check(obj)) return DOUBLE;
    if (PyInt_Check(obj)) return LONG;
    // TODO: The following line should be removed for Python 3.
    if (PyLong_Check(obj)) return LONG;
    if (PyObject_HasAttr(obj, index_str)) return LONG;

    if (PyObject_HasAttr(obj, complex_str)) return COMPLEX;
    if (PyObject_HasAttr(obj, float_str)) return DOUBLE;
    if (PyObject_HasAttr(obj, int_str)) return LONG;
    // TODO: The following line should be removed for Python 3.
    if (PyObject_HasAttr(obj, long_str)) return LONG;

    return NONE;
}

Dtype dtype_of_buffer(Py_buffer *view)
{
    const char *fmt = view->format;
    Dtype dtype = NONE;

    // Currently, we only understand native endianness and alignment.
    if (*fmt == '@') fmt++;

    if (strchr("cbB?hHiIlLqQnN", *fmt)) {
        dtype = LONG;
        fmt++;
    } else if (strchr("fdg", *fmt)) {
        dtype = DOUBLE;
        fmt++;
    } else if (*fmt == 'Z') {
        fmt++;
        if (strchr("fdg", *fmt)) {
            dtype = COMPLEX;
        }
        fmt++;
    }

    // Right now, no composite data structures are supported; if we found a
    // single supported data type, we should be at the end of the string.
    if (*fmt != '\0') return NONE;

    return dtype;
}

template<typename O, typename I>
PyObject *convert_array(PyObject *in_, int ndim, size_t *shape)
{
    assert(Array<I>::check_exact(in_)); Array<I> *in = (Array<I>*)in_;
    size_t size;
    if (ndim == -1) {
        assert(shape == 0);
        in->ndim_shape(&ndim, &shape);
    } else {
#ifndef NDEBUG
        int in_ndim;
        size_t *in_shape;
        in->ndim_shape(&in_ndim, &in_shape);
        assert(shape);
        assert(calc_size(ndim, shape) == calc_size(in_ndim, in_shape));
#endif
    }
    Array<O> *out = Array<O>::make(ndim, shape, &size);
    I *src = in->data();
    O *dest = out->data();
    for (size_t i = 0; i < size; ++i) dest[i] = src[i];
    return (PyObject*)out;
}

typedef PyObject *Convert_array(PyObject*, int, size_t*);

Convert_array *convert_array_dtable[][3] = {
    {convert_array<long, long>,
     convert_array<long, double>,
     0},
    {convert_array<double, long>,
     convert_array<double, double>,
     0},
    {convert_array<Complex, long>,
     convert_array<Complex, double>,
     convert_array<Complex, Complex>}
};

PyObject *convert_array(Dtype dtype_out, PyObject *in, Dtype dtype_in,
                        int ndim = -1, size_t *shape = 0)
{
    if (dtype_in == NONE)
        dtype_in = get_dtype(in);
    assert(get_dtype(in) == get_dtype(in));
    Convert_array *func = convert_array_dtable[int(dtype_out)][int(dtype_in)];
    if (!func) {
        PyErr_Format(PyExc_TypeError, "Cannot convert %s to %s.",
                     dtype_names[int(dtype_in)], dtype_names[int(dtype_out)]);
        return 0;
    }
    return func(in, ndim, shape);
}

const char *seq_err_msg =
    "A sequence does not support sequence protocol - "
    "this is probably due to a bug in numpy for 0-d arrays.";

// This function determines the shape of an array-like sequence (of
// sequences...) given to it as first parameter.  `dtype_guess' is the dtype of
// the first element of the sequence.
//
// All four arguments after the first one are written to. `shape' and `seqs'
// must have space for at least `max_ndim' elements.
//
// After successful execution `seqs' will contain `ndim' new references
// returned by PySequence_Fast.
int examine_sequence(PyObject *arraylike, int *ndim, size_t *shape,
                     PyObject **seqs, Dtype *dtype_guess)
{
    PyObject *p = arraylike;
    int d = -1;
    assert(PySequence_Check(p));
    for (bool is_sequence = true; ; is_sequence = PySequence_Check(p)) {
        if (is_sequence) {
            ++d;
            if (d == ptrdiff_t(max_ndim)) {
                // Strings are, in a way, infinitely nested sequences because
                // the first element of a string is a again a string.
                if (PyString_Check(p))
                    PyErr_SetString(PyExc_TypeError, "Expecting a number.");
                else
                    PyErr_SetString(PyExc_ValueError, "Too many dimensions.");
                --d;
                goto fail;
            }
        } else {
            // We are in the innermost sequence.  Determine the dtype if
            // requested.
            if (dtype_guess) {
                *dtype_guess = dtype_of_scalar(p);
                if (*dtype_guess == NONE) {
                    PyErr_SetString(PyExc_TypeError, "Expecting a number.");
                    goto fail;
                }
            }
            break;
        }

        // See https://github.com/numpy/numpy/issues/652.
        seqs[d] = PySequence_Fast(p, seq_err_msg);
        if (!seqs[d]) {--d; goto fail;}

        if ((shape[d] = PySequence_Fast_GET_SIZE(seqs[d]))) {
            p = *PySequence_Fast_ITEMS(seqs[d]);
        } else {
            // We are in the innermost sequence which is empty.
            if (dtype_guess) *dtype_guess = NONE;
            break;
        }
    }
    *ndim = d + 1;
    return 0;

fail:
    for (; d >= 0; --d) Py_DECREF(seqs[d]);
    return -1;
}

// This function is designed to be run after examine_sequence.  It takes care
// of releasing the references passed to it in seqs.
template <typename T>
int readin_seqs(PyObject **seqs, T *dest, int ndim, const size_t *shape,
                bool exact)
{
    assert(ndim > 0);

    // seqs is the stack of sequences being processed, all returned by
    // PySequence_Fast.  ps[d] and es[d] are the begin and end of the elements
    // of seqs[d - 1].
    PyObject **ps[max_ndim], **es[max_ndim];
    es[0] = ps[0] = 0;

    for (int d = 1; d < ndim; ++d) {
        PyObject **p = PySequence_Fast_ITEMS(seqs[d - 1]);
        ps[d] = p + 1;
        es[d] = p + shape[d - 1];
    }

    int d = ndim - 1;
    size_t len = shape[d];
    PyObject **p = PySequence_Fast_ITEMS(seqs[d]), **e = p + len;
    while (true) {
        if (len && PySequence_Check(p[0])) {
            if (d + 1 == ndim) {
                PyErr_SetString(PyExc_ValueError,
                                "Input has irregular nesting depth.");
                goto fail;
            }
            ++d;
            ps[d] = p;
            es[d] = e;
        } else {
            // Read-in a leaf sequence.
            while (p < e) {
                T value;
                if (exact)
                    value = number_from_pyobject_exact<T>(*p++);
                else
                    value = number_from_pyobject<T>(*p++);
                if (value == T(-1) && PyErr_Occurred()) goto fail;
                *dest++ = value;
            }
            Py_DECREF(seqs[d]);

            while (ps[d] == es[d]) {
                if (d == 0) {
                    // Success!
                    return 0;
                }
                --d;
                Py_DECREF(seqs[d]);
            }
            if (!PySequence_Check(*ps[d])) {
                --d;
                PyErr_SetString(PyExc_ValueError,
                                "Input has irregular nesting depth.");
                goto fail;
            }
        }

        // See https://github.com/numpy/numpy/issues/652.
        seqs[d] = PySequence_Fast(*ps[d]++, seq_err_msg);
        if (!seqs[d]) {--d; goto fail;}
        len = PySequence_Fast_GET_SIZE(seqs[d]);

        // Verify that the length of the current sequence agrees with the
        // shape.
        if (len != shape[d]) {
            PyErr_SetString(PyExc_ValueError,
                            "Input has irregular shape.");
            goto fail;
        }

        p = PySequence_Fast_ITEMS(seqs[d]);
        e = p + len;
    }

fail:
    while (true) {
        Py_DECREF(seqs[d]);
        if (d == 0) break;
        --d;
    }
    return -1;
}

template <typename T>
PyObject *readin_seqs_into_new(PyObject **seqs, int ndim_in, int ndim_out,
                               const size_t *shape_out, bool exact)
{
    Array<T> *result = Array<T>::make(ndim_out, shape_out);
    assert(ndim_out >= ndim_in);
#ifndef NDEBUG
    for (int d = 0, e = ndim_out - ndim_in; d < e; ++d)
        assert(shape_out[d] == 1);
#endif
    if (result == 0) return 0;
    if (readin_seqs<T>(seqs, result->data(), ndim_in,
                       shape_out + ndim_out - ndim_in, exact)
        == -1) {
        Py_DECREF(result);
        return 0;
    }
    return (PyObject*)result;
}

PyObject *(*readin_seqs_into_new_dtable[])(
    PyObject**, int, int, const size_t*, bool) =
    DTYPE_DISPATCH(readin_seqs_into_new);

template <typename T>
PyObject *readin_scalar_into_new(PyObject *in, bool exact, int ndim = 0)
{
    T value;
    if (exact)
        value = number_from_pyobject_exact<T>(in);
    else
        value = number_from_pyobject<T>(in);

    if (value == T(-1) && PyErr_Occurred()) return 0;

    Array<T> *result = Array<T>::make(ndim, 1);
    *result->data() = value;

    size_t *shape;
    result->ndim_shape(0, &shape);
    for (int d = 0; d < ndim; ++d) shape[d] = 1;

    return (PyObject*)result;
}

PyObject *(*readin_scalar_into_new_dtable[])(PyObject*, bool, int) =
    DTYPE_DISPATCH(readin_scalar_into_new);

int examine_buffer(PyObject *in, Py_buffer *view, Dtype *dtype)
{
    if (!PyObject_CheckBuffer(in)) return -1;
    Dtype dt = NONE;
    memset(view, 0, sizeof(Py_buffer));

    // I don't know if the following makes much sense: I try to get the buffer
    // using less and less demanding flags. NumPy does the same.
    if (PyObject_GetBuffer(in, view, PyBUF_ND | PyBUF_FORMAT) == 0)
        dt = dtype_of_buffer(view);
    else if (PyObject_GetBuffer(in, view, PyBUF_STRIDES | PyBUF_FORMAT) == 0)
        dt = dtype_of_buffer(view);
    else if (PyObject_GetBuffer(in, view, PyBUF_FULL_RO) == 0)
        dt = dtype_of_buffer(view);
    PyErr_Clear();

    // Check if the buffer can actually be converted into one of our
    // formats.
    if (dt == NONE) return -1;

    if (dtype) *dtype = dt;
    return 0;
}

template<typename T>
T (*get_buffer_converter_complex(const char *fmt))(const void *);

template<>
long (*get_buffer_converter_complex(const char *))(const void *)
{
    // Complex can only be cast to complex.
    PyErr_Format(PyExc_TypeError, "Complex cannot be cast to int.");

    return 0;
}

template<>
double (*get_buffer_converter_complex(const char *))(const void *)
{
    // complex can only be cast to complex
    PyErr_Format(PyExc_TypeError, "Complex cannot be cast to float.");

    return 0;
}

template<>
Complex (*get_buffer_converter_complex(const char *fmt))(const void *)
{
    switch(*(fmt + 1)){
    case 'f':
        return number_from_ptr<Complex,  std::complex<float> >;
    case 'd':
        return number_from_ptr<Complex, std::complex<double> >;
    case 'g':
        return number_from_ptr<Complex, std::complex<long double> >;
    }

    return 0;
}

template<typename T>
T (*get_buffer_converter(Py_buffer *view))(const void *)
{
    // currently, we only understand native endianness and alignment
    char *fmt = view->format;

    if (*fmt == '@') {
        fmt++;
    }

    switch(*fmt) {
    case 'c':
        return number_from_ptr<T, char>;
    case 'b':
        return number_from_ptr<T, signed char>;
    case 'B':
        return number_from_ptr<T, unsigned char>;
    case '?':
        return number_from_ptr<T, bool>;
    case 'h':
        return number_from_ptr<T, short>;
    case 'H':
        return number_from_ptr<T, unsigned short>;
    case 'i':
        return number_from_ptr<T, int>;
    case 'I':
        return number_from_ptr<T, unsigned int>;
    case 'l':
        return number_from_ptr<T, long>;
    case 'L':
        return number_from_ptr<T, unsigned long>;
    case 'q':
        return number_from_ptr<T, long long>;
    case 'Q':
        return number_from_ptr<T, unsigned long long>;
    case 'n':
        return number_from_ptr<T, ssize_t>;
    case 'N':
        return number_from_ptr<T, size_t>;
    case 'f':
        return number_from_ptr<T, float>;
    case 'd':
        return number_from_ptr<T, double>;
    case 'g':
        return number_from_ptr<T, long double>;
    case 'Z':
        return get_buffer_converter_complex<T>(fmt);
    }

    return 0;
}

template<typename T>
int readin_buffer(T *dest, Py_buffer *view)
{
    if (view->len == 0) return 0;

    T (*number_from_ptr)(const void *) = get_buffer_converter<T>(view);
    if (!number_from_ptr) return -1;

    if (view->ndim == 0) {
        *dest = (*number_from_ptr)(view->buf);
        if (PyErr_Occurred()) return -1;
        else return 0;
    }

    Py_ssize_t indices[max_ndim];
    for (int i = 0; i < view->ndim; i++) {
        indices[i] = 0;
    }

    if (view->suboffsets) {
        while(indices[0] < view->shape[0]) {
            char *pointer = (char*)view->buf;
            for (int i = 0; i < view->ndim; i++) {
                pointer += view->strides[i] * indices[i];
                if (view->suboffsets[i] >=0 ) {
                    pointer = *((char**)pointer) + view->suboffsets[i];
                }
            }

            *dest++ = (*number_from_ptr)(pointer);
            if (PyErr_Occurred()) return -1;

            indices[view->ndim-1]++;

            for (int i = view->ndim - 1; i > 0; i--) {
                if (indices[i] < view->shape[i]) break;
                assert(indices[i] == view->shape[i]);
                indices[i-1]++;
                indices[i] = 0;
            }
        }
    } else if (view->strides) {
        char *ptr = (char *)view->buf;

        while(indices[0] < view->shape[0]) {
            *dest++ = (*number_from_ptr)(ptr);
            if (PyErr_Occurred()) return -1;

            indices[view->ndim-1]++;
            ptr += view->strides[view->ndim-1];

            for (int i = view->ndim - 1; i > 0; i--) {
                if (indices[i] < view->shape[i]) break;
                assert(indices[i] == view->shape[i]);
                indices[i-1]++;
                ptr += view->strides[i-1];
                indices[i] = 0;
                ptr -= view->strides[i] * view->shape[i];
            }
        }
    } else {
        // Must be C-contiguous.
        char *end = (char *)view->buf + view->len;
        char *p = (char *)view->buf;
        while(p < end) {
            *dest++ = (*number_from_ptr)(p);
            if (PyErr_Occurred()) return -1;

            p += view->itemsize;
        }
    }

    return 0;
}

template <typename T>
PyObject *make_and_readin_buffer(Py_buffer *view, int ndim_out,
                                 const size_t *shape_out)
{
    Array<T> *result = Array<T>::make(ndim_out, shape_out);
    assert(ndim_out >= view->ndim);
#ifndef NDEBUG
    for (int d = 0, e = ndim_out - view->ndim; d < e; ++d)
        assert(shape_out[d] == 1);
#endif
    if (result == 0) return 0;
    if (readin_buffer<T>(result->data(), view) == -1) {
        Py_DECREF(result);
        return 0;
    }
    return (PyObject*)result;
}

PyObject *(*make_and_readin_buffer_dtable[])(
    Py_buffer *, int, const size_t*) = DTYPE_DISPATCH(make_and_readin_buffer);

template <typename T>
PyObject *to_pystring(Array<T> *self, PyObject* to_str(PyObject *),
                      const char *header, const char *trailer,
                      const char *indent, const char *separator)
{
    int ndim;
    size_t *shape;
    self->ndim_shape(&ndim, &shape);

    std::ostringstream o;
    o << header;

    const T *p = self->data();
    if (ndim > 0) {
        int d = 0;
        size_t i[max_ndim];
        i[0] = shape[0];

        o << '[';
        while (true) {
            if (i[d]) {
                --i[d];
                if (d < ndim - 1) {
                    o << '[';
                    ++d;
                    i[d] = shape[d];
                } else {
                    PyObject *num = pyobject_from_number(*p++);
                    PyObject *str = to_str(num);
                    o << PyString_AsString(str);
                    Py_DECREF(str);
                    Py_DECREF(num);
                    if (i[d] > 0) o << separator << ' ';
                }
            } else {
                o << ']';
                if (d == 0) break;
                --d;
                if (i[d]) {
                    o << separator << "\n " << indent;
                    for (int i = 0; i < d; ++i) o << ' ';
                }
            }
        }
    } else {
        PyObject *num = pyobject_from_number(*p);
        PyObject *str = to_str(num);
        o << PyString_AsString(str);
        Py_DECREF(str);
        Py_DECREF(num);
    }
    o << trailer;

    return PyString_FromString(o.str().c_str());
}

template <typename T>
PyObject *repr(PyObject *obj)
{
    Array<T> *self = reinterpret_cast<Array<T> *>(obj);
    return to_pystring(self, PyObject_Repr, "array(", ")", "      ", ",");
}

template <typename T>
PyObject *str(PyObject *obj)
{
    Array<T> *self = reinterpret_cast<Array<T> *>(obj);
    return to_pystring(self, PyObject_Str, "", "", "", "");
}

Py_ssize_t len(Array_base *self)
{
    int ndim;
    size_t *shape;
    self->ndim_shape(&ndim, &shape);
    if (ndim == 0) {
        PyErr_SetString(PyExc_TypeError, "len() of unsized object.");
        return -1;
    }
    return shape[0];
}

Py_ssize_t index_from_key(int ndim, const size_t *shape, PyObject *key)
{
    long indices[max_ndim];
    int res = load_index_seq_as_long(key, indices, max_ndim);
    if (res == -1) {
        PyErr_SetString(PyExc_IndexError, "Invalid index.");
        return -1;
    }
    if (res != ndim) {
        PyErr_SetString(PyExc_IndexError, "Number of indices "
                        "must be equal to number of dimensions.");
        return -1;
    }

    int d = 0;
    Py_ssize_t s = shape[0];
    Py_ssize_t index = indices[0];
    if (index < 0) index += s;
    if (index < 0 || index >= s) goto out_of_range;
    for (d = 1; d < ndim; ++d) {
        s = shape[d];
        Py_ssize_t i = indices[d];
        if (i < 0) i += s;
        if (i < 0 || i >= s) goto out_of_range;
        index *= s;
        index += i;
    }
    return index;

out_of_range:
    PyErr_Format(PyExc_IndexError, "Index %ld out of range "
                 "(-%lu <= index < %lu) in dimension %d.",
                 indices[d], (unsigned long)s, (unsigned long)s, d);
    return -1;
}

template <typename T>
PyObject *getitem(PyObject *obj, PyObject *key)
{
    Array<T> *self = reinterpret_cast<Array<T> *>(obj);

    if (PySlice_Check(key)) {
        PyErr_SetString(PyExc_NotImplementedError,
                        "Slices are not implemented.");
        return 0;
    } else {
        int ndim;
        size_t *shape;
        self->ndim_shape(&ndim, &shape);
        T *data = self->data();
        Py_ssize_t index = index_from_key(ndim, shape, key);
        if (index == -1) return 0;
        return pyobject_from_number(data[index]);
    }
}

template <typename T>
PyObject *seq_getitem(PyObject *obj, Py_ssize_t index)
{
    int ndim;
    size_t *shape;
    Array<T> *self = reinterpret_cast<Array<T> *>(obj);
    self->ndim_shape(&ndim, &shape);
    assert(ndim != 0);

    if (index < 0) index += shape[0];
    if (size_t(index) >= shape[0]) {
        PyErr_SetString(PyExc_IndexError, "Invalid index.");
        return 0;
    }

    T *src = self->data();
    if (ndim == 1) {
        assert(index >= 0);
        assert(size_t(index) < shape[0]);
        return pyobject_from_number(src[index]);
    }

    assert(ndim > 1);
    size_t item_size;
    Array<T> *result = Array<T>::make(ndim - 1, shape + 1, &item_size);
    if (!result) return 0;
    src += index * item_size;
    T *dest = result->data();
    for (size_t i = 0; i < item_size; ++i) dest[i] = src[i];
    return (PyObject*)result;
}

template <typename T>
int getbuffer(PyObject *obj, Py_buffer *view, int flags)
{
    int ndim;
    size_t *shape, size;
    Array<T> *self = reinterpret_cast<Array<T> *>(obj);

    assert(view);
    if ((flags & PyBUF_F_CONTIGUOUS) == PyBUF_F_CONTIGUOUS) {
        PyErr_SetString(PyExc_BufferError,
                        "Tinyarrays are not Fortran contiguous.");
        goto fail;
    }
    // The following has been commented out as a workaround for Cython's
    // inability to deal with read-only buffers.
    //
    // if ((flags & PyBUF_WRITEABLE) == PyBUF_WRITEABLE) {
    //     PyErr_SetString(PyExc_BufferError, "Tinyarrays are not writeable");
    //     goto fail;
    // }

    self->ndim_shape(&ndim, &shape);
    size = calc_size(ndim, shape);

    view->buf = self->data();
    view->itemsize = sizeof(T);
    view->len = size * view->itemsize;
    view->readonly = 1;
    if ((flags & PyBUF_FORMAT) == PyBUF_FORMAT)
        view->format = (char*)Array<T>::pyformat;
    else
        view->format = 0;
    if ((flags & PyBUF_ND) == PyBUF_ND) {
        view->ndim = ndim;
        view->shape = (Py_ssize_t*)shape;
        // From the documentation it's not clear whether it is allowed not to
        // set strides to NULL (for C continuous arrays), but it works, so we
        // do it.  However, there is a bug in current numpy
        // (http://projects.scipy.org/numpy/ticket/2197) which requires strides
        // if view->len == 0.  Because we don't have proper strides, we just
        // set strides to shape.  This dirty trick seems to work well -- no one
        // looks at strides when len == 0.
        if (size != 0)
            view->strides = 0;
        else
            view->strides = (Py_ssize_t*)shape;
    } else {
        view->ndim = 0;
        view->shape = 0;
        view->strides = 0;
    }
    view->internal = 0;
    view->suboffsets = 0;

    // Success.
    Py_INCREF(self);
    view->obj = (PyObject*)self;

    return 0;

fail:
    view->obj = 0;
    return -1;
}

// Given the same input, these hash functions return the same result as those
// in Python.  As tinyarrays compare equal to equivalent tuples it is important
// for the hashes to agree.  If not, there will be problems with dictionaries.

#if PY_MAJOR_VERSION >= 3

// the only documentation for this is in the Python sourcecode
const Py_hash_t HASH_IMAG = _PyHASH_IMAG;

Py_hash_t hash(long x)
{
    // For integers the hash is just the integer itself modulo _PyHASH_MODULUS
    // except for the singular case of -1.
    // define 'sign' of the correct width to avoid overflow
    Py_hash_t sign = x < 0 ? -1 : 1;
    Py_hash_t result = sign * ((sign * x) % _PyHASH_MODULUS);
    return result == -1 ? -2 : result;
}

#else

/* In Python 2 hashes were long integers, as indicated by
   https://github.com/python/cpython/blob/2.7/Include/object.h#L314
*/
typedef long Py_hash_t;
typedef unsigned long Py_uhash_t;
const Py_hash_t HASH_IMAG = 1000003L;

Py_hash_t hash(long x)
{
    return x != -1 ? x : -2;
}

#endif

Py_hash_t hash(double x)
{
    // We used to have our own implementation of this, but the extra function
    // call is quite negligible compared to the execution time of the function.
    return _Py_HashDouble(x);
}

Py_hash_t hash(Complex x)
{
    // x.imag == 0  =>  hash(x.imag) == 0  =>  hash(x) == hash(x.real)
    return hash(x.real()) + HASH_IMAG * hash(x.imag());
}

// The following routine calculates the hash of a multi-dimensional array.  The
// hash is equal to that of an arrangement of nested tuples equivalent to the
// array.
//
// It exists in two versions because Python's tuplehash has changed in Python
// 3.8 with the following motivation: "The hash function for tuples is now
// based on xxHash which gives better collision results on (formerly)
// pathological cases. Additionally, on 64-bit systems it improves tuple hashes
// in general."

#if (PY_MAJOR_VERSION < 3 || PY_MINOR_VERSION < 8) && PY_MAJOR_VERSION < 4

// Version for Python < 3.8
template <typename T>
Py_hash_t hash(PyObject *obj)
{
    int ndim;
    size_t *shape;
    Array<T> *self = reinterpret_cast<Array<T> *>(obj);
    self->ndim_shape(&ndim, &shape);
    T *p = self->data();
    if (ndim == 0) return hash(*p);

    const Py_uhash_t mult_init = 1000003, r_init = 0x345678;
    const Py_uhash_t mul_addend = 82520, r_addend = 97531;
    Py_ssize_t i[max_ndim];
    Py_uhash_t mult[max_ndim], r[max_ndim];
    --ndim;                     // For convenience.
    int d = 0;
    i[0] = shape[0];
    mult[0] = mult_init;
    r[0] = r_init;
    while (true) {
        if (i[d]) {
            --i[d];
            if (d == ndim) {
                // Innermost loop body.
                r[d] = (r[d] ^ hash(*p++)) * mult[d];
                mult[d] += mul_addend + 2 * i[d];
            } else {
                // Entering a loop.
                ++d;
                i[d] = shape[d];
                mult[d] = mult_init;
                r[d] = r_init;
            }
        } else {
            // Exiting a loop.
            if (d == 0) {
                // Exiting the outermost loop.
                Py_uhash_t r_next = r[0] + r_addend;
                return r_next == Py_uhash_t(-1) ? -2 : r_next;
            }
            --d;
            Py_uhash_t r_next = r[d+1] + r_addend;
            r_next = r_next == Py_uhash_t(-1) ? -2 : r_next;
            r[d] = (r[d] ^ r_next) * mult[d];
            mult[d] += mul_addend + 2 * i[d];
        }
    }
}

#else

#if SIZEOF_PY_UHASH_T > 4

const Py_uhash_t _hash_init = 2870177450012600261U;

inline void _hash_inner_loop(Py_uhash_t &acc, Py_uhash_t lane)
{
    acc += lane * 14029467366897019727U;
    acc = ((acc << 31) | (acc >> 33)); // Rotate left 31 bits.
    acc *= 11400714785074694791U;
}

#else

const Py_uhash_t _hash_init = 374761393U;

inline void _hash_inner_loop(Py_uhash_t &acc, Py_uhash_t lane)
{
    acc += lane * 2246822519U;
    acc = ((acc << 13) | (acc >> 19)); // Rotate left 13 bits.
    acc *= 2654435761U;
}

#endif

inline Py_uhash_t _hash_loop_end(Py_uhash_t acc, Py_uhash_t len)
{
    acc += len ^ (_hash_init ^ 3527539UL);
    if (acc == Py_uhash_t(-1)) return 1546275796;
    return acc;
}

// Version for Python >= 3.8
template <typename T>
Py_hash_t hash(PyObject *obj)
{
    int ndim;
    size_t *shape;
    Array<T> *self = reinterpret_cast<Array<T> *>(obj);
    self->ndim_shape(&ndim, &shape);
    T *p = self->data();
    if (ndim == 0) return hash(*p);

    Py_ssize_t i[max_ndim];
    Py_uhash_t acc[max_ndim];
    --ndim;                     // For convenience.
    int d = 0;
    i[0] = shape[0];
    acc[0] = _hash_init;
    // The following is equivalent to 'ndim' (the original value) nested loops.
    while (true) {
        if (i[d]) {
            --i[d];
            if (d == ndim) {
                _hash_inner_loop(acc[d], hash(*p++));
            } else {
                ++d;
                i[d] = shape[d];
                acc[d] = _hash_init;
            }
        } else {
            if (d == 0) return _hash_loop_end(acc[0], shape[0]);
            --d;
            _hash_inner_loop(acc[d], _hash_loop_end(acc[d+1], shape[d+1]));
        }
    }
}

#endif

template <typename T>
bool compare_scalar(const int op, const T a, const T b) {
    switch(op){
        case Py_EQ: return a == b;
        case Py_NE: return a != b;
        case Py_LE: return a <= b;
        case Py_GE: return a >= b;
        case Py_LT: return a < b;
        case Py_GT: return a > b;
        default:
           assert(false);  // If we get here something is very wrong.
           return false;   // Stop the compiler complaining.
    }
}


template <>
bool compare_scalar<Complex>(const int op, const Complex a, const Complex b) {
    switch(op){
        case Py_EQ: return a == b;
        case Py_NE: return a != b;
        // This function is never called in a context where
        // the following code path is run -- fall through.
        case Py_LE:
        case Py_GT:
        case Py_LT:
        case Py_GE:
        default:
           assert(false);
           return false;   // Stop the compiler complaining.
    }
}


template <typename T>
bool compare_data(int op, PyObject *a_, PyObject *b_, size_t size)
{
    assert(Array<T>::check_exact(a_)); Array<T> *a = (Array<T>*)a_;
    assert(Array<T>::check_exact(b_)); Array<T> *b = (Array<T>*)b_;
    const T *data_a = a->data();
    const T *data_b = b->data();
    // Sequences are ordered the same as their first differing elements, see:
    // https://docs.python.org/3/reference/expressions.html#value-comparisons
    // comparison for "multidimensional" sequences is identical to comparing
    // the flattened sequences when they have the same shape (the present case).
    size_t i = 0;
    for (; i < size; ++i)
        if (data_a[i] != data_b[i]) break;
    // Any of these operations should return true when objects are equal.
    if (i == size) return ((op == Py_EQ) || (op == Py_LE) || (op == Py_GE));
    // encapsulate this into a function to handle the COMPLEX case
    return compare_scalar<T>(op, data_a[i], data_b[i]);
}

bool (*compare_data_dtable[])(int, PyObject*, PyObject*, size_t) =
    DTYPE_DISPATCH(compare_data);

#if PY_MAJOR_VERSION < 3
    #define PY2_RAISE_TYPEERROR(msg)\
        PyErr_SetString(PyExc_TypeError, msg);\
        return 0
#else
    #define PY2_RAISE_TYPEERROR(msg)
#endif  // PY_MAJOR_VERSION < 3

PyObject *richcompare(PyObject *a, PyObject *b, int op)
{
    PyObject *result;
    const bool equality_comparison = (op == Py_EQ || op == Py_NE);

    // Short circuit when we are comparing the same object.
    bool equal = (a == b);
    if (equal) {
        // Any of these operations should return true when objects are equal
        equal = (op == Py_EQ) || (op == Py_GE) || (op == Py_LE);
        result = equal ? Py_True : Py_False;
        goto done;
    }

    Dtype dtype;
    if (coerce_to_arrays(&a, &b, &dtype) < 0) return 0;

    // Obviate the need for `compare_scalar<Complex` to
    // handle the case of an undefined comparison.
    if (dtype == COMPLEX && !equality_comparison) {
        PY2_RAISE_TYPEERROR("unorderable type: complex()");
        result = Py_NotImplemented;
        goto decref_then_done;
    }

    int ndim_a, ndim_b;
    size_t *shape_a, *shape_b;
    reinterpret_cast<Array_base*>(a)->ndim_shape(&ndim_a, &shape_a);
    reinterpret_cast<Array_base*>(b)->ndim_shape(&ndim_b, &shape_b);

    // TODO: Enable array comparisons between arrays of differing dimensions.
    if (ndim_a != ndim_b) {
        if (equality_comparison) {
            goto equality_then_done;
        } else {
            PY2_RAISE_TYPEERROR("Unorderable type: only arrays with"
                                "the same shape can be ordered.");
            result = Py_NotImplemented;
            goto decref_then_done;
        }
    }
    for (int d = 0; d < ndim_a; ++d) {
        if (shape_a[d] != shape_b[d]) {
            if (equality_comparison) {
                goto equality_then_done;
            } else {
                PY2_RAISE_TYPEERROR("Unorderable type: only arrays with"
                                    "the same shape can be ordered.");
                result = Py_NotImplemented;
                goto decref_then_done;
            }
        }
    }

    // Actually compare the data.
    equal = compare_data_dtable[int(dtype)](op, a, b, calc_size(ndim_a, shape_a));
    result = equal ? Py_True : Py_False;
    goto decref_then_done;

// Non error-path exit points from this function
equality_then_done:
    result = ((op == Py_EQ) == equal) ? Py_True : Py_False;
decref_then_done:
    Py_DECREF(a);
    Py_DECREF(b);
done:
    Py_INCREF(result);
    return result;
}

PyObject *get_dtype_py(PyObject *self, void *)
{
    static PyObject *dtypes[] = {
        (PyObject*)&PyInt_Type,
        (PyObject*)&PyFloat_Type,
        (PyObject*)&PyComplex_Type
    };
    int dtype = int(get_dtype(self));
    assert(dtype < int(NONE));
    Py_INCREF(dtypes[dtype]);
    return dtypes[dtype];
}

PyObject *get_ndim(Array_base *self, void *)
{
    int ndim;
    self->ndim_shape(&ndim, 0);
    return PyLong_FromLong(ndim);
}

PyObject *get_size(Array_base *self, void *)
{
    int ndim;
    size_t *shape;
    self->ndim_shape(&ndim, &shape);
    return PyLong_FromSize_t(calc_size(ndim, shape));
}

PyObject *get_shape(Array_base *self, void *)
{
    int ndim;
    size_t *shape;
    self->ndim_shape(&ndim, &shape);
    size_t result_shape = ndim;
    Array<long> *result = Array<long>::make(1, &result_shape);
    if (!result) return 0;
    long *data = result->data();
    for (int d = 0; d < ndim; ++d) data[d] = shape[d];
    return (PyObject*)result;
}

PyGetSetDef getset[] = {
    {(char*)"dtype", get_dtype_py, 0, 0, 0},
    {(char*)"ndim", (getter)get_ndim, 0, 0, 0},
    {(char*)"size", (getter)get_size, 0, 0, 0},
    {(char*)"shape", (getter)get_shape, 0, 0, 0},
    {0, 0, 0, 0, 0}               // Sentinel
};

// **************** Iterator ****************

template <typename T>
class Array_iter {
public:
    static Array_iter *make(Array<T> *array);
    static void dealloc(Array_iter<T> *self);
    static PyObject *next(Array_iter<T> *self);
    static PyObject *len(Array_iter<T> *self);
private:
    static PyMethodDef methods[];
    static PyTypeObject pytype;
    static const char *pyname;
    PyObject ob_base;
    size_t index;
    Array<T> *array;            // Set to 0 when iterator is exhausted.
};

template <>
const char *Array_iter<long>::pyname = "tinyarray.ndarrayiter_int";
template <>
const char *Array_iter<double>::pyname = "tinyarray.ndarrayiter_float";
template <>
const char *Array_iter<Complex>::pyname = "tinyarray.ndarrayiter_complex";

template <typename T>
Array_iter<T> *Array_iter<T>::make(Array<T> *array)
{
    int ndim;
    assert(Array<T>::check_exact((PyObject*)array));
    array->ndim_shape(&ndim, 0);
    if (ndim == 0) {
        PyErr_SetString(PyExc_TypeError, "Iteration over a 0-d array.");
        return 0;
    }
    Array_iter<T> *ret = PyObject_New(Array_iter<T>, &Array_iter<T>::pytype);
    if (ret == 0) return 0;
    ret->index = 0;
    Py_INCREF(array);
    ret->array = array;
    return ret;
}

template <typename T>
void Array_iter<T>::dealloc(Array_iter<T> *self)
{
    // We use Py_XDECREF as array is already decref'ed when the iterator gets
    // exhausted.
    Py_XDECREF(self->array);
    PyObject_Del(self);
}

template <typename T>
PyObject *Array_iter<T>::next(Array_iter<T> *self)
{
    Array<T> *array = self->array;
    if (array == 0) return 0;
    int ndim;
    size_t *shape;
    array->ndim_shape(&ndim, &shape);
    assert(ndim != 0);

    if (self->index == shape[0]) {
        // End of iteration.
        Py_DECREF(array);
        self->array = 0;
        return 0;
    }

    T *src = array->data();

    if (ndim == 1) {
        assert(size_t(self->index) < shape[0]);
        return pyobject_from_number(src[self->index++]);
    }

    assert(ndim > 1);
    size_t item_size;
    Array<T> *result = Array<T>::make(ndim - 1, shape + 1, &item_size);
    if (!result) return 0;
    src += item_size * self->index++;
    T *dest = result->data();
    for (size_t i = 0; i < item_size; ++i) dest[i] = src[i];
    return (PyObject*)result;
}

template <typename T>
PyObject *Array_iter<T>::len(Array_iter<T> *self)
{
    Py_ssize_t len = 0;
    if (self->array) {
#ifndef NDEBUG
        int ndim;
        self->array->ndim_shape(&ndim, 0);
        assert(ndim != 0);
#endif
        size_t *shape;
        self->array->ndim_shape(0, &shape);
        len = shape[0] - self->index;
    }
    return PyInt_FromSsize_t(len);
}

template <typename T>
PyMethodDef Array_iter<T>::methods[] = {
    {"__length_hint__", (PyCFunction)Array_iter<T>::len, METH_NOARGS,
     "Private method returning an estimate of len(list(it))."},
    {0, 0}                      // Sentinel
};

template <typename T>
PyTypeObject Array_iter<T>::pytype = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    pyname,                             // tp_name
    sizeof(Array_iter<T>),              // tp_basicsize
    0,                                  // tp_itemsize
    // methods
    (destructor)Array_iter<T>::dealloc, // tp_dealloc
    0,                                  // tp_print
    0,                                  // tp_getattr
    0,                                  // tp_setattr
    0,                                  // tp_compare
    0,                                  // tp_repr
    0,                                  // tp_as_number
    0,                                  // tp_as_sequence
    0,                                  // tp_as_mapping
    0,                                  // tp_hash
    0,                                  // tp_call
    0,                                  // tp_str
    PyObject_GenericGetAttr,            // tp_getattro
    0,                                  // tp_setattro
    0,                                  // tp_as_buffer
    Py_TPFLAGS_DEFAULT,                 // tp_flags
    0,                                  // tp_doc
    0,                                  // tp_traverse
    0,                                  // tp_clear
    0,                                  // tp_richcompare
    0,                                  // tp_weaklistoffset
    PyObject_SelfIter,                  // tp_iter
    (iternextfunc)Array_iter<T>::next,  // tp_iternext
    Array_iter<T>::methods              // tp_methods
};

// The following explicit instantiations are necessary for GCC 4.6 but not for
// GCC 4.7.  I don't know why.

template PyObject *repr<long>(PyObject*);
template PyObject *repr<double>(PyObject*);
template PyObject *repr<Complex>(PyObject*);

template PyObject *str<long>(PyObject*);
template PyObject *str<double>(PyObject*);
template PyObject *str<Complex>(PyObject*);

template Py_hash_t hash<long>(PyObject*);
template Py_hash_t hash<double>(PyObject*);
template Py_hash_t hash<Complex>(PyObject*);

template int getbuffer<long>(PyObject*, Py_buffer*, int);
template int getbuffer<double>(PyObject*, Py_buffer*, int);
template int getbuffer<Complex>(PyObject*, Py_buffer*, int);

template PyObject *getitem<long>(PyObject*, PyObject*);
template PyObject *getitem<double>(PyObject*, PyObject*);
template PyObject *getitem<Complex>(PyObject*, PyObject*);

template PyObject *seq_getitem<long>(PyObject*, Py_ssize_t);
template PyObject *seq_getitem<double>(PyObject*, Py_ssize_t);
template PyObject *seq_getitem<Complex>(PyObject*, Py_ssize_t);

} // Anonymous namespace

// **************** Public interface ****************

PyDoc_STRVAR(tinyarray_doc,
"Arrays of numbers for Python, optimized for small sizes\n\n\
\n\
The tinyarray module provides multi-dimensional arrays of numbers, similar to\n\
NumPy, but with the following differences:\n\
\n\
* Optimized for small sizes: Compared to NumPy, common operations on small\n\
  arrays (e.g. length 3) are up to 35 times faster, and 3 times less memory is\n\
  used to store them.\n\
\n\
* Arrays are immutable and hashable, and can be thus used as dictionary keys.\n\
\n\
* The tinyarray module provides only the functionality that is deemed essential\n\
  with small arrays.  For example, there exists a fast tinyarray.dot function,\n\
  but there is no fancy indexing or slicing.\n\
\n\
The module's interface is a basic subset of that of NumPy and hence should be\n\
familiar to many Python programmers.  All functions are simplified versions of\n\
their NumPy counterparts.\n\
\n\
For example, arrays can be created with:\n\
\n\
    tinyarray.array(arraylike, [dtype])\n\
\n\
where arraylike can be a number, a sequence (of sequences, ...) of numbers,\n\
a NumPy or tinyarray array, or another object supporting the buffer protocol.\n\
The dtype parameter is optional and can only take the values int, float, and\n\
complex.  Note that dtype is a positional argument and cannot be used as a\n\
keyword argument.  Arrays can be also created with the functions identity,\n\
zeros, and ones.\n\
\n\
Tinyarrays support iteration and indexing (currently without slicing), as well\n\
as vectorized elementwise arithmetics.  A small number of operations like dot,\n\
floor, and transpose are provided.  Printing works as well as pickling.\n\
Whenever an operation is missing from Tinyarray, NumPy can be used directly,\n\
e.g.: numpy.linalg.det(my_tinyarray).");

extern "C"
MOD_INIT_FUNC(tinyarray)
{
    // Determine storage formats.
    bool be = is_big_endian();
    if (std::numeric_limits<double>::is_iec559 &&
        sizeof(double) == 8) {
        format_by_dtype[int(DOUBLE)] = Format(FLOAT64_LE + be);
        format_by_dtype[int(COMPLEX)] = Format(COMPLEX128_LE + be);
    } else {
        format_by_dtype[int(DOUBLE)] = UNKNOWN;
        format_by_dtype[int(COMPLEX)] = UNKNOWN;
    }
    if (sizeof(long) == 8)
        format_by_dtype[int(LONG)] = Format(INT64_LE + be);
    else if (sizeof(long) == 4)
        format_by_dtype[int(LONG)] = Format(INT32_LE + be);
    else
        format_by_dtype[int(LONG)] = UNKNOWN;

    if (PyType_Ready(&Array<long>::pytype) < 0) return MOD_ERROR_VAL;
    if (PyType_Ready(&Array<double>::pytype) < 0) return MOD_ERROR_VAL;
    if (PyType_Ready(&Array<Complex>::pytype) < 0) return MOD_ERROR_VAL;

    PyObject *m;
    MOD_DEF(m, "tinyarray", functions, tinyarray_doc);

    reconstruct = PyObject_GetAttrString(m, "_reconstruct");

    Py_INCREF(&Array<long>::pytype);
    Py_INCREF(&Array<double>::pytype);
    Py_INCREF(&Array<Complex>::pytype);

    PyModule_AddObject(m, "__version__", PyString_FromString(VERSION));

    PyObject *all = PyList_New(0);
    for (const PyMethodDef *f = functions; f->ml_name; ++f) {
        if (f->ml_name[0] == '_') continue;
        PyObject *f_py = PyObject_GetAttrString(m, f->ml_name);
        PyList_Append(all, PyObject_GetAttrString(f_py, "__name__"));
        Py_DECREF(f_py);
    }
    PyModule_AddObject(m, "__all__", all);

    PyModule_AddObject(m, "ndarray_int",
                       (PyObject *)&Array<long>::pytype);
    PyModule_AddObject(m, "ndarray_float",
                       (PyObject *)&Array<double>::pytype);
    PyModule_AddObject(m, "ndarray_complex",
                       (PyObject *)&Array<Complex>::pytype);

    // export information on the sizes of different dtypes in bytes
    PyObject *dtype_size = PyDict_New();
    PyDict_SetItem(dtype_size,
                   (PyObject*)&PyInt_Type,
                   PyInt_FromSize_t(sizeof(long)));
    PyDict_SetItem(dtype_size,
                   (PyObject*)&PyFloat_Type,
                   PyInt_FromSize_t(sizeof(double)));
    PyDict_SetItem(dtype_size,
                   (PyObject*)&PyComplex_Type,
                   PyInt_FromSize_t(sizeof(Complex)));
    PyModule_AddObject(m, "dtype_size", dtype_size);

    // We never release these references but this is not a problem.  The Python
    // interpreter does the same, see try_complex_special_method in
    // complexobject.c
    int_str = PyString_InternFromString("__int__");
    if (int_str == 0) return MOD_ERROR_VAL;
    long_str = PyString_InternFromString("__long__");
    if (long_str == 0) return MOD_ERROR_VAL;
    float_str = PyString_InternFromString("__float__");
    if (float_str == 0) return MOD_ERROR_VAL;
    complex_str = PyString_InternFromString("__complex__");
    if (complex_str == 0) return MOD_ERROR_VAL;
    index_str = PyString_InternFromString("__index__");
    if (complex_str == 0) return MOD_ERROR_VAL;

    return MOD_SUCCESS_VAL(m);
}

int load_index_seq_as_long(PyObject *obj, long *out, int maxlen)
{
    assert(maxlen >= 1);
    int len;
    if (PySequence_Check(obj)) {
        // get a new reference -- don't forget to DECREF on all codepaths
        obj = PySequence_Fast(obj, "Bug in tinyarray, load_index_seq_as_long");
        if (!obj) return -1;
        Py_ssize_t long_len = PySequence_Fast_GET_SIZE(obj);
        if (long_len > maxlen) {
            PyErr_Format(PyExc_ValueError, "Sequence too long."
                         " Maximum length is %d.", maxlen);
            goto fail;
        }
        len = static_cast<int>(long_len);
        for (PyObject **p = PySequence_Fast_ITEMS(obj), **e = p + len; p < e;
             ++p, ++out) {
            PyObject *index = PyNumber_Index(*p);
            if (index == 0) goto fail;
            *out = PyInt_AsLong(index);
            Py_DECREF(index);
            if (*out == -1 && PyErr_Occurred()) goto fail;
        }
        Py_DECREF(obj);
    } else {
        len = 1;
        *out = PyInt_AsLong(obj);
        if (*out == -1 && PyErr_Occurred()) return -1;
    }
    return len;

fail:
    Py_DECREF(obj);
    return -1;
}

int load_index_seq_as_ulong(PyObject *obj, unsigned long *uout,
                            int maxlen, const char *errmsg)
{
    long *out = reinterpret_cast<long*>(uout);
    int len = load_index_seq_as_long(obj, out, maxlen);
    if (len == -1) return -1;
    for (int i = 0; i < len; ++i)
        if (out[i] < 0) {
            if (errmsg == 0)
                errmsg = "Sequence may not contain negative values.";
            PyErr_SetString(PyExc_ValueError, errmsg);
            return -1;
        }
    return len;
}

// If *dtype == NONE the simplest fitting dtype (at least dtype_min)
// will be used and written back to *dtype.  Any other value of *dtype requests
// an array of the given dtype.
PyObject *array_from_arraylike(PyObject *in, Dtype *dtype, Dtype dtype_min,
                               bool as_matrix)
{
    Dtype dtype_in = get_dtype(in), dt = *dtype;
    int ndim;
    size_t shape[max_ndim];
    PyObject *seqs[max_ndim], *result;
    if (dtype_in != NONE) {
        // `in` is already an array.
        if (dt == NONE)
            dt = Dtype(std::max(int(dtype_in), int(dtype_min)));
        if (as_matrix) {
            size_t *in_shape;
            reinterpret_cast<Array_base*>(in)->ndim_shape(&ndim, &in_shape);
            if (ndim == 2) {
                if (dt == dtype_in)
                    Py_INCREF(result = in);
                else
                    result = convert_array(dt, in, dtype_in);
            } else if (ndim < 2) {
                shape[1] = (ndim == 0) ? 1 : in_shape[0];
                shape[0] = 1;
                result = convert_array(dt, in, dtype_in, 2, shape);
            } else {
                PyErr_SetString(PyExc_ValueError,
                                "Matrix must be 2-dimensional.");
                result = 0;
            }
        } else {
            if (dt == dtype_in)
                Py_INCREF(result = in);
            else
                result = convert_array(dt, in, dtype_in);
        }

        *dtype = dt;
        return result;
    } else if(PySequence_Check(in)) {
        // `in` is not an array, but is a sequence.

        bool find_type = (dt == NONE);

        // Try if buffer interface is supported.
        Py_buffer view;
        if (examine_buffer(in, &view, find_type ? &dt : 0) == 0) {
            if (find_type && int(dt) < int(dtype_min)) dt = dtype_min;
            for (int i = 0; i < view.ndim; i++)
                shape[i] = view.shape[i];
            if (as_matrix && view.ndim != 2) {
                if (view.ndim > 2) {
                    PyErr_SetString(PyExc_ValueError,
                                    "Matrix must be 2-dimensional.");
                    return 0;
                }
                shape[1] = (view.ndim == 0) ? 1 : shape[0];
                shape[0] = 1;
            }
            result = make_and_readin_buffer_dtable[int(dt)](
                &view, (as_matrix ? 2 : view.ndim), shape);
            PyBuffer_Release(&view);

            *dtype = dt;
            return result;
        }

        if (examine_sequence(in, &ndim, shape, seqs,
                             find_type ? &dt : 0) == 0) {
            if (as_matrix && ndim != 2) {
                if (ndim > 2) {
                    for (int d = 0; d < ndim; ++d) Py_DECREF(seqs[d]);
                    PyErr_SetString(PyExc_ValueError,
                                    "Matrix must be 2-dimensional.");
                    return 0;
                }
                shape[1] = (ndim == 0) ? 1 : shape[0];
                shape[0] = 1;
            }
            if (find_type) {
                PyObject *seqs_copy[max_ndim];
                for (int d = 0; d < ndim; ++d)
                    Py_INCREF(seqs_copy[d] = seqs[d]);
                if (dt == NONE) {
                    assert(shape[(as_matrix ? 2 : ndim) - 1] == 0);
                    dt = default_dtype;
                }
                if (int(dt) < int(dtype_min)) dt = dtype_min;
                while (true) {
                    result = readin_seqs_into_new_dtable[int(dt)](
                        seqs, ndim, (as_matrix ? 2 : ndim), shape, true);
                    if (result) break;
                    dt = Dtype(int(dt) + 1);
                    if (dt == NONE) {
                        result = 0;
                        break;
                    }
                    PyErr_Clear();
                    for (int d = 0; d < ndim; ++d)
                        Py_INCREF(seqs[d] = seqs_copy[d]);
                }
                for (int d = 0; d < ndim; ++d) Py_DECREF(seqs_copy[d]);
            } else {
                // A specific dtype has been requested.
                result = readin_seqs_into_new_dtable[int(dt)](
                    seqs, ndim, (as_matrix ? 2 : ndim), shape, false);
            }

            *dtype = dt;
            return result;
        }
    } else {
        // `in` is a scalar, or an invalid input.

        dtype_in = dtype_of_scalar(in);
        bool find_type = (dt == NONE);

        if (dtype_in == NONE) {
            PyErr_SetString(PyExc_TypeError,
                            "Expecting an arraylike object or a scalar.");
            return 0;
        }

        if (find_type) {
            dt = Dtype(std::max(int(dtype_in), int(dtype_min)));
            result = readin_scalar_into_new_dtable[int(dt)](
                in, true, (as_matrix ? 2 : 0));
        } else {
            result = readin_scalar_into_new_dtable[int(dt)](
                in, false, (as_matrix ? 2 : 0));
        }

        *dtype = dt;
        return result;
    }

    return 0;
}

int coerce_to_arrays(PyObject **a_, PyObject **b_, Dtype *coerced_dtype)
{
    PyObject *a = *a_, *b = *b_;

    // Make sure a and b are tinyarrays.
    Dtype dtype_a = NONE, dtype_b = NONE, dtype;
    a = array_from_arraylike(a, &dtype_a);
    if (!a) return -1;
    b = array_from_arraylike(b, &dtype_b, dtype_a);
    if (!b) {
        Py_DECREF(a);
        return -1;
    }

    // Promote to a common dtype.
    dtype = Dtype(std::max(int(dtype_a), int(dtype_b)));
    if (dtype_a != dtype) {
        PyObject *temp = convert_array(dtype, a, dtype_a);
        if (temp == 0) goto fail;
        Py_DECREF(a);
        a = temp;
    } else if (dtype_b != dtype) {
        PyObject *temp = convert_array(dtype, b, dtype_b);
        if (temp == 0) goto fail;
        Py_DECREF(b);
        b = temp;
    }

    // Success
    *a_ = a; *b_ = b; *coerced_dtype = dtype;
    return 0;

fail:
    Py_DECREF(a);
    Py_DECREF(b);
    return -1;
}

template <typename T>
PyObject *transpose(PyObject *in_, PyObject *)
{
    assert(Array<T>::check_exact(in_)); Array<T> *in = (Array<T>*)in_;

    int ndim;
    ptrdiff_t hops[max_ndim];
    size_t *shape_in, shape_out[max_ndim], stride = 1;
    in->ndim_shape(&ndim, &shape_in);
    if (ndim == 0) {
        Py_INCREF(in_);
        return in_;
    }
    for (int id = ndim - 1, od = 0; id >= 0; --id, ++od) {
        size_t ext = shape_in[id];
        shape_out[od] = ext;
        hops[od] = stride;
        stride *= ext;
    }
    for (int d = 1; d < ndim; ++d) hops[d - 1] -= hops[d] * shape_out[d];
    Array<T> *out = Array<T>::make(ndim, shape_out);
    if (!out) return 0;
    T *src = in->data(), *dest = out->data();

    int d = 0;
    size_t i[max_ndim];
    --ndim;
    i[0] = shape_out[0];
    while (true) {
        if (i[d]) {
            --i[d];
            if (d == ndim) {
                *dest++ = *src;
                src += hops[d];
            } else {
                ++d;
                i[d] = shape_out[d];
            }
        } else {
            if (d == 0) return (PyObject*)out;
            --d;
            src += hops[d];
        }
    }
}

template <typename T>
PyObject *conjugate(PyObject *in_, PyObject *)
{
  return apply_unary_ufunc<Conjugate<T> >(in_);
}

template <typename T>
PyObject *size_of(PyObject *in_, PyObject *)
{
    assert(Array<T>::check_exact(in_));
    return PyInt_FromSsize_t(((const Array<T>*) in_)->object_size());
}

template <typename T>
Array<T> *Array<T>::make(int ndim, size_t size)
{
    Py_ssize_t ob_size = size;
    assert(ndim != 0 || size == 1);
    if (ndim > 1)
        ob_size += (ndim * sizeof(size_t) + sizeof(T) - 1) / sizeof(T);
    Array *result = PyObject_NewVar(Array<T>, &Array<T>::pytype, ob_size);
    if (!result) return 0;
    if (ndim > 1)
        result->ob_base.ob_size = -ndim;
    else if (ndim == 0)
        result->ob_base.ob_size = -1;
    return result;
}

template <typename T>
Array<T> *Array<T>::make(int ndim, const size_t *shape, size_t *sizep)
{
    // Check shape and calculate size, the total number of elements.
    size_t size = 1;
    // `reserve' allows to detect overflow.
    size_t reserve = PY_SSIZE_T_MAX;
    for (int d = 0; d < ndim; ++d) {
        size_t elem = shape[d];
        if (elem > reserve) {
            PyErr_SetString(PyExc_ValueError, "Array would be too big.");
            return 0;
        }
        size *= elem;
        if (elem) reserve /= elem;
    }

    Array *result = Array<T>::make(ndim, size);
    if (!result) return 0;
    size_t *result_shape;
    result->ndim_shape(0, &result_shape);
    for (int d = 0; d < ndim; ++d) result_shape[d] = shape[d];

    if (sizep) *sizep = size;
    return result;
}


template <typename T>
PyObject *reduce(PyObject *self_, PyObject*)
{
    assert(Array<T>::check_exact(self_)); Array<T> *self = (Array<T>*)self_;
    PyObject *result = PyTuple_New(2);
    if (!result) return 0;

    int ndim;
    size_t *shape;
    self->ndim_shape(&ndim, &shape);
    size_t size_in_bytes = calc_size(ndim, shape) * sizeof(T);

    PyObject *pyshape = PyTuple_New(ndim);
    for (int i=0; i < ndim; ++i)
        PyTuple_SET_ITEM(pyshape, i, PyInt_FromSize_t(shape[i]));
    PyObject *format = PyInt_FromLong(format_by_dtype[int(get_dtype(self_))]);
    PyObject *data = PyBytes_FromStringAndSize((char*)self->data(),
                                                size_in_bytes);

    // PyTuple_SET_ITEM steals references, so we need to INCREF
    Py_INCREF(reconstruct);
    PyTuple_SET_ITEM(result, 0, reconstruct);
    // Py_BuildValue does not steal references, so we need to DECREF
    PyTuple_SET_ITEM(result, 1, Py_BuildValue("(OOO)", pyshape, format, data));
    Py_DECREF(pyshape);
    Py_DECREF(format);
    Py_DECREF(data);

    return result;
}

// **************** Type object ****************

template <>
const char *Array<long>::pyname = "tinyarray.ndarray_int";
template <>
const char *Array<double>::pyname = "tinyarray.ndarray_float";
template <>
const char *Array<Complex>::pyname = "tinyarray.ndarray_complex";

template <typename T>
PySequenceMethods Array<T>::as_sequence = {
    (lenfunc)len,                // sq_length
    0,                           // sq_concat
    0,                           // sq_repeat
    seq_getitem<T> // sq_item
};

template <typename T>
PyMappingMethods Array<T>::as_mapping = {
    (lenfunc)len,               // mp_length
    getitem<T>      // mp_subscript
};

#if PY_MAJOR_VERSION >= 3
template <typename T>
PyBufferProcs Array<T>::as_buffer = {
    getbuffer<T>,  // bf_getbuffer
    0,             // bf_releasebuffer
};
#else
template <typename T>
PyBufferProcs Array<T>::as_buffer = {
    // We only support the new buffer protocol.
    0,                          // bf_getreadbuffer
    0,                          // bf_getwritebuffer
    0,                          // bf_getsegcount
    0,                          // bf_getcharbuffer
    getbuffer<T> // bf_getbuffer
};
#endif

template <typename T>
PyMethodDef Array<T>::methods[] = {
    {"transpose", (PyCFunction)transpose<T>, METH_NOARGS},
    {"conjugate", (PyCFunction)conjugate<T>, METH_NOARGS},
    {"__sizeof__", (PyCFunction)size_of<T>, METH_NOARGS},
    {"__reduce__", (PyCFunction)reduce<T>, METH_NOARGS},
    {0, 0}                      // Sentinel
};

#if PY_MAJOR_VERSION >= 3  // don't need flags for buffers or checking types
    static unsigned long _tp_flags = Py_TPFLAGS_DEFAULT;
#else
    static long _tp_flags = Py_TPFLAGS_DEFAULT |
        Py_TPFLAGS_HAVE_NEWBUFFER |
        Py_TPFLAGS_CHECKTYPES;
#endif

template <typename T>
PyTypeObject Array<T>::pytype = {
    PyVarObject_HEAD_INIT(&PyType_Type, 0)
    pyname,
    sizeof(Array_base),             // tp_basicsize
    sizeof(T),                      // tp_itemsize
    (destructor)PyObject_Del,       // tp_dealloc
    0,                              // tp_print
    0,                              // tp_getattr
    0,                              // tp_setattr
    0,                              // tp_compare  (tp_reserved in Python 3.x)
    repr<T>,                        // tp_repr
    &as_number,                     // tp_as_number
    &as_sequence,                   // tp_as_sequence
    &as_mapping,                    // tp_as_mapping
    hash<T>,                        // tp_hash
    0,                              // tp_call
    str<T>,                         // tp_str
    PyObject_GenericGetAttr,        // tp_getattro
    0,                              // tp_setattro
    &as_buffer,                     // tp_as_buffer
    _tp_flags,                      // tp_flags
    0,                              // tp_doc
    0,                              // tp_traverse
    0,                              // tp_clear
    (richcmpfunc)richcompare,       // tp_richcompare
    0,                              // tp_weaklistoffset
    (getiterfunc)Array_iter<T>::make, // tp_iter
    0,                              // tp_iternext
    methods,                        // tp_methods
    0,                              // tp_members
    getset,                         // tp_getset
    0,                              // tp_base
    0,                              // tp_dict
    0,                              // tp_descr_get
    0,                              // tp_descr_set
    0,                              // tp_dictoffset
    0,                              // tp_init
    0,                              // tp_alloc
    0,                              // tp_new
    PyObject_Del                    // tp_free
};

// **************** Explicit instantiations ****************
template class Array<long>;
template class Array<double>;
template class Array<Complex>;

template PyObject *transpose<long>(PyObject*, PyObject*);
template PyObject *transpose<double>(PyObject*, PyObject*);
template PyObject *transpose<Complex>(PyObject*, PyObject*);

template PyObject *conjugate<long>(PyObject*, PyObject*);
template PyObject *conjugate<double>(PyObject*, PyObject*);
template PyObject *conjugate<Complex>(PyObject*, PyObject*);

template PyObject *size_of<long>(PyObject*, PyObject*);
template PyObject *size_of<double>(PyObject*, PyObject*);
template PyObject *size_of<Complex>(PyObject*, PyObject*);

template PyObject *reduce<long>(PyObject*, PyObject*);
template PyObject *reduce<double>(PyObject*, PyObject*);
template PyObject *reduce<Complex>(PyObject*, PyObject*);
