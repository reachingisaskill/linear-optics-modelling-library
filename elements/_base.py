
ELEMENT_COUNTER = 0


class Element_base(object) :
  def __init__(self, name, type_name) :
    global ELEMENT_COUNTER
    if name is None :
      name = "Element_"+str(ELEMENT_COUNTER)
      ELEMENT_COUNTER += 1
    self.__name = str(name)
    self.__type = str(type_name)
    self.__matrix = None
    self.__rotated_matrix = None


  def rotate(self) :
    raise NotImplementedError( "Base class function should be overiddent by derived classes." )


  def get_length(self) :
    raise NotImplementedError( "Base class function should be overiddent by derived classes." )


  def get_name(self) :
    return self.__name


  def get_type(self) :
    return self.__type

  
  def get_matrix(self) :
    return self.__matrix

  
  def get_rotated_matrix(self) :
    return self.__rotated_matrix

  
  def _set_matrix(self, matrix) :
    self.__matrix = matrix


  def _set_rotated_matrix(self, matrix) :
    self.__rotated_matrix = matrix


  def load_params(self, param_table) :
    raise NotImplementedError( "Base class function should be overidden by derived classes." )


