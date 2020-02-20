
from _base import Element_base

import numpy

class Drift(Element_base) :
  def __init__(self, length, name=None) :
    Element_base.__init__(self, name, "drift")
    if type(length) is str :
      self.__length_param = length
      self.set_length(0.0)
    else :
      self.__length_param = None
      self.set_length(length)


  def rotate(self) :
    return self

  
  def get_length(self) :
    return self.__length


  def set_length(self, length) :
    self.__length = length
    self._set_matrix(numpy.array( [ [ 1.0, length, 0.0 ], [ 0.0, 1.0, 0.0 ], [ 0.0, 0.0, 1.0 ] ] ))
    self._set_rotated_matrix(numpy.array( [ [ 1.0, length, 0.0 ], [ 0.0, 1.0, 0.0 ], [ 0.0, 0.0, 1.0 ] ] ))


  def load_params(self, param_table) :
    if self.__length_param is not None :
      self.set_length(param_table.get_parameter(self.__length_param))


