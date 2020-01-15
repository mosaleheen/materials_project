#!/bin//bin/bash
#$ -cwd
#$ -pe mpi 20
#$ -l exclusive=1
#$ -o H2O.stdout
#$ -e H2O.stderr
#$ -l m_mem_free=2G
#$ -l h_cpu=36:00:00
#$ -m beas
#$ -M jlym@udel.edu

source /etc/profile.d/valet.sh
vpkg_rollback all
export PYTHONPATH=/home/work/ccei_biomass/programs/ase/:/home/work/ccei_biomass/programs/ase/tsase:$PYTHONPATH
export PATH=/home/work/ccei_biomass/bin/:/home/work/ccei_biomass/programs/ase/tools:$PATH

vpkg_require openmpi/1.10.2-intel64-2016 python-numpy python-scipy

export VASP_COMMAND="mpiexec -n 20 /home/work/ccei_biomass/programs/vasp5.4/vasp.5.4.1/build/std/vasp"
export VASP_PP_PATH=/home/work/ccei_biomass/programs/vasp_psp/v54/


echo "$(date)  H2O.py started." >> H2O.log
echo "$(date)  H2O.py started at path $(pwd)." >> /home/work/ccei_biomass/users/jlym/farber_jobs.log
python H2O.py >& H2O.out
echo "$(date)  H2O.py completed." >> H2O.log
echo "$(date)  H2O.py completed at path $(pwd)." >> /home/work/ccei_biomass/users/jlym/farber_jobs.log
