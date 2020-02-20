
import numpy

import elements
import beamline

element_list = []

K1 = 0.1222
#K1 = 0.244381

element_list.append(elements.Quadrupole(0.5, K1))
element_list.append(elements.Drift(2.0))
element_list.append(elements.Quadrupole(0.5, -K1))
element_list.append(elements.Quadrupole(0.5, -K1))
element_list.append(elements.Drift(2.0))
element_list.append(elements.Quadrupole(0.5, K1))

#p = 10.0E9
p = 7.0E9
bl = beamline.Beamline(element_list)

beta_x = 12.74364
beta_y = 6.75453
alpha_x = 0.0
alpha_y = 0.0
gamma_x = 1.0/beta_x
gamma_y = 1.0/beta_y


beam_x = numpy.array( [ [ beta_x, alpha_x, 0.0 ] ,\
                        [ alpha_x, gamma_x, 0.0 ] ,\
                        [ 0.0, 0.0, 0.0 ] ] )
beam_y = numpy.array( [ [ beta_y, alpha_y, 0.0 ] ,\
                        [ alpha_y, gamma_y, 0.0 ] ,\
                        [ 0.0, 0.0, 0.0 ] ] )


end = bl.propagate_beam( beam_x, beam_y )

print beam_x
print beam_y
print
print bl.get_matrix_x()
print bl.get_matrix_y()
print
print end[0]
print end[1]


