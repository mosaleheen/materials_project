import numpy as np
from ase import Atom
from ase.build import surface, molecule
from ase.constraints import FixAtoms
from ase.calculators.vasp import Vasp
from ase.io import read, write
from ase.io.trajectory import Trajectory
from ase.optimize import LBFGS
from os.path import basename, exists
from py_box.ase import run_testRun
from py_box.ase.set_calc import print_vasp_param, calc_dict, handle_restart

testRun = False
file_name_py = basename(__file__)
file_name = file_name_py.replace('.py','')
file_traj = file_name + '.traj'
file_out = file_name + '.out'

mode = 'a'
try:
    sys = Trajectory(file_traj, 'r')[-1]
except (IOError, RuntimeError):
    print "Creating molecule from scratch"
    sys = molecule('H2')
    sys.set_cell(np.array([20, 21, 22]))
    sys.center()
    #sys *= (2, 3, 1)
else:
    print "Importing trajectory file from: %s" % file_traj

vasp_param = calc_dict['TiO2_step']
vasp_param['kpts'] = (1, 1, 1)
calc = Vasp(**vasp_param)
handle_restart(calc, sys)
print_vasp_param(calc)
sys.set_calculator(calc)

del sys.constraints
#print 'Constraints:'
#print '\tc1: Freezing bottom two layers (z < 15.)'
#c1 = FixAtoms(mask = [atom.z < 15 for atom in sys])
#sys.set_constraint(c1)
if testRun == True:
    run_testRun(sys)
else:
    geo_traj = Trajectory(file_traj, mode, sys)
    dyn = LBFGS(sys, trajectory = geo_traj)
    dyn.run(fmax = 0.05)
    print 'Completed energy optimization'
    energy = sys.get_potential_energy()
    print "Energy: %f" % energy
print "Completed %s" % file_name_py
