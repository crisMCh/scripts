from os import path
import sys

#take first argument as file name
inputfile = sys.argv[1]
#inputfile = "Singles3.txt"
target_extension = 'dat'

(basename, _) = path.splitext(inputfile)
outputfile = basename + '.' + target_extension
print("Your file is at: {}".format(outputfile))


with open(inputfile)as f:
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

            