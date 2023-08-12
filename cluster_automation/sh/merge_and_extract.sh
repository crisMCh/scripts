#!/bin/bash
set -euf -o pipefail

# Usage: ./merge_and_extract.sh root-file-name output-folder

source /beegfs1/software/geant4/gate/gate9.2_install/bin/gate_env.sh

WORK_DIR=/beegfs2/scratch/${USER}/JOB/$2
rm -r $WORK_DIR/$2/output/Singles*

# Merge files
cd $WORK_DIR/output 
hadd -f $1.root $11.root $12.root $13.root $14.root $15.root $16.root $17.root $18.root $19.root $110.root 

# Extract singles
cd ..
sbatch convert.sh $1 $2 Singles_S1
sbatch convert.sh $1 $2 Singles_S2

exit 0
