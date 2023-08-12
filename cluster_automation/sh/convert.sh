#!/bin/bash
set -euf -o pipefail

# Author: Cristina Chifu, June 2023
#
# About: - This is a slurm script to run 'root2dat.py' on the cluster.
#
# Before running:
#	- a working installation of ROOT is necesary!! 	 
#
# To run: 
#  - usually the script is called in merge_and_copy.sh 
#  - for standalone calling: 
# Template ===>  sbatch convert.sh <root-file-name> <output-folder> <tree_2_extract>
# Example ===>   sbatch convert.sh hem_PET_LSO_10MBq LSO_10Mbq Singles
#
#

########################################################################################################################################################################

#SBATCH -J Convert                                  # jobname displayed by squeue
#SBATCH -N 1                                        # minimum number of nodes needed or minN-maxN, do not waste nodes (check scaling of your app), other users may need them
#SBATCH --ntasks-per-node 1                         # 16 for pure MPI-code or 16 single-core-apps
##SBATCH --ntasks=1 --cpus-per-task=16
#SBATCH --time 00:40:00                             # set walltime
#SBATCH --partition short                           # partition if not specified in the sbatch command
#SBATCH --mem 100000                                # [MB/node], please use less than 120000 MB
##SBATCH -e slurm-%j.err                            # error file

source /beegfs1/software/geant4/gate/gate9.2_install/bin/gate_env.sh

WORK_DIR=/beegfs2/scratch/${USER}/JOB/$2

srun bash -c "python3 root2dat.py $WORK_DIR/output/$1.root $3"

echo
echo ----------------------- DONE ---------------------------------
echo
echo -e "Time after job execution \t"     `date`

exit 0
