''' usage: python3 root2dat.py full_path_to_root_file desired_tree_2_extract
    original code and more scripts found at https://github.com/crisMCh/scripts
'''

import os
import sys
import ROOT # type: ignore

INPUTFILE = sys.argv[1]
DESIRED_TREE = sys.argv[2]    # e.g. "Singles"


# --- save the output at the same path as input file. Change if desired!
outputpath = os.path.dirname(INPUTFILE) + "/"
outputfile = outputpath + DESIRED_TREE + ".dat"

intermadiaryfile = outputfile + ".int"

root_data = ROOT.TFile.Open(INPUTFILE, "READ")
tree = root_data.Get(DESIRED_TREE)

# tree.SetScanField(0); #SetScanField(maxrows)-default 50; 0 -> show all raws of the tree;
tree.GetPlayer().SetScanRedirect(True)
tree.GetPlayer().SetScanFileName(intermadiaryfile)
tree.Scan("*")


with open(intermadiaryfile) as f:
    lines = f.readlines()
    num_lines = len(lines)
    with open(outputfile, 'w+') as outf:
        for index, line in enumerate(lines):
            #ignore the first 3 lines and the last one 
            if index > 2 and index < num_lines-1:
                line = line.replace("*","")
                line = line.replace("NULL","0")
                #print(line)
                outf.write(line)

os.remove(intermadiaryfile)
print(f"Intermediary file {intermadiaryfile} was removed")
print(f"Your file is at {outputfile}")
