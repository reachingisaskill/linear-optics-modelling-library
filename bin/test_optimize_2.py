
import sys
import numpy
import operator

import elements
import beamline
import parameters


beta_x = 12.7436
beta_y = 6.7545
alpha_x = 0.0
alpha_y = 0.0
gamma_x = 1.0/beta_x
gamma_y = 1.0/beta_y



quad_capf = elements.Quadrupole( 0.5, 0.24438 )
dba_dp = elements.SectorDipole( 2.0, 20.0, name="dipole")
dba_quad_f = elements.Quadrupole( "dba_q_len", "dba_qf_k1", name="q_f")
dba_quad_d = elements.Quadrupole( "dba_q_len", "dba_qd_k1", name="q_d")
dba_mquad_f = elements.Quadrupole( "dba_mq_len", "dba_mqf_k1", name="qm_f")
dba_mquad_d = elements.Quadrupole( "dba_mq_len", "dba_mqd_k1", name="qm_d")

dba_disp_open = elements.Marker("disp_open")
dba_disp_close = elements.Marker("disp_close")

dba_d_1 = elements.Drift(2.0, name="d_1")
dba_d_2 = elements.Drift(0.3, name="d_2")
dba_d_3 = elements.Drift(2.9, name="d_3")


element_list = [ quad_capf, dba_d_1, dba_mquad_d, dba_d_1, dba_mquad_f, dba_d_1, \
dba_disp_open, dba_dp, dba_d_2, dba_quad_d, dba_d_3, dba_quad_f, dba_d_3, dba_quad_d, \
dba_d_2, dba_dp, dba_disp_close, \
dba_d_1, dba_mquad_f, dba_d_1, dba_mquad_d, dba_d_1, quad_capf ]



params = parameters.ParameterTable()
params.set_parameter("dba_q_len", 1.0, disabled=True)
params.set_parameter("dba_mq_len", 1.0, disabled=True)
params.set_parameter("dba_qf_k1", 0.1, lower=-1.0, upper=1.0)
params.set_parameter("dba_qd_k1", -0.81, lower=-1.0, upper=1.0)
params.set_parameter("dba_mqf_k1", -0.1, lower=-1.0, upper=1.0)
params.set_parameter("dba_mqd_k1", -0.1, lower=-1.0, upper=1.0)
#params.set_parameter("dba_qf_k1", 0.422, lower=-1.0, upper=1.0)
#params.set_parameter("dba_qd_k1", -0.281, lower=-1.0, upper=1.0)
#params.set_parameter("dba_mqf_k1", 0.324, lower=-1.0, upper=1.0)
#params.set_parameter("dba_mqd_k1", -0.298, lower=-1.0, upper=1.0)



constraints = parameters.ConstraintTable()
constraints.set_constraint("#END#", "beta_x", operator.eq, beta_x )
constraints.set_constraint("#END#", "beta_y", operator.eq, beta_y )
constraints.set_constraint("#END#", "alpha_x", operator.eq, alpha_x )
constraints.set_constraint("#END#", "alpha_y", operator.eq, alpha_y )
constraints.set_constraint("#disp_close", "dx", operator.eq, 0.0 )
constraints.set_constraint("#disp_close", "dpx", operator.eq, 0.0 )

constraints.set_constraint("#END#", "dx", operator.eq, 0.0 )
constraints.set_constraint("#END#", "dpx", operator.eq, 0.0 )
constraints.set_constraint("dipole", "beta_x", operator.lt, 18.0 )
constraints.set_constraint("dipole", "beta_y", operator.lt, 18.0 )
constraints.set_constraint("qm_f", "beta_x", operator.lt, 18.0 )
constraints.set_constraint("qm_f", "beta_y", operator.lt, 18.0 )
constraints.set_constraint("qm_d", "beta_x", operator.lt, 18.0 )
constraints.set_constraint("qm_d", "beta_y", operator.lt, 18.0 )
constraints.set_constraint("q_f", "beta_x", operator.lt, 14.0 )
constraints.set_constraint("q_f", "beta_y", operator.lt, 14.0 )




bl = beamline.Beamline(element_list, parameter_table=params, constraint_table=constraints)

beam_x = numpy.array( [ [ beta_x, alpha_x, 0.0 ] ,\
                        [ alpha_x, gamma_x, 0.0 ] ,\
                        [ 0.0, 0.0, 0.0 ] ] )
beam_y = numpy.array( [ [ beta_y, alpha_y, 0.0 ] ,\
                        [ alpha_y, gamma_y, 0.0 ] ,\
                        [ 0.0, 0.0, 0.0 ] ] )

bl.set_beams(beam_x, beam_y)

print bl
print
print
print beam_x
print beam_y
print
print
print

bl.propagate()
optics = bl.get_optics()
beamline.plot_optics(optics)

print bl.print_optics()

print
print bl.get_penalty()
print
print


print "OPTIMIZING"
print

#bl, result = parameters.Optimize(bl)
bl, result = parameters.Evolve(bl)
print result


bl.propagate()
optics = bl.get_optics()

print
print bl.print_optics()
print
print bl.get_penalty()
print
beamline.plot_optics(optics)





sys.exit(0)

bl.set_constraint_table(constraints)

bl, result = parameters.Optimize(bl)
#bl, result = parameters.Evolve(bl)
print result

optics = bl.get_optics()

print
print optics
print
print bl.get_penalty()
print
print
