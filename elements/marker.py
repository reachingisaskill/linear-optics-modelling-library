
from _base import Element_base

import numpy

class Marker(Element_base) :
  def __init__(self, name) :
    Element_base.__init__(self, name, "marker")
    self._set_matrix(numpy.array( [ [ 1.0, 0.0, 0.0 ], [ 0.0, 1.0, 0.0 ], [ 0.0, 0.0, 1.0 ] ] ))
    self._set_rotated_matrix(numpy.array( [ [ 1.0, 0.0, 0.0 ], [ 0.0, 1.0, 0.0 ], [ 0.0, 0.0, 1.0 ] ] ))


  def get_length(self) :
    return 0.0


  def rotate(self) :
    pass


  def load_params(self, param_table) :
    pass



