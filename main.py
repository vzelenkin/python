
def genTests(dir) :
    import test
    test.genTestsDentSply(dir)
    pass

def testFiles(dir) :
    # Enumerates *.test.xml files in the specified folder. Returns Path object
    from pathlib import Path
    for file in Path(dir).glob("*.test.xml") :
        yield file
    return

def copyFailedTests(dir) :
    from pathlib import Path
    import datetime
    import shutil

    dstDir = None
    for test in testFiles(dir) :
        if not Path(str(test) + ".result").exists() : continue
        
        # create destination folder
        if not dstDir :
            dt = datetime.datetime.now()
            dstDir = Path(dir, "{0}_{1}_{2}_{3}_{4}_failed".format(dt.year, dt.month, dt.day, dt.hour, dt.minute))
            dstDir.mkdir()
            dstDir = str(dstDir)
            pass
        mask = "{0}.*".format(test.name)
        for file in Path(dir).glob(mask) :
            shutil.copy(str(file), dstDir)
    return True

def make_xyz(dir, list_mask) :
    from pathlib import Path
    import os

    for mask in list_mask :
        for file in Path(dir).rglob(mask) :
            file_xyz = file.with_suffix(".xyz")
            with open(str(file), "rt") as src : lines = src.readlines()
            with open(str(file_xyz), "wt") as dst: dst.writelines(lines[1:])
            os.remove(str(file))

    return True

def main():
    import sys
    import svn

    if len(sys.argv) < 2 :
        print("Invalid arguments");
        return False

    # merge
    if sys.argv[1] == "merge" : 
        svn.merge(sys.argv[2], sys.argv[3], True)
        return

    # generate tests
    if sys.argv[1] == "gentests" : genTests(sys.argv[2])

    # copy failed tests
    if sys.argv[1] == "copyfail" :
        if len(sys.argv) < 3 :
            print("copyfail: please specify the source folder")
            return False
        return copyFailedTests(sys.argv[2])
    
    # make *.xyz files
    if sys.argv[1] == "makexyz" :
        if len(sys.argv) < 4 :
            print("makexyz: please specify the source folder and mask for files")
            return False    
        return make_xyz(sys.argv[2], sys.argv[3:])
    pass

    print("Invalid arguments");
    return False

if __name__ == '__main__':
    
    res = False
    try:
        res = main()
        pass
    except Exception as err :
        print("Errror: \n {0}".format(err))

    str = "Success"
    if not res : str = "Failed"
    input(str)
