
import math
import operator

PARAMETER_WEIGHTS = { "beta_x" : 1.0, "beta_y" : 1.0, "alpha_x" : 10.0, "alpha_y" : 10.0, "dx": 10.0, "dy": 10.0, "dpx": 100.0, "dpy": 100.0 }


def op_to_string(op) :
  if op is operator.eq :
    return "="
  if op is operator.gt :
    return ">"
  if op is operator.ge :
    return ">="
  if op is operator.lt :
    return "<"
  if op is operator.le :
    return "<="
  if op is operator.ne :
    return "!="
  else :
    return "*"



class Constraint(object) :
  def __init__(self, operator, value, weight=1.0) :
    self.__operator = operator
    self.__value = value
    self.__weight = weight


  def get_value(self) :
    return self.__value


  def get_operator(self) :
    return self.__operator


  def get_weight(self) :
    return self.__weight


  def compare(self, param) :
    if self.__operator(param, self.__value) :
      return 0.0
    else :
      return self.__weight*(param - self.__value)**2



class ConstraintTable(object) :
  def __init__(self) :
    self.__constraint_dict = {}
    self.__range_constraints = []


  def set_constraint(self, location, parameter, operator, value, weight=None) :
    try :
      parameter = str(parameter)
    except :
      raise ValueError( "Parameter name must be a string" )
    try :
      value = float(value)
    except :
      raise ValueError( "Value of '"+parameter+"' must be a float : "+str(value) )
  
    if weight is None :
      weight = PARAMETER_WEIGHTS[parameter]
    else :
      try :
        weight = float(weight)
      except :
        raise ValueError( "Weight of '"+parameter+"' must be a float : "+str(weight) )

    if type(location) is str :
      if location not in self.__constraint_dict :
        self.__constraint_dict[location] = []
      self.__constraint_dict[location].append((parameter, Constraint(operator, value, weight=weight)))

    elif type(location) is tuple :
      try : 
        loc_1, loc_2 = location
        if (type(loc_1) is not str) or (type(loc_2) is not str) :
          raise ValueError( "Location names must be strings" )
      except :
        raise ValueError( "If location range is specified, it must be a tuple of length 2" )
      
      self.__range_constraints.append( ( loc_1, loc_2, parameter, Constraint(operator, value) ) )


  def calculate_penalty(self, values) :
    penalty = 0.0

    for start, finish, param, constraint in self.__range_constraints :
      go = False
      for location, data in values :
        if location == start :
          go = True
        if go :
          delta = constraint.compare( data[param] )
          penalty += delta
        if location == finish :
          break

    for location, data in values :
      if location in self.__constraint_dict :
        for param, constraint in self.__constraint_dict[location] :
          delta = constraint.compare( data[param] )
          penalty += delta
    
    return penalty


  def calculate_contributions(self, values) :
    the_string  = "Constraint Contributions Follow:\n"
    the_string += "{0:20s} {1:8s} {2:8s} {3:8s} {4:8s} {5:8s}\n".format("Location", "Parameter", "SimValue", "Operat.", "Value", "Penalty")
    location_list = []
    constraint_data = {}
    for location, _ in values :
      constraint_data[location] = []
      location_list.append(location)

    for start, finish, param, constraint in self.__range_constraints :
      go = False
      for location, data in values :
        if location == start :
          go = True
        if go :
          delta = constraint.compare( data[param] )
          constraint_data[location].append( (param, data[param], op_to_string(constraint.get_operator()), constraint.get_value(), delta) )
        if location == finish :
          break

    for location, data in values :
      if location in self.__constraint_dict :
        for param, constraint in self.__constraint_dict[location] :
          delta = constraint.compare( data[param] )
          constraint_data[location].append( (param, data[param], op_to_string(constraint.get_operator()), constraint.get_value(), delta) )
    
    for location in location_list :
      for line in constraint_data[location] :
        the_string += "{0:20s} {1:>8s} {2: 8.3f} {3:^8s} {4: 8.3f} {5: 8.3f}\n".format( location, *line )
  
    return the_string
    


  def print_constraint(self, location) :
    if location in self.__constraint_dict :
      the_string = "Location: {0: >20s}. Constraints:\n".format(location)
      for param, constraint in self.__constraint_dict[location] :
        the_string += "{0:10s} {1} {2: 8.4f}  (x{3:f})\n".format(param, op_to_string(constraint.get_operator()), constraint.get_value(), constraint.get_weight())
    else :
      the_string = "Location: {0:20s}. No Constraints Found.\n".format(location)
    return the_string


#  def remove_constraint(self, param_name) :
#    if param_name not in self.__constraint_dict :
#      raise ValueError( "Parameter '"+param_name+"' not found" )
#
#    num = None
#    for count, element in enumerate(self.__keys_list) :
#      if element == param_name :
#        num = count
#        break
#    if num is not None :
#      del self.__keys_list[num]
#
#    del self.__constraint_dict[param_name]
#
#
#  def disable_constraint(self, param_name) :
#    if param_name not in self.__constraint_dict :
#      raise ValueError( "Parameter '"+param_name+"' not found" )
#
#    num = None
#    for count, element in enumerate(self.__keys_list) :
#      if element == param_name :
#        num = count
#        break
#    if num is not None :
#      del self.__keys_list[num]
#
#
#  def enable_constraint(self, param_name) :
#    if param_name not in self.__constraint_dict :
#      raise ValueError( "Parameter '"+param_name+"' not found" )
#
#    num = None
#    for count, element in enumerate(self.__keys_list) :
#      if element == param_name :
#        num = count
#        break
#    if num is None :
#      self.__keys_list.append(param_name)
      




