
import numpy
import operator

import elements
import beamline
import parameters

element_list = []

#K1 = 0.1222
#K1 = 0.244381
K1 = 0.0611

element_list.append(elements.Quadrupole("q_len", "q_k", name="Q1"))
element_list.append(elements.Drift("drift_len"))
element_list.append(elements.Quadrupole("q_len", "q_k", focussing=False, name="Q2"))
element_list.append(elements.Quadrupole("q_len", "q_k", focussing=False, name="Q2"))
element_list.append(elements.Drift("drift_len"))
element_list.append(elements.Quadrupole("q_len", "q_k", name="Q1"))

#p = 10.0E9
p = 7.0E9
bl = beamline.Beamline(element_list)

beta_x = 21.6502786
beta_y = 15.9057134
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

params.set_parameter("q_len", 0.5, disabled=True)
params.set_parameter("q_k", K1, lower=-1.0, upper=1.0)
params.set_parameter("drift_len", 2.0, disabled=True)

constraints = parameters.ConstraintTable()
#constraints.set_constraint("#START#", "beta_x", operator.eq, beta_x )
constraints.set_constraint("#END#", "beta_x", operator.eq, beta_x )

print beam_x
print beam_y
print
print
print

bl.set_parameter_table(params)
bl.set_constraint_table(constraints)
bl.set_beams(beam_x, beam_y)

end = bl.propagate()
optics = bl.get_optics()
end_x, end_y = bl.get_output()


print optics
print
print bl.get_penalty()
print
print end_x
print end_y
print
print
print "OPTIMIZING"
print

#print parameters.Optimize(bl)
print parameters.Evolve(bl)

optics = bl.get_optics()
end_x, end_y = bl.get_output()

print
print optics
print
print bl.get_penalty()
print
print end_x
print end_y
print
print
