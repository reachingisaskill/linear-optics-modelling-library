
import numpy
import operator

import elements
import beamline
import parameters

element_list = []

K1 = 0.1222
#K1 = 0.244381

element_list.append(elements.Quadrupole("q_len", "q_k", name="Q1"))
element_list.append(elements.Drift("drift_len"))
element_list.append(elements.Quadrupole("q_len", "q_k", focussing=False, name="Q2"))
element_list.append(elements.Quadrupole("q_len", "q_k", focussing=False, name="Q2"))
element_list.append(elements.Drift("drift_len"))
element_list.append(elements.Quadrupole("q_len", "q_k", name="Q1"))

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

params = parameters.ParameterTable()

params.set_parameter("q_len", 0.5)
params.set_parameter("q_k", K1)
params.set_parameter("drift_len", 2.0)

constraints = parameters.ConstraintTable()
constraints.set_constraint("Q1", "beta_x", operator.eq, beta_x )


bl.set_parameter_table(params)
bl.set_constraint_table(constraints)

end = bl.propagate_beam( beam_x, beam_y )
matrices = bl.calculate_matrix()

optics = bl.get_optics()


print beam_x
print beam_y
print
print matrices[0]
print matrices[1]
print
print end[0]
print end[1]
print
print optics
print
print bl.get_penalty()
print
print

params.set_parameter("q_k", 2.0*K1)
bl.set_parameter_table(params)
end = bl.propagate_beam( beam_x, beam_y )
matrices = bl.calculate_matrix()

print beam_x
print beam_y
print
print matrices[0]
print matrices[1]
print
print end[0]
print end[1]
print optics
print
print bl.get_penalty()

