
import numpy

import elements
import beamline



element_list = []

element_list.append( elements.Drift(1.0) )
#element_list.append( elements.Quadrupole(0.5, 0.1222) )
element_list.append( elements.Quadrupole(1.7, 0.1222) )
element_list.append( elements.Drift(1.0) )

bl = beamline.Beamline(element_list)

bl.set_input( beta_x=20.0, alpha_x=0.0, beta_y=10.0, alpha_y=0.0, dx=1.0, dpx=0.0 )

end = bl.propagate()

print
print bl
print
print bl.print_optics()
beamline.plot_optics(bl.get_optics(), smooth=5)
print


#
#element_list = []
#
#element_list.append( elements.Drift(1.0) )
#element_list.append( elements.SectorDipole(2.0, 10.0) )
#element_list.append( elements.Drift(1.0) )
#
#bl = beamline.Beamline(element_list)
#
#bl.set_input( beta_x=20.0, alpha_x=0.0, beta_y=10.0, alpha_y=0.0, dx=1.0, dpx=0.0 )
#
#end = bl.propagate()
#
#print
#print bl
#print
#print bl.print_optics()
#beamline.plot_optics(bl.get_optics(), smooth=5)
#print
#
#
