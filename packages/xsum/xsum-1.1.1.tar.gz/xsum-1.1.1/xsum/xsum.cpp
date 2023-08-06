//
// XSUM.cpp
//
// LGPL Version 2.1 HEADER START
//
// This library is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public
//
// License as published by the Free Software Foundation; either
// version 2.1 of the License, or (at your option) any later version.
//
// This library is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
// Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public
// License along with this library; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
// MA 02110-1301  USA
//
// LGPL Version 2.1 HEADER END
//

// This file contains the XSUM Python bindings using pybind11

//
// Copyright (c) 2020, Regents of the University of Minnesota.
// All rights reserved.
//
// Contributors:
//    Yaser Afshar
//

#include "xsum.hpp"

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

using namespace xsum;

template <typename accumulatorType>
void py_xsum_add(accumulatorType *const acc,
                 pybind11::array_t<xsum_flt> const &py_vec) {
  pybind11::buffer_info buf = py_vec.request();
  if (buf.ndim != 1) {
    throw std::runtime_error("Number of dimensions must be one!");
  }
  xsum_flt *vec = static_cast<xsum_flt *>(buf.ptr);
  xsum_length const n = static_cast<xsum_length>(buf.size);
  xsum_add<accumulatorType>(acc, vec, n);
}

template <typename accumulatorType>
void py_xsum_add_sqnorm(accumulatorType *const acc,
                        pybind11::array_t<xsum_flt> const &py_vec) {
  pybind11::buffer_info buf = py_vec.request();
  if (buf.ndim != 1) {
    throw std::runtime_error("Number of dimensions must be one!");
  }
  xsum_flt *vec = static_cast<xsum_flt *>(buf.ptr);
  xsum_length const n = static_cast<xsum_length>(buf.size);
  xsum_add_sqnorm<accumulatorType>(acc, vec, n);
}

template <typename accumulatorType>
void py_xsum_add_dot(accumulatorType *const acc,
                     pybind11::array_t<xsum_flt> const &py_vec1,
                     pybind11::array_t<xsum_flt> const &py_vec2) {
  pybind11::buffer_info buf1 = py_vec1.request();
  pybind11::buffer_info buf2 = py_vec2.request();
  if (buf1.ndim != 1 || buf2.ndim != 1) {
    throw std::runtime_error("Number of dimensions must be one!");
  }
  xsum_flt *vec1 = static_cast<xsum_flt *>(buf1.ptr);
  xsum_flt *vec2 = static_cast<xsum_flt *>(buf2.ptr);
  xsum_length const n = static_cast<xsum_length>(buf1.size);
  if (n != static_cast<xsum_length>(buf2.size)) {
    throw std::runtime_error("Input shapes must match!");
  }
  xsum_add_dot<accumulatorType>(acc, vec1, vec2, n);
}

class py_xsum_small : public xsum_small {
 public:
  /* Inherit the constructors */
  using xsum_small::xsum_small;

  void add(pybind11::array_t<xsum_flt> const &py_vec) {
    pybind11::buffer_info buf = py_vec.request();
    if (buf.ndim != 1) {
      throw std::runtime_error("Number of dimensions must be one!");
    }
    xsum_flt *vec = static_cast<xsum_flt *>(buf.ptr);
    xsum_length const n = static_cast<xsum_length>(buf.size);
    xsum_small::add(vec, n);
  }

  void add_sqnorm(pybind11::array_t<xsum_flt> const &py_vec) {
    pybind11::buffer_info buf = py_vec.request();
    if (buf.ndim != 1) {
      throw std::runtime_error("Number of dimensions must be one!");
    }
    xsum_flt *vec = static_cast<xsum_flt *>(buf.ptr);
    xsum_length const n = static_cast<xsum_length>(buf.size);
    xsum_small::add_sqnorm(vec, n);
  }

  void add_dot(pybind11::array_t<xsum_flt> const &py_vec1,
               pybind11::array_t<xsum_flt> const &py_vec2) {
    pybind11::buffer_info buf1 = py_vec1.request();
    pybind11::buffer_info buf2 = py_vec2.request();
    if (buf1.ndim != 1 || buf2.ndim != 1) {
      throw std::runtime_error("Number of dimensions must be one!");
    }
    xsum_flt *vec1 = static_cast<xsum_flt *>(buf1.ptr);
    xsum_flt *vec2 = static_cast<xsum_flt *>(buf2.ptr);
    xsum_length const n = static_cast<xsum_length>(buf1.size);
    if (n != static_cast<xsum_length>(buf2.size)) {
      throw std::runtime_error("Input shapes must match!");
    }
    xsum_small::add_dot(vec1, vec2, n);
  }
};

class py_xsum_large : public xsum_large {
 public:
  /* Inherit the constructors */
  using xsum_large::xsum_large;

  void add(pybind11::array_t<xsum_flt> const &py_vec) {
    pybind11::buffer_info buf = py_vec.request();
    if (buf.ndim != 1) {
      throw std::runtime_error("Number of dimensions must be one!");
    }
    xsum_flt *vec = static_cast<xsum_flt *>(buf.ptr);
    xsum_length const n = static_cast<xsum_length>(buf.size);
    xsum_large::add(vec, n);
  }

  void add_sqnorm(pybind11::array_t<xsum_flt> const &py_vec) {
    pybind11::buffer_info buf = py_vec.request();
    if (buf.ndim != 1) {
      throw std::runtime_error("Number of dimensions must be one!");
    }
    xsum_flt *vec = static_cast<xsum_flt *>(buf.ptr);
    xsum_length const n = static_cast<xsum_length>(buf.size);
    xsum_large::add_sqnorm(vec, n);
  }

  void add_dot(pybind11::array_t<xsum_flt> const &py_vec1,
               pybind11::array_t<xsum_flt> const &py_vec2) {
    pybind11::buffer_info buf1 = py_vec1.request();
    pybind11::buffer_info buf2 = py_vec2.request();
    if (buf1.ndim != 1 || buf2.ndim != 1) {
      throw std::runtime_error("Number of dimensions must be one!");
    }
    xsum_flt *vec1 = static_cast<xsum_flt *>(buf1.ptr);
    xsum_flt *vec2 = static_cast<xsum_flt *>(buf2.ptr);
    xsum_length const n = static_cast<xsum_length>(buf1.size);
    if (n != static_cast<xsum_length>(buf2.size)) {
      throw std::runtime_error("Input shapes must match!");
    }
    xsum_large::add_dot(vec1, vec2, n);
  }
};

PYBIND11_MODULE(xsum, m) {
  PYBIND11_NUMPY_DTYPE(xsum_small_accumulator, chunk, Inf, NaN,
                       adds_until_propagate);
  PYBIND11_NUMPY_DTYPE(xsum_large_accumulator, chunk, count, chunks_used,
                       used_used, sacc);

  pybind11::class_<xsum_small_accumulator>(m, "xsum_small_accumulator")
      .def(pybind11::init<>());

  pybind11::class_<xsum_large_accumulator>(m, "xsum_large_accumulator")
      .def(pybind11::init<>());

  m.def("xsum_init", &xsum_init<xsum_small_accumulator>,
        "Initilize the xsum_small_accumulator object");

  m.def("xsum_init", &xsum_init<xsum_large_accumulator>,
        "Initilize the xsum_large_accumulator object");

  m.def("xsum_add",
        (void (*)(xsum_small_accumulator *const, xsum_flt const)) &
            xsum_add<xsum_small_accumulator>,
        "Add a value to the superaccumulator.");

  m.def("xsum_add",
        (void (*)(xsum_large_accumulator *const, xsum_flt const)) &
            xsum_add<xsum_large_accumulator>,
        "Add a value to the superaccumulator.");

  m.def("xsum_add",
        (void (*)(xsum_small_accumulator *const,
                  pybind11::array_t<xsum_flt> const &)) &
            py_xsum_add<xsum_small_accumulator>,
        "Add a vector of values to the superaccumulator.");

  m.def("xsum_add",
        (void (*)(xsum_large_accumulator *const,
                  pybind11::array_t<xsum_flt> const &)) &
            py_xsum_add<xsum_large_accumulator>,
        "Add a vector of values to the superaccumulator.");

  m.def("xsum_add",
        (void (*)(xsum_small_accumulator *const,
                  xsum_small_accumulator const *const)) &
            xsum_add<xsum_small_accumulator>,
        "Add a small accumulator to the small superaccumulator.");

  m.def(
      "xsum_add",
      (void (*)(xsum_large_accumulator *const, xsum_large_accumulator *const)) &
          xsum_add<xsum_large_accumulator>,
      "Add a large accumulator to the large superaccumulator.");

  m.def("xsum_add",
        (void (*)(xsum_large_accumulator *const,
                  xsum_small_accumulator const *const)) &
            xsum_add<xsum_large_accumulator>,
        "Add a small accumulator to the large superaccumulator.");

  m.def("xsum_add_sqnorm", &py_xsum_add_sqnorm<xsum_small_accumulator>,
        "Add a squared norm of vector of values to the superaccumulator.");

  m.def("xsum_add_sqnorm", &py_xsum_add_sqnorm<xsum_large_accumulator>,
        "Add a squared norm of vector of values to the superaccumulator.");

  m.def("xsum_add_dot", &py_xsum_add_dot<xsum_small_accumulator>,
        "Add dot product of two vectors of values to the superaccumulator.");

  m.def("xsum_add_dot", &py_xsum_add_dot<xsum_large_accumulator>,
        "Add dot product of two vectors of values to the superaccumulator.");

  m.def("xsum_round", &xsum_round<xsum_small_accumulator>,
        "Return the results of rounding the superaccumulator.");

  m.def("xsum_round", &xsum_round<xsum_large_accumulator>,
        "Return the results of rounding the superaccumulator.");

  m.def("xsum_round_to_small", &xsum_round_to_small<xsum_large_accumulator>,
        "Return the results of rounding a large superaccumulator to a small "
        "superaccumulator.");

  m.def("print_binary", &print_binary<double>,
        "Print double precision floating point value in binary.");

  pybind11::class_<py_xsum_small>(m, "xsum_small")
      .def(pybind11::init<>())
      .def(pybind11::init<xsum_small_accumulator const &>())
      .def(pybind11::init<xsum_small_accumulator const *>())
      .def("reset", &py_xsum_small::xsum_small::reset,
           "Replace the xsum_small_accumulator object")
      .def("init", &py_xsum_small::xsum_small::init,
           "Initilize the xsum_small_accumulator object")
      .def("add",
           (void (py_xsum_small::xsum_small::*)(xsum_flt const)) &
               py_xsum_small::xsum_small::add,
           "Add a value to the superaccumulator.")
      .def("add",
           (void (py_xsum_small::xsum_small::*)(
               xsum_small_accumulator const &)) &
               py_xsum_small::xsum_small::add,
           "Add a small accumulator to the superaccumulator.")
      .def("add",
           (void (py_xsum_small::xsum_small::*)(
               xsum_small_accumulator const *)) &
               py_xsum_small::xsum_small::add,
           "Add a small accumulator to the superaccumulator.")
      .def("add",
           (void (py_xsum_small::xsum_small::*)(xsum_small const &)) &
               py_xsum_small::xsum_small::add,
           "Add a xsum_small object to the superaccumulator.")
      .def("add",
           (void (py_xsum_small::*)(pybind11::array_t<xsum_flt> const &)) &
               py_xsum_small::add,
           "Add a vector of values to the superaccumulator.")
      .def("add_sqnorm", &py_xsum_small::add_sqnorm,
           "Add a squared norm of vector of values to the superaccumulator.")
      .def("add_dot", &py_xsum_small::add_dot,
           "Add dot product of two vectors of values to the superaccumulator.")
      .def("round", &py_xsum_small::xsum_small::round,
           "Return the results of rounding the superaccumulator.")
      .def("chunks_used", &py_xsum_small::xsum_small::chunks_used,
           "Return number of chunks in use in the superaccumulator.");

  pybind11::class_<py_xsum_large>(m, "xsum_large")
      .def(pybind11::init<>())
      .def(pybind11::init<xsum_large_accumulator const &>())
      .def(pybind11::init<xsum_large_accumulator const *>())
      .def(pybind11::init<xsum_small_accumulator const &>())
      .def(pybind11::init<xsum_small_accumulator const *>())
      .def(pybind11::init<xsum_small const &>())
      .def(pybind11::init<xsum_small const *>())
      .def("reset", &py_xsum_large::xsum_large::reset,
           "Replace the xsum_large_accumulator object")
      .def("init", &py_xsum_large::xsum_large::init,
           "Initilize the xsum_large_accumulator object")
      .def("add",
           (void (py_xsum_large::xsum_large::*)(xsum_flt const)) &
               py_xsum_large::xsum_large::add,
           "Add a value to the superaccumulator.")
      .def("add",
           (void (py_xsum_large::xsum_large::*)(
               xsum_small_accumulator const *const)) &
               py_xsum_large::xsum_large::add,
           "Add a small accumulator to the superaccumulator.")
      .def(
          "add",
          (void (py_xsum_large::xsum_large::*)(xsum_large_accumulator *const)) &
              py_xsum_large::xsum_large::add,
          "Add a large accumulator to the superaccumulator.")
      .def("add",
           (void (py_xsum_large::xsum_large::*)(xsum_large &)) &
               py_xsum_large::xsum_large::add,
           "Add a large accumulator object to the superaccumulator.")
      .def("add",
           (void (py_xsum_large::*)(pybind11::array_t<xsum_flt> const &)) &
               py_xsum_large::add,
           "Add a vector of values to the superaccumulator.")
      .def("add_sqnorm", &py_xsum_large::add_sqnorm,
           "Add a squared norm of vector of values to the superaccumulator.")
      .def("add_dot", &py_xsum_large::add_dot,
           "Add dot product of two vectors of values to the superaccumulator.")
      .def("round", &py_xsum_large::xsum_large::round,
           "Return the results of rounding the superaccumulator.")
      .def("round_to_small",
           (xsum_small_accumulator(py_xsum_large::xsum_large::*)()) &
               py_xsum_large::xsum_large::round_to_small)
      .def("round_to_small",
           (xsum_small_accumulator(py_xsum_large::xsum_large::*)(
               xsum_large_accumulator *const)) &
               py_xsum_large::xsum_large::round_to_small)
      .def("chunks_used", &py_xsum_large::xsum_large::chunks_used,
           "Return number of chunks in use in the superaccumulator.");
}