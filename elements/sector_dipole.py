
from _base import Element_base

import numpy
import math


class SectorDipole(Element_base) :
  def __init__(self, l, r, coplanar=True, name=None) :
    Element_base.__init__(self, name, "sbend")

    if type(l) is str :
      self.__length_param = l
      self.__length = 0.0
    else :
      self.__length_param = None
      self.__length = float(l)

    if type(r) is str :
      self.__r_param = r
      self.__r = 1.0E26
    else :
      self.__r_param = None
      self.__r = float(r)

    self.__coplanar = coplanar

    self._calculate()


  def rotate(self) :
    self.__coplanar = not self.__coplanar
    self.set_param(self.__r)
    return self

  
  def get_length(self) :
    return  self.__length


  def set_length(self, lenth) :
    self.__length = length
    self._calculate()


  def get_radius(self) :
    return self.__r


  def set_radius(self, r) :
    self.__r = r
    self._calculate()

  
  def _calculate(self) :
    cos = math.cos( self.__length/self.__r )
    sin = self.__r*math.sin( self.__length/self.__r )
    cosp = -(1.0/self.__r)*math.sin( self.__length/self.__r )
    sinp = math.cos( self.__length/self.__r )

    if self.__coplanar :
      self._set_matrix(numpy.array( [ [ cos,   sin, self.__r*(1.0-cos) ], \
                                      [ cosp, sinp, sin/self.__r ], \
                                      [ 0.0,   0.0, 1.0 ] ] ) )
      self._set_rotated_matrix(numpy.array( [ [ 1.0, self.__length, 0.0 ], [ 0.0, 1.0, 0.0 ], [ 0.0, 0.0, 1.0 ] ] ))
    else :
      self._set_matrix(numpy.array( [ [ 1.0, self.__length, 0.0 ], [ 0.0, 1.0, 0.0 ], [ 0.0, 0.0, 1.0 ] ] ))
      self._set_rotated_matrix(numpy.array( [ [ cos,   sin, self.__r*(1.0-cos) ], \
                                      [ cosp, sinp, sin/self.__r ], \
                                      [ 0.0,   0.0, 1.0 ] ] ) )


  def load_params(self, param_table) :
    if self.__length_param is not None :
      self.__length = param_table.get_parameter(self.__length_param)
    if self.__r_param is not None :
      self.__r = param_table.get_parameter(self.__r_param)
    self._calculate()
    
    


