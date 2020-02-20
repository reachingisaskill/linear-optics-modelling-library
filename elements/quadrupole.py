
from _base import Element_base

import numpy
import math


class Quadrupole(Element_base) :
  def __init__(self, l, k, focussing=True, name=None) :
    Element_base.__init__(self, name, "quadrupole")
    
    if type(l) is str :
      self.__length_param = l
      self.__length = 0.0
    else :
      self.__length_param = None
      self.__length = float(l)
    if type(k) is str :
      self.__k_param = k
      self.__k = 0.0
    else :
      self.__k_param = None
      self.__k = float(k)

    if focussing :
      self.__focussing = 1.0
    else :
      self.__focussing = -1.0

    self._calculate()


  def rotate(self) :
    self.__focussing *= -1
    return self


  def get_is_focussing(self) :
    if self.__focussing > 0.0 :
      return True
    else :
      return False


  def get_param(self) :
    return self.__k


  def set_param(self, k) :
    self.__k = k
    self._calculate()


  def get_length(self) :
    return self.__length

  
  def set_length(self, length) :
    self.__length = length
    self._calculate()


  def _calculate(self) :
    k = self.__k*self.__focussing
    if (math.fabs(self.__length) < 1.0e-6) or (math.fabs(self.__k) < 1.0e-6) :
      self._set_matrix( numpy.array([ [ 1.0, 0.0, 0.0 ], \
                                      [ -k, 1.0, 0.0 ], \
                                      [ 0.0, 0.0, 1.0 ] ] ) )
      self._set_rotated_matrix( numpy.array([ [ 1.0, 0.0, 0.0 ], \
                                              [ k, 1.0, 0.0 ], \
                                              [ 0.0, 0.0, 1.0 ] ] ) )
    else :
      K = math.sqrt(math.fabs(k))
      cos = math.cos( K*self.__length )
      sin = (1.0/K)*math.sin(K*self.__length)
      cosp = -K*math.sin(K*self.__length)
      sinp = math.cos(K*self.__length)

      hcos = math.cosh( K*self.__length )
      hsin = (1.0/K)*math.sinh(K*self.__length)
      hcosp = K*math.sinh(K*self.__length)
      hsinp = math.cosh(K*self.__length)

      if k > 0.0 :
        self._set_matrix(numpy.array( [ [ cos,   sin, 0.0 ], \
                                        [ cosp, sinp, 0.0 ], \
                                        [ 0.0,   0.0, 1.0 ] ] ) )

        self._set_rotated_matrix(numpy.array( [ [ hcos,   hsin, 0.0 ], \
                                        [ hcosp, hsinp, 0.0 ], \
                                        [ 0.0,     0.0, 1.0 ] ] ) )
      else :
        self._set_rotated_matrix(numpy.array( [ [ cos,   sin, 0.0 ], \
                                        [ cosp, sinp, 0.0 ], \
                                        [ 0.0,   0.0, 1.0 ] ] ) )

        self._set_matrix(numpy.array( [ [ hcos,   hsin, 0.0 ], \
                                        [ hcosp, hsinp, 0.0 ], \
                                        [ 0.0,     0.0, 1.0 ] ] ) )


  def load_params(self, param_table) :
    if self.__length_param is not None :
      self.__length = param_table.get_parameter(self.__length_param)
    if self.__k_param is not None :
      self.__k = param_table.get_parameter(self.__k_param)
    self._calculate()


