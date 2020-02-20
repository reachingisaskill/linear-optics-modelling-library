
import scipy.optimize
import signal
from beamline import plot_optics

signal.signal(signal.SIGINT, signal.default_int_handler)


def _optimize_function( params, beamline ) :
  beamline._set_parameters(params)
  beamline.propagate()
  return beamline.get_penalty()


def _status_callback( x, convergence ) :
  print "\r Evolving: ", convergence,
  return False


def Optimize( beamline, method="L-BFGS-B" ) :
  starting_params = beamline._get_parameters()
  bounds = beamline._get_bounds()

  try :
    result = scipy.optimize.minimize(_optimize_function, starting_params, (beamline), method, bounds=bounds, options={"maxiter": 10000})
  except KeyboardInterrupt as ex :
    print
    print beamline.get_parameter_table()
    print
    raise ex

  beamline._set_parameters( result.x )

  return beamline, result


def Anneal( beamline ) :
  starting_params = beamline._get_parameters()
  bounds = beamline._get_bounds()

  try :
    result = scipy.optimize.dual_annealing(_optimize_function, bounds, (beamline,), maxiter=10000 )
  except KeyboardInterrupt as ex :
    print
    print beamline.get_parameter_table()
    print
    raise ex

  beamline._set_parameters( result.x )

  return beamline, result


def Evolve( beamline, progress=True, **options ) :
  starting_params = beamline._get_parameters()
  bounds = beamline._get_bounds()

  try :
    if progress :
      result = scipy.optimize.differential_evolution(_optimize_function, bounds, callback=_status_callback, args=(beamline,), **options)
    else :
      result = scipy.optimize.differential_evolution(_optimize_function, bounds, args=(beamline,), **options)
  except KeyboardInterrupt as ex :
    print
    print beamline.get_parameter_table()
    print
    raise ex
    

  beamline._set_parameters( result.x )

  return beamline, result

