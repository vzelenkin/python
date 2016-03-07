
def merge(base, mine, bSkipEquals) :
    from pathlib import Path
    base = Path(base)
    mine = Path(mine)

    if base.is_file() and mine.is_file() :
        mergeFiles(str(base), str(mine), bSkipEquals)
        return

    if not base.is_dir() or not mine.is_dir() :
        print("\t mine and base should be both filea or directories")
        return

    # search for files with the same name
    files_b = set(str(f.relative_to(base)) for f in list(base.rglob("*")) if f.is_file())
    files_m = set(str(f.relative_to(mine)) for f in list(mine.rglob("*")) if f.is_file())
    files = files_b.intersection(files_m)

    for file in files :
        mergeFiles(str(base.joinpath(file)), str(mine.joinpath(file)), True)
        pass
pass

def mergeFiles(base, mine, bSkipEquals) :
    """ Calls the tortoise merge utility for two specified files. The base file is 'base' (fixed), mine - if 'mine' (to be modified). """
    import os
    import filecmp
    from pathlib import Path 
    print("Merge files using TortoiseMerge:\n\t Base: {0}\n\t Mine: {1}".format(base, mine))
    if bSkipEquals and filecmp.cmp(base, mine) : 
        print("\t Files are equal") 
        return
    comandline = "TortoiseMerge.exe /base:\"{0}\" /mine:\"{1}\"".format(base, mine)
    os.system(comandline);


def mergeFilesD(dir) :
    """ Calls the tortoise merge utility for each pair of the exam/result files in the specified directory. """ 
    from pathlib import Path 

    # search for all pairs result/exam files
    count = 0
    mergeList = []
    for result in list(Path(dir).glob("*.result")) : 
        exam = result.with_suffix(".exam")
        if exam.exists() : 
            mergeList.append((str(result), str(exam)))
            count += 1
    
    # do merging
    i = 0
    print("Merge the directory \"{0}\": {1} exams found.".format(dir, count))
    for pair in mergeList :
        i += 1
        print("{0} from {1}".format(i, count))
        mergeFiles(pair[0], pair[1], True)
    input("Merging finished. Press enter...")


def mergeFilesD2(dirMine, dirTheirs, extMine, extTheirs) :
    """ Calls the tortoise merge utility for each of files in two specified folders by extention. """ 
    from pathlib import Path

    # search for all pairs of files by mask
    count = 0
    mergeList = []
    mask = "*." + extMine
    suffixTheirs = "." + extTheirs
    for mine in list(Path(dirMine).glob(mask)) :
        theirs = Path(dirTheirs) / mine.name
        theirs = theirs.with_suffix(suffixTheirs)
        if theirs.exists() : 
            mergeList.append((str(theirs), str(mine)))
            count += 1

    # do merging
    i = 0
    print("Merge the directories \"{0}\" and \"{1}\": {2} exams found.".format(dirMine, dirTheirs, count))
    for pair in mergeList :
        i += 1
        print("{0} from {1}".format(i, count))
        mergeFiles(pair[0], pair[1], True)
    input("Merging finished. Press enter...")

def mergeFilesL(list) :   
    """ Calls the tortoise merge utility for two files which are specified in the file 'list'. """ 
    import sys
    from pathlib import Path 

    #open list with files
    file = open(list, 'r');
    arg0 = file.readline().strip();
    if Path(arg0).is_dir() : 
        mergeFilesD(arg0)
    else :
        arg1 = file.readline().strip()
        mergeFiles(arg1, arg0, False)
        pass
    return

class Info :
    def __init__(self, path) :
        from subprocess import Popen, PIPE
        import xml.etree.ElementTree as ET

        cmd = r"svn info {0} --xml".format(path)
        stdout = Popen(cmd, stdout=PIPE).stdout
        xml = stdout.read()
        root = ET.fromstring(xml)
        entry = root.find("entry")
        self.__revision = entry.attrib.get("revision")
        self.__url = entry.find("url").text
        self.__relative_url = entry.find("relative-url").text
        self.__repository_root = entry.find("repository/root").text
        self.__repository_uuid = entry.find("repository/uuid").text
        self.__commit_revision = entry.find(r"commit").attrib.get("revision")
        self.__commit_author = entry.find(r"commit/author").text
        self.__commit_date = entry.find(r"commit/date").text
        pass

    @property 
    def revision(self) :
        return self.__revision

    @property 
    def url(self) :
        return self.__url

    @property 
    def relative_url(self) :
        return self.__relative_url

    @property 
    def repository_root(self) :
        return self.__repository_root

    @property 
    def repository_uuid(self) :
        return self.__repository_uuid

    @property 
    def commit_revision(self) :
        return self.__commit_revision

    @property 
    def commit_author(self) :
        return self.__commit_author

    @property 
    def commit_date(self) :
        return self.__commit_date
    pass


#mergeFilesD2(r"c:\projects\Test\convert_to_pdpmi", r"t:\cadviewer\log\2014_09\2014_09_12_21_00\2014_09_12_21_00_convert_to_pdpmi\exam", "result", "exam")