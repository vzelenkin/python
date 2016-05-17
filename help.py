def start(cmd) : 
    import os
    print("Starting the \"{0}\" command...".format(cmd))
    os.system(cmd)
 #   import subprocess
  #  subprocess.Popen(cmd)  

    
import sys
from pathlib import Path

# script location
folder = Path(Path(sys.argv[0]).parents[0])

# commands mapping
map = { "p3" : str(folder/"python341.chm"), "p2" : str(folder/"python278.chm") }

# start command
start(map[sys.argv[1]])

