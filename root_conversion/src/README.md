# Usage
-> use this script after the conversion from root to txt (on the text document with * characters) \
-> run the script from terminal with the text file (and path if necessary) as an argument\
  Example run: \
               *$ python3 conv.py Singles.txt*  \
               *$ python3 /Documents/root/Singles.txt*\
               \
-> the script will return a document with the same name as the input but with the extension .dat and the formatting required\
-> the output will be in the same path as the input file 
  
# Behavior  
The script: 
 - removes the first 3 lines and the last line of text ( *, headers, *)
 - removes all * in the input document
 - replaces all NULL values with 0
 - saves the output in a .dat file 

NOTE: the script can be used both with Linux and Windows
