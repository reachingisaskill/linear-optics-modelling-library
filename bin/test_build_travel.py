

import numpy

import elements
import beamline


filename = "examples/L4T.txt"
p = 0.16E9

bl = beamline.build_travel(filename, p)


ref_x = numpy.array( [ 0.001, 0.0, 0.0 ] )
ref_y = numpy.array( [ 0.001, 0.0, 0.0 ] )

end = bl.propagate_track( ref_x, ref_y )

print ref_x
print ref_y
print
print bl.get_matrix_x()
print bl.get_matrix_y()
print
print end[0]
print end[1]

