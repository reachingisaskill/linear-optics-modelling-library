
import numpy
from scipy.interpolate import make_interp_spline, BSpline

import matplotlib
from matplotlib import pyplot
from matplotlib import patches
from matplotlib import gridspec


def interpolate( data, col ) :
  return make_interp_spline(data[:,0], data[:,col], k=3)  # type: BSpline
  


def plot_optics(optics, smooth=None) :
  data = []
  types = []

  fig = pyplot.figure()
  gs = gridspec.GridSpec(2, 1, height_ratios=[1, 5], hspace=0.0)
  ax = pyplot.subplot(gs[1])
  ax.ticklabel_format(style="plain", useOffset=False)

  pyplot.xlabel('S [m]')

  prev = -1.0
  for _, d in optics :
    if (d['position']-prev) < 1.0e-6 :
      continue
    prev = d['position']
    data.append( [ d['position'], d['length'], d['beta_x'], d['beta_y'], d['alpha_x'], d['alpha_y'], d['dx'], d['dy'], d['dpx'], d['dpy']  ] )
    types.append( d['type'] )

  data = numpy.array(data)

  max_beta = max( [ max(numpy.fabs(data[:,2])), max(numpy.fabs(data[:,3])) ] )
  max_d = max( [ max(data[:,6]), max(data[:,7]) ] )
  min_d = min( [ min(data[:,6]), min(data[:,7]) ] )

  ax.axis([0.0, float(data[-1,0]), 0.0, 1.1*max_beta])
  pyplot.ylabel('Beta [m]')

  if smooth is not None :
    xnew = numpy.linspace(0.0, float(data[-1,0]), smooth*len(data)) 
    beta_x = interpolate( data, 2 )
    beta_y = interpolate( data, 3 )
    dx = interpolate( data, 6 )
    dy = interpolate( data, 7 )

    ax.plot(xnew, beta_x(xnew), 'black')
    ax.plot(xnew, beta_y(xnew), 'blue')
    tax = ax.twinx()
    tax.axis([0.0, float(data[-1,0]), 1.1*min_d, 1.1*max_d])
    pyplot.ylabel('Dispersion [m]')
    tax.plot(xnew, dx(xnew), 'green')
    tax.plot(xnew, dy(xnew), 'red')

  else :
    ax.plot(data[:,0], data[:,2], 'black')
    ax.plot(data[:,0], data[:,3], 'blue')
    tax = ax.twinx()
    tax.axis([0.0, float(data[-1,0]), 1.05*min_d, 1.05*max_d])
    pyplot.ylabel('Dispersion [m]')
    tax.plot(data[:,0], data[:,6], 'green')
    tax.plot(data[:,0], data[:,7], 'red')



  ax = pyplot.subplot(gs[0])
  ax.ticklabel_format(style="plain", useOffset=False)
  ax.axis([0.0, float(data[-1,0]), -1.0, 1.0])
  ax.get_xaxis().set_visible(False)
  ax.get_yaxis().set_visible(False)

  pyplot.xlabel('S [m]')

  start_z = 0.0
  end_z = 0.0
  for t, row in zip(types, data) :
    end_z = row[0]
    if t == "quadrupole" :
      draw_quadrupole( ax, float(start_z), float(end_z) )
    elif t == "sbend" :
      draw_dipole( ax, float(start_z), float(end_z) )
    start_z = end_z

  pyplot.show()


def draw_dipole(ax, start_z, end_z) :
  width = end_z - start_z
  x_pos = start_z
  y_pos = 0.0 - 0.75
  height = 1.5
  ax.add_patch(patches.Rectangle((x_pos, y_pos), width, height, 0.0, alpha=0.6, edgecolor=None, color='b'))


def draw_quadrupole(ax, start_z, end_z) :
  width = end_z - start_z
  x_pos = start_z
  y_pos = 0.0 - 0.5
  height = 1.0
  ax.add_patch(patches.Rectangle((x_pos, y_pos), width, height, 0.0, alpha=0.6, color='r'))


