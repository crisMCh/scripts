
#!/bin/bash

#
# Author: Cristina Chifu, 13.5.2022
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
# the outputs of your Gate simulation will be present both in the Source directory (until the next simulation when they are replaced) and in the target folder where
# Always look at the outputs in the target folder!
# to merge the root outputs run: 
#				hadd desired-output-name.root *.root   


######################################################################################################################################################################

# Define where the working directory is, based on the username of the user submitting
DATE=$(date +"%d-%m-%Y")
#WORKINGDIRECTORY=$(pwd)/$1
# where the output goes/ aka target folder
WORK_DIR=/beegfs2/scratch/${USER}/JOB/$1
#where the script is called from
SOURCE_DIR=$(pwd)
echo "Source directory = $SOURCE_DIR"


#preparing the environment. Note: .Gate folder should be in home/user - check with: echo $GC_DOT_GATE_DIR
source /beegfs1/software/geant4/gate/gate9.2_install/bin/gate_env.sh
export GC_DOT_GATE_DIR=$WORK_DIR

#remove old output files
cd $SOURCE_DIR 
rm -r output/*

# Create the scratch folder if it does not exist:
if [[ ! -e $WORK_DIR ]]; then
    chmod a+w $(pwd)
    mkdir -p "$WORK_DIR/$DATE"
    echo "Work directory= $WORK_DIR"

    rsync -avh --progress $SOURCE_DIR/* $WORK_DIR
    #rsync -avh --progress $SOURCE_DIR/output $WORK_DIR

else
    echo "##WARNING: File already exists, do you want to overwrite it? (y or n)"
    read answer
    if [[ "$answer" = "y" || "$answer" = "Y" ]] ;then
        echo "Overwriting files and running new job..."
        chmod a+w $(pwd)
        rm -rfv $WORK_DIR
        mkdir -p "$WORK_DIR/$DATE"
        echo "Work directory= $WORK_DIR"
        rsync -avh --progress $SOURCE_DIR/* $WORK_DIR
        
    else
        echo "Exiting...nothing to do"
        exit 0
    fi
fi

# CALL THE JOB SPLITTER
cd $WORK_DIR
echo $(pwd)
gjs -n 10 -c slurm -slurmscript run_Slurm mac/$2.mac 
./mac/$2.submit

# I could not make gjm work properly. Run hadd manually instead
#gjm  $GC_DOT_GATE_DIR/.Gate/$2/$2.split

#copy output to current target
#cd $SOURCE_DIR 
#cp -r output/ $WORK_DIR
#rsync -avh --progress $SOURCE_DIR/output $WORK_DIR
echo "Done with running run_Simulation script!"
