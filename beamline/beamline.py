
import scipy
import scipy.linalg
import copy
import numpy



class Beamline(object) :
  def __init__(self, element_list, parameter_table=None, constraint_table=None) :
    self.__elements = element_list

    self.__parameter_table = parameter_table
    self.__constraint_table = constraint_table
    self.__optics = None
    self.__beam_x = None
    self.__beam_y = None
    self.__end_beam_x = None
    self.__end_beam_y = None
    self.__track_x = numpy.array( [0.0, 0.0, 0.01] ).transpose()
    self.__track_y = numpy.array( [0.0, 0.0, 0.01] ).transpose()
    self.__end_track_x = None
    self.__end_track_y = None

    if self.__parameter_table is not None :
      self._load_table()


  def __repr__(self) :
    the_string = "Beamline Description Follows:"
    position = 0.0
    the_string += "\n{0:8.3f}  {1:20s}  {2:4.3f}m".format(position, "#START#", 0.0)
    for element in self.__elements :
#      the_string += "\n  " + element.get_name() + "   " + element.get_type() + "   " + str(element.get_length())
      the_string += "\n{0:8.3f}  {1:20s}  {2:4.3f}m   ({3})".format(position, element.get_name(), element.get_length(), element.get_type())
      position += element.get_length()
    the_string += "\n{0:8.3f}  {1:20s}  {2:4.3f}m".format(position, "#END#", 0.0)
    the_string += "\n"
    return the_string


  def calculate_matrix(self) :
    matrix = numpy.identity(3)
    matrix_v = numpy.identity(3)

    for element in self.__elements :
      matrix = matrix.dot( element.get_matrix() )
      matrix_v = matrix_v.dot( element.get_rotated_matrix() )

    return matrix, matrix_v

  
  def set_input(self, beta_x=1.0, beta_y=1.0, alpha_x=0.0, alpha_y=0.0, dx=0.0, dy=0.0, dpx=0.0, dpy=0.0) :
    gamma_x = (1.0+alpha_x**2)/beta_x
    gamma_y = (1.0+alpha_y**2)/beta_y
    self.__beam_x = numpy.array( [ [ beta_x, alpha_x, 0.0 ] ,\
                                   [ alpha_x, gamma_x, 0.0 ] ,\
                                   [ 0.0, 0.0, 0.0 ] ] )
    self.__beam_y = numpy.array( [ [ beta_y, alpha_y, 0.0 ] ,\
                                   [ alpha_y, gamma_y, 0.0 ] ,\
                                   [ 0.0, 0.0, 0.0 ] ] )
    self.__track_x = numpy.array( [ 0.001*dx, 0.001*dpx, 0.001 ] ).transpose()
    self.__track_y = numpy.array( [ 0.001*dy, 0.001*dpy, 0.001 ] ).transpose()
    
  
  def get_output(self) :
    if self.__end_beam_x is None or self.__end_track_x is None :
      return { "beta_x" : 0.0, "beta_y": 0.0, "alpha_x": 0.0, "alpha_y": 0.0, "dx":0.0, "dy": 0.0, "dpx":0.0 ,"dpy":0.0 }
    else :
      return { "beta_x" : self.__end_beam_x[0][0], "beta_y": self.__end_beam_y[0][0],\
               "alpha_x": -self.__end_beam_x[0][1], "alpha_y": -self.__end_beam_y[0][1],\
               "dx": self.__end_track_x[0]/self.__end_track_x[2], "dy": self.__end_track_y[0]/self.__end_track_y[2],\
               "dpx": self.__end_track_x[1]/self.__end_track_x[2], "dpy": self.__end_track_y[1]/self.__end_track_y[2] }


#  def get_output(self) :
#    return self.__end_beam_x, self.__end_beam_y


  def set_beams(self, beam_x=None, beam_y=None) :
    if beam_x is not None :
      self.__beam_x = beam_x
    if beam_y is not None :
      self.__beam_y = beam_y


  def set_tracks(self, track_x=None, track_y=None) :
    if track_x is not None :
      self.__track_x = track_x
    if track_y is not None :
      self.__track_y = track_y


  def propagate(self) :
    if (self.__beam_x is None) or (self.__beam_y is None) :
      raise ValueError("No beam specified to simulate")

    covariance_x = self.__beam_x
    covariance_y = self.__beam_y
    track_x = self.__track_x
    track_y = self.__track_y
    self.__optics = []

    position = 0.0
    self.__optics.append(("#START#", { "beta_x": covariance_x[0,0], "alpha_x" : -covariance_x[0,1], "beta_y": covariance_y[0,0], "alpha_y" : -covariance_y[0,1], \
                                       "dx" : track_x[0]/track_x[2], "dpx": track_x[1]/track_x[2], "dy" : track_y[0]/track_y[2], "dpy": track_y[1]/track_y[2], \
                                       "position" : 0.0, "length" : 0.0, "type": "marker" } ))
    for element in self.__elements :
      covariance_x = element.get_matrix().dot(covariance_x.dot(element.get_matrix().transpose()))
      covariance_y = element.get_rotated_matrix().dot(covariance_y.dot(element.get_rotated_matrix().transpose()))

      track_x = element.get_matrix().dot(track_x)
      track_y = element.get_rotated_matrix().dot(track_y)

      position += element.get_length()

      self.__optics.append(( element.get_name(), { "beta_x": covariance_x[0,0], "alpha_x" : -covariance_x[0,1], "beta_y": covariance_y[0,0], "alpha_y" : -covariance_y[0,1], \
                                                   "dx" : track_x[0]/track_x[2], "dpx": track_x[1]/track_x[2], "dy" : track_y[0]/track_y[2], "dpy": track_y[1]/track_y[2], \
                                                   "position" : position, "length" : element.get_length(), "type": element.get_type() } ))

    self.__optics.append(("#END#", { "beta_x": covariance_x[0,0], "alpha_x" : -covariance_x[0,1], "beta_y": covariance_y[0,0], "alpha_y" : -covariance_y[0,1], \
                                     "dx" : track_x[0]/track_x[2], "dpx": track_x[1]/track_x[2], "dy" : track_y[0]/track_y[2], "dpy": track_y[1]/track_y[2], \
                                     "position" : position, "length" : 0.0, "type": "marker" } ))

    self.__end_beam_x = covariance_x
    self.__end_beam_y = covariance_y
    self.__end_track_x = track_x
    self.__end_track_y = track_y



  def propagate_beam(self, covariance_x, covariance_y) :
    if covariance_x.shape != (3,3) :
      raise ValueError( "Covariance x matrix must be 3x3 numpy array." )
    if covariance_y.shape != (3,3) :
      raise ValueError( "Covariance y matrix must be 3x3 numpy array." )

    self.__optics = []

    self.__optics.append(("#START#", { "beta_x": covariance_x[0,0], "alpha_x" : -covariance_x[0,1], "beta_y": covariance_y[0,0], "alpha_y" : -covariance_y[0,1] } ))
    for element in self.__elements :
      covariance_x = element.get_matrix().dot(covariance_x.dot(element.get_matrix().transpose()))
      covariance_y = element.get_rotated_matrix().dot(covariance_y.dot(element.get_rotated_matrix().transpose()))
      self.__optics.append(( element.get_name(), { "beta_x": covariance_x[0,0], "alpha_x" : -covariance_x[0,1], "beta_y": covariance_y[0,0], "alpha_y" : -covariance_y[0,1] } ))
    self.__optics.append(("#END#", { "beta_x": covariance_x[0,0], "alpha_x" : -covariance_x[0,1], "beta_y": covariance_y[0,0], "alpha_y" : -covariance_y[0,1] } ))

    self.__end_beam_x = covariance_x
    self.__end_beam_y = covariance_y
    return covariance_x, covariance_y


  def get_optics(self) :
    return self.__optics


  def print_optics(self) :
    the_string = "Optics Description Follows:"
    the_string += "\n{0:20s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {7:10s} {8:10s}".format("", "Beta x", "Beta y", "Alpha x", "Alpha y", "D x", "D y", "D px", "D py")
    for location, data in self.__optics :
      the_string += "\n{0:20s} {1: 10.4f} {2: 10.4f} {3: 10.4f} {4: 10.4f} {5: 10.4f} {6: 10.4f} {7: 10.4f} {8: 10.4f}".format(location, data["beta_x"], data["beta_y"], \
                                                    data["alpha_x"], data["alpha_y"], \
                                                    data["dx"], data["dy"], data["dpx"], data["dpy"] )


    return the_string


  def get_penalty(self) :
    if self.__constraint_table is not None :
      return self.__constraint_table.calculate_penalty(self.__optics)
    else :
      return 0.0


  def print_constraint_details(self) :
    if self.__constraint_table is not None :
      return self.__constraint_table.calculate_contributions(self.__optics)
    else :
      return None


  def propagate_track(self, vector_x, vector_y) :
    if vector_x.shape != (3,) :
      raise ValueError( "X Vector matrix must be 3x1 numpy array: "+str(vector.shape) )
    if vector_y.shape != (3,) :
      raise ValueError( "Y Vector matrix must be 3x1 numpy array: "+str(vector.shape) )

    result_x = self.__matrix[0].dot(vector_x.transpose())
    result_y = self.__matrix[1].dot(vector_y.transpose())

    return result_x, result_y

    
  def _get_parameters(self) : 
    if self.__parameter_table is None :
      raise ValueError("No parameter table provided to beamline")
    return self.__parameter_table.get_parameters_list()
      

  def _set_parameters(self, params) :
    if self.__parameter_table is None :
      raise ValueError("No parameter table provided to beamline")
    self.__parameter_table.set_parameters_list(params)
    self._load_table()


  def _get_bounds(self) :
    return self.__parameter_table.get_bounds_list()


  def _load_table(self) :
    for element in self.__elements :
      element.load_params(self.__parameter_table)


  def set_parameter_table(self, table) :
    self.__parameter_table = table
    self._load_table()


  def get_parameter_table(self) :
    return self.__parameter_table


  def set_constraint_table(self, table) :
    self.__constraint_table = table


  def get_constraint_table(self) :
    return self.__constraint_table
    
  

