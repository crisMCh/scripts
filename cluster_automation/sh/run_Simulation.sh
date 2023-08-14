#!/bin/bash
#set -euf -o pipefail

#
# Author: Cristina Chifu, 13.5.2023
#
# Before starting:
# Make sure the environment variables are set on the head-node(login node), as per the project directory.
# Use ===> source /beegfs1/software/geant4/gate/gate9.2_install/bin/gate_env.sh
#
# To run: 
# Usually run from the Gate project directory (note: you must have a mac folder in which the macro sits).
# Name-of-target-folder = chosen name where the output goes. The script will create a new folder in the WORK_DIR directory with this name
# main-mac-file-to-call = the mac file (WITHOUT the .mac extension)
# Template ===>  ./run_Simulation.sh <Name-of-target-folder> <main-mac-file-to-call>
# Example ===>  ./run_Simulation.sh myTest main

# Outputs:
# The outputs of your Gate simulation will be present in the target folder.
# to merge the root outputs run: 
#				hadd desired-output-name.root *.root   


######################################################################################################################################################################

DATE=$(date +"%d-%m-%Y")

# Where the output goes aka target folder
WORK_DIR=/beegfs2/scratch/${USER}/JOB/$1
# Where the script is called from
SOURCE_DIR=/beegfs2/scratch/${USER}/tmp/hemispheric_PET
echo "Source directory = $SOURCE_DIR"

# Preparing the environment. Note: .Gate folder should be in home/user - check with: echo $GC_DOT_GATE_DIR
source /beegfs1/software/geant4/gate/gate9.2_install/bin/gate_env.sh
export GC_DOT_GATE_DIR=$WORK_DIR

# Remove old output files
cd $SOURCE_DIR 
rm -r output/*

# Create the scratch folder if it does not exist:
if [[ ! -e $WORK_DIR ]]; then
    chmod a+w $(pwd)
    mkdir -p "$WORK_DIR/$DATE"
    echo "Work directory= $WORK_DIR"
    rsync -avh --progress $SOURCE_DIR/* $WORK_DIR
else
    echo "Overwriting files and running new job..."
    chmod a+w $(pwd)
    rm -rfv $WORK_DIR
    mkdir -p "$WORK_DIR/$DATE"
    echo "Work directory= $WORK_DIR"
    rsync -avh --progress $SOURCE_DIR/* $WORK_DIR
fi

# CALL THE JOB SPLITTER
cd $WORK_DIR
echo $(pwd)
gjs -n 10 -c slurm -slurmscript run_Slurm mac/$2.mac 
./mac/$2.submit

exit 0
