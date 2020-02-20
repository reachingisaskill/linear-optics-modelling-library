
# Linear Optics Modelling Toolkit

## Description

I wrote this little toolkit for two reasons. Firstly because I could(!) it seemed like a fun little project.
Secondly because I was asking a lot from [MadX](https://mad.web.cern.ch/mad/ "Methodical Accelerator Design") which involved awkward optimisation schemes changing variaous lengths and sizes, which MadX struggles to do natively. Hence this little project was born.

I chose to use the SciPy optmisation library (yes I could have implemented a more focussed, custom algorithm, but I could not be bothered to write all of the options and wrap them in a C-library).
The user has the option of using any of the standard optimisation algorithms or the dual-annealing algorithm.

I think the result is quite a nice pythonic toolkit for creating simulating and optimizing particle beamlines.

## Usage

I threw this together in less than a month, so there is no real documentation.
Best bet is to look at some of the tests and see how it works.
To be honest there's of lot of cleaning up that needs doing, but at the time we were pushed to meet a deadline for the design of the nuSTORM project - which I did!

### Things to note:
- Tk is used to display results in matplotlib.


## TODO

1. Fix the tests:
   - test_optimize.py
   - test_build_travel.py

2. Implement the global optimization functions based on phase advance.


If I ever have time:
- Implement a multithreaded dual-annealing algorithm, quite easy to do and could be a huge time save.

