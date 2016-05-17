import pathlib
import os
import sys

# find tools and add to path
#_3dv_tools = os.getenv("_3dv_tools") + "/Python";
#sys.path.append(_3dv_tools)
#print(_3dv_tools)
#print(sys.argv)

# import svn
import svn

if len(sys.argv) == 1 : print("Incorrect script parameters")

# merge files in list specified by text file
if sys.argv[1] == "-l" and len(sys.argv) == 3 : 
    svn.mergeFilesL(sys.argv[2])
elif len(sys.argv) == 3 : 
    # merge two files or two directories
    svn.merge(sys.argv[1], sys.argv[2], False)
elif len(sys.argv) == 5 : 
    # merge two directories by mask
    svn.mergeFilesD2(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

