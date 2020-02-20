
import beamline
import elements

import math
import copy
import numpy


def build_travel(filename, nominal_p) :
  element_list = []
  with open(filename, 'r') as infile : 
    for line in infile :
      parts = line.split(";")
      line = parts[0].strip()
      words = line.split()

      if line == "SENTINEL" :
        break

      elif words[0] == "5" :
        L = float(words[1])
        pole_tip_field = float(words[2])
        pole_tip_radius = float(words[3])
        if math.fabs(pole_tip_field) < 1.0E-6 :
          element_list.append( elements.Drift(L) )
          continue
        grad = 5.0*pole_tip_field/pole_tip_radius
        K1 = -1.0*3.0E8*grad/nominal_p
        print "Quad", L, K1
        element_list.append( elements.Quadrupole( L, K1 ) )

      elif words[0] == "4" :
        L = float(words[1])
        B_0 = float(words[2])
        gradient = float(words[3])
        if math.fabs(B_0) < 1.0E-6 :
          element_list.append( elements.Drift(L) )
          continue
        angle = L*3.0E8*B_0 / nominal_p
        rho = L / angle
        print "Dipole", L, rho
        element_list.append( elements.SectorDipole( L, rho ) )

      elif words[0] == "3" :
        L = float(words[1])
        print "Drift", L
        element_list.append( elements.Drift(L) )

      else :
        continue

  return beamline.Beamline(element_list)
  

