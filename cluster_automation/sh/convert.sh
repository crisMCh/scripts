#!/bin/bash

########################################################################################################################################################################

#SBATCH -J Convert                                 # jobname displayed by squeue
#SBATCH -N 1                                     # minimum number of nodes needed or minN-maxN, do not waste nodes (check scaling of your app), other users may need them
#SBATCH --ntasks-per-node 1                      # 16 for pure MPI-code or 16 single-core-apps
##SBATCH --ntasks=1 --cpus-per-task=16
##SBATCH --time 00:50:00                         # set 1h walltime (=maximum runtime), see sinfo
#SBATCH --time 00:40:00                          # set 24h walltime
#SBATCH --partition short                       # partition if not specified in the sbatch command
#SBATCH --mem 100000                              # [MB/node], please use less than 120000 MB
##                                                 please use all cores of a node (especially small jobs fitting to one node)
##                                                 nodes will not be shared between jobs (avoiding problems) (added 2017.06)
##SBATCH -e slurm-%j.err                           # error file

# H E R E you may set up your environment      <<<<<<<<<<  see include/my_environment.example
##. my_environment
source /beegfs1/software/geant4/gate/gate9.2_install/bin/gate_env.sh

WORK_DIR=/beegfs2/scratch/${USER}/JOB/$2

# executable 
srun bash -c "python3 root2dat.py $WORK_DIR/output/$1.root $3"

echo
echo ----------------------- DONE ---------------------------------
echo
echo -e "Time after job execution \t"     `date`

exit 0
