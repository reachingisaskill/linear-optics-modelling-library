
import sys
import numpy
import operator

import elements
import beamline
import parameters


beta_x = 9.441
beta_y = 23.264
alpha_x = -0.081
alpha_y = -0.115
dx = 0.39155
dpx = -0.5183

end_beta_x = 5.9033
end_beta_y = 8.3784
end_alpha_x = 1.4900
end_alpha_y = -1.2411



rm_d_1 = elements.Drift("d_1", name="d_1")
rm_d_2 = elements.Drift("d_2", name="d_2")
rm_d_3 = elements.Drift("d_3", name="d_3")
rm_d_4 = elements.Drift("d_4", name="d_4")
rm_d_5 = elements.Drift("d_5", name="d_5")
rm_d_6 = elements.Drift("d_6", name="d_6")
rm_d_7 = elements.Drift("d_7", name="d_7")

rm_dp   = elements.SectorDipole( 2.0, 1.0e9, name="dp_0" )
rm_dp_1 = elements.SectorDipole( 2.5, 8, name="dp_1")
rm_dp_2 = elements.SectorDipole( 1.5, 30, name="dp_2")
rm_dp_3 = elements.SectorDipole( 2.5, -10, name="dp_3")
rm_dp_4 = elements.SectorDipole( 2.5, -16.66666667, name="dp_4")

rm_q_1  = elements.Quadrupole( "rm_q_len", "rm_q1_k1", name="rm_q1" )
rm_q_2  = elements.Quadrupole( "rm_q_len", "rm_q2_k1", name="rm_q2" )
rm_q_3  = elements.Quadrupole( "rm_q_len", "rm_q3_k1", name="rm_q3" )
rm_q_4  = elements.Quadrupole( "rm_q_len", "rm_q4_k1", name="rm_q4" )
rm_q_5  = elements.Quadrupole( "rm_q_len", "rm_q5_k1", name="rm_q5" )
rm_q_6  = elements.Quadrupole( "rm_q_len", "rm_q6_k1", name="rm_q6" )
rm_q_7  = elements.Quadrupole( "rm_q_len", "rm_q7_k1", name="rm_q7" )
rm_q_8  = elements.Quadrupole( "rm_q_len", "rm_q8_k1", name="rm_q8" )
rm_q_9  = elements.Quadrupole( "rm_q_len", "rm_q9_k1", name="rm_q9" )
rm_q_10 = elements.Quadrupole( "rm_q_len", "rm_q10_k1", name="rm_q10" )
rm_q_11 = elements.Quadrupole( "rm_q_len", "rm_q11_k1", name="rm_q11" )
rm_q_12 = elements.Quadrupole( "rm_q_len", "rm_q11_k1", name="rm_q12" )
rm_ql_1 = elements.Quadrupole( "rm_q_fat_len", "rm_q1_k1", name="rm_ql1" )
rm_ql_2 = elements.Quadrupole( "rm_q_fat_len", "rm_q2_k1", name="rm_ql2" )
rm_ql_3 = elements.Quadrupole( "rm_q_fat_len", "rm_q3_k1", name="rm_ql3" )

rm_disp_close = elements.Marker("disp_open")
aperture_change = elements.Marker("aperture_change")




params = parameters.ParameterTable()
params.set_parameter("rm_q_len", 1.0, lower=0.5, upper=2.0)
params.set_parameter("rm_q_fat_len", 2.0, disabled=True)

params.set_parameter("d_1", 0.2, lower=0.3, upper=0.3)
params.set_parameter("d_2", 2.0, lower=0.3, upper=3.0)
params.set_parameter("d_3", 1.0, lower=0.3, upper=2.0)
params.set_parameter("d_4", 0.3, lower=0.3, upper=1.0)
params.set_parameter("d_5", 3.0, lower=0.3, upper=4.0)
params.set_parameter("d_6", 1.0, lower=0.3, upper=2.0)
params.set_parameter("d_7", 3.0, lower=0.3, upper=4.0)

params.set_parameter("rm_q1_k1",  -0.25, lower=-1.0, upper=1.0)
params.set_parameter("rm_q2_k1",   0.40, lower=-1.0, upper=1.0)
params.set_parameter("rm_q3_k1",  -0.27, lower=-1.0, upper=1.0)
params.set_parameter("rm_q4_k1",   0.33, lower=-1.0, upper=1.0)
params.set_parameter("rm_q5_k1",  -0.30, lower=-1.0, upper=1.0)
params.set_parameter("rm_q6_k1",   0.20, lower=-1.0, upper=1.0)
#params.set_parameter("rm_q7_k1",   0.10, lower=-1.0, upper=1.0)
#params.set_parameter("rm_q8_k1",  -0.10, lower=-1.0, upper=1.0)
#params.set_parameter("rm_q9_k1",   0.10, lower=-1.0, upper=1.0)
#params.set_parameter("rm_q10_k1", -0.11, lower=-1.0, upper=1.0)
#params.set_parameter("rm_q11_k1",  0.26, lower=-1.0, upper=1.0)
#params.set_parameter("rm_q12_k1", -0.18, lower=-1.0, upper=1.0)



constraints = parameters.ConstraintTable()
constraints.set_constraint("#END#", "beta_x", operator.eq, end_beta_x )
constraints.set_constraint("#END#", "beta_y", operator.eq, end_beta_y )
constraints.set_constraint("#END#", "alpha_x", operator.eq, end_alpha_x )
constraints.set_constraint("#END#", "alpha_y", operator.eq, end_alpha_y )
constraints.set_constraint("#END#", "dx", operator.eq, 0.0 )
constraints.set_constraint("#END#", "dpx", operator.eq, 0.0 )
constraints.set_constraint("disp_open", "dx", operator.eq, 0.0 )
constraints.set_constraint("disp_open", "dpx", operator.eq, 0.0 )

constraints.set_constraint( ("#START#", "#END#"), "beta_x", operator.lt, 20.0 )
constraints.set_constraint( ("#START#", "#END#"), "beta_y", operator.lt, 20.0 )
constraints.set_constraint( ("#START#", "#END#"), "dx", operator.gt, -1.0 )
constraints.set_constraint( ("aperture_change", "#END#"), "beta_x", operator.lt, 15.0 )
constraints.set_constraint( ("aperture_change", "#END#"), "beta_x", operator.lt, 15.0 )



element_list = [rm_d_1, rm_q_1, rm_d_6, rm_q_2, rm_d_3, rm_dp_1, aperture_change, rm_d_3, rm_q_3, rm_d_3, rm_q_4, rm_d_5, rm_q_5, rm_d_4, rm_q_6, rm_d_4, rm_dp_3, rm_disp_close, rm_d_2 ]



bl = beamline.Beamline(element_list, parameter_table=params, constraint_table=constraints)

bl.set_input( beta_x=beta_x, beta_y=beta_y, alpha_x=alpha_x, alpha_y=alpha_y, dx=dx, dpx=dpx)


print bl
print
print
bl.propagate()
print bl.print_optics()
print
print "Penalty =", bl.get_penalty()
print bl.get_parameter_table()
print
beamline.plot_optics(bl.get_optics(), smooth=5)
print
print "EVOLVING"
print
bl, result = parameters.Evolve(bl)
print "EVOLUTION FINISHED"
print
print result
print
print "OPTIMIZING"
print
bl, result = parameters.Optimize(bl)
print result
print
print bl.print_optics()
print
print "Penalty =", bl.get_penalty()
print bl.get_parameter_table()
print
beamline.plot_optics(bl.get_optics(), smooth=5)



