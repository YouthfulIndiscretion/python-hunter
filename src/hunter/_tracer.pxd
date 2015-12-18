cimport cython
from cpython cimport pystate

cdef extern from "frameobject.h":
    ctypedef class types.CodeType[object PyCodeObject]:
        cdef object co_filename
        cdef int co_firstlineno

    ctypedef class types.FrameType[object PyFrameObject]:
        cdef CodeType f_code
        cdef object f_back
        cdef object f_trace
        cdef object f_globals
        cdef object f_locals
        cdef int f_lineno

    void PyEval_SetTrace(pystate.Py_tracefunc func, object obj)

@cython.final
cdef class Tracer:
    cdef:
        public object _handler
        public object _previous_tracer
