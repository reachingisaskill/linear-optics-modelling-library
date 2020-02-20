


class ParameterTable(object) :
  def __init__(self) :
    self.__parameter_dict = {}
    self.__bounds_dict = {}
    self.__keys_list = []


  def __repr__(self) :
    the_string = "Parameter Table Follows:"
    the_string += "\n{0:20s} {1:10s} {2:10s} {3:10s}".format("Param. Name", "Value", "Lower", "Upper")
    for key in self.__keys_list :
      the_string += "\n{0:20s} {1: 10.4f} {2: 10.4f} {3: 10.4f}".format(key, self.__parameter_dict[key], self.__bounds_dict[key][0], self.__bounds_dict[key][1])
    return the_string


  def get_parameters_list(self) :
    param_list = []
    for key in self.__keys_list :
      param_list.append( self.__parameter_dict[key] )
    return param_list


  def get_bounds_list(self) :
    bounds_list = []
    for key in self.__keys_list :
      bounds_list.append( self.__bounds_dict[key] )
    return bounds_list

    
  def set_parameters_list(self, param_list) :
    for key, value in zip(self.__keys_list, param_list) :
      self.__parameter_dict[key] = value


  def set_bounds_list(self, bounds_list) :
    for key, value in zip(self.__keys_list, bounds_list) :
      self.__bounds_dict[key] = value


  def get_parameter(self, param_name) :
    return self.__parameter_dict[param_name]


  def get_parameter_bounds(self, param_name) :
    return self.__bounds_dict[param_name]


  def set_parameter(self, param_name, value, disabled=False, lower=-1.0e+10, upper=1.0e+10) :
    try :
      param_name = str(param_name)
    except :
      raise ValueError( "Parameter name must be a string" )
    try :
      value = float(value)
    except :
      raise ValueError( "Value of '"+param_name+"' must be a float : "+str(value) )

    self.__parameter_dict[param_name] = value
    self.__bounds_dict[param_name] = (lower, upper)
    
    if not disabled :
      self.__keys_list.append( param_name )


  def remove_parameter(self, param_name) :
    if param_name not in self.__parameter_dict :
      raise ValueError( "Parameter '"+param_name+"' not found" )

    num = None
    for count, element in enumerate(self.__keys_list) :
      if element == param_name :
        num = count
        break
    if num is not None :
      del self.__keys_list[num]

    del self.__parameter_dict[param_name]
    del self.__bounds_dict[param_name]


  def disable_parameter(self, param_name) :
    if param_name not in self.__parameter_dict :
      raise ValueError( "Parameter '"+param_name+"' not found" )

    num = None
    for count, element in enumerate(self.__keys_list) :
      if element == param_name :
        num = count
        break
    if num is not None :
      del self.__keys_list[num]


  def enable_parameter(self, param_name) :
    if param_name not in self.__parameter_dict :
      raise ValueError( "Parameter '"+param_name+"' not found" )

    num = None
    for count, element in enumerate(self.__keys_list) :
      if element == param_name :
        num = count
        break
    if num is None :
      self.__keys_list.append(param_name)
      


