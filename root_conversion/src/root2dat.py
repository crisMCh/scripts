import os
import sys
import ROOT

#take first argument as file name
inputfile = sys.argv[1]
# inputfile = "/mnt/windows/Uwintu/work/scripts/root_conversion/test_data/test.root"
desiredTree = "Singles"

# --- save the output at the same path as input file. Change if desired!
outputpath = os.path.dirname(inputfile) + "/"
outputfile= outputpath + desiredTree +".dat"

intermadiaryfile = outputfile + ".int"


root_data = ROOT.TFile.Open(inputfile, "READ")
tree  = root_data.Get(desiredTree)

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
print("Intermediary file {} was removed".format(intermadiaryfile))
print("Your file is at {}".format(outputfile))



# leaves = tree.GetListOfLeaves()

# treeEntries = tree.GetEntries()

# entry_list = []

# for i in range(0,leaves.GetEntries()) :
#     leaf = leaves.At(i)
#     print(leaf)
#     name = leaf.GetName()
#     entry_list.append(name)

# for i in range(0,leaves.GetEntries()) :
#     leaf = leaves.At(i)
#     name = leaf.GetName()
#     #print("Leaf name: {}".format(name))
#     for entryNum in range(0,treeEntries): 
#         if entryNum < 2:
#             tree.GetEntry(entryNum)
#             entry_list.append(getattr(tree,name))
        
# with open(outputfile, 'w+') as outf:
#     outf.writelines(str(entry_list))


