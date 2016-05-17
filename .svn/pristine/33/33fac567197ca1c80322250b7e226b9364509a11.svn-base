
def copy(src, dst) : 
    # copies the 'src' file to 'dst' destination (may be directory or file name)
    import shutil
    shutil.copy(str(src), str(dst))
    pass

def copyDir(src, dst) : 
    # copies the 'src' directory to 'dst' destination 
    import shutil
    shutil.copytree(str(src), str(dst))
    pass

def rmDir(path) :
    # removes the specified directory
    import shutil
    shutil.rmtree(str(path), True)
    pass

def mkDir(path) :
    # creates the directory. If specified directory already exista it will be removed
    from pathlib import Path
    path = Path(path)
    if path.exists() : rmDir(path) 
    path.mkdir()
    pass

def copySln(sln, dst) :
    # copies the specified 'sln' solution to 'dst' destination folder
    import os
    from pathlib import Path 
    if not Path(sln).exists() :
        sln = Path(os.getenv("_3DV"), sln)
        if not sln.exists() : return False
        pass

    comandline = r'perl {0}\tools\copy_sln.pl "{1}" "{2}"'.format(os.getenv("_3DV"), str(sln), str(dst))
    os.system(comandline)
    return True
    pass

def listTestFiles(xml) : 
    # generates list of files for tests specified in the 'xml' file
    import re
    from pathlib import Path
    xml = str(xml)
    dir = Path(xml).parents[0]

    # extract test files from the 'xml' list
    tests = []
    with open(xml, "r") as files:
        for line in files:
            match = re.search(r'name="(.*?)"', line)
            if(match) : tests.append(match.group(1))
            pass
        pass

    # collect test files and accompany ones (exam, model)
    list = []
    for test in tests :
        list.append(test)
        exam = Path(dir, test + ".exam")
        if exam.exists() : list.append(exam.name)
        test = Path(dir, test)
        with open(str(test), "r") as file:
            for line in file : 
                match = re.search(r'model="(.*?)"', line)
                if(match) : 
                    list.append(match.group(1))
                    break
                pass
            pass
        pass
    return list


def copyTests(list, dst) :
    # For list of test specified in the 'list' file copies test files, exams, models etc from the folder of lication 'list' file to 'dst' folder
    import util
    from pathlib import Path
    dst = Path(dst)
    src = Path(list).parents[0]
    
    if not dst.exists() : dst.mkdir(parents = True)
    for file in listTestFiles(list) :
        util.copy(Path(src, file), dst)
        pass
    pass

def copyDirs(src, dst, list) :
    # copies folders by list of masks specified in 'list' from 'src' folder to 'dst' one
    from pathlib import Path
    dst = Path(dst)
    src = Path(src)
    if not dst.exists() : dst.mkdir()
    for mask in list : 
        for dir in src.glob(mask) : 
            copyDir(dir, dst.joinpath(dir.name))
            pass
        pass
    pass

def copyList(src, dst, list) :
    # copies list of files/directories from 'src' folder to 'dst' one
    from pathlib import Path
    if not Path(dst).exists() : Path(dst).mkdir()
    for item in list :
        pathSrc = Path(src, item)
        if not pathSrc.exists() : return False
        pathDst = Path(dst, item)
        if pathSrc.is_dir() :
            copyDir(pathSrc, pathDst)
        else :
            if not pathDst.parents[0].exists() : pathDst.parents[0].mkdir(parents=True)
            copy(pathSrc, pathDst)
        pass
    return True

def genHelp(dir, dst) :
    # TODO: generate help
    pass

def copySdkReverseImp(dst, sourcecode, sourcebinaries, testfolder) :

    from pathlib import Path 
    import util

    # source files to be copied
    source = {"include": ["in_assert.h", "in_base.h", "in_ref.h"], 
           "kit" : ["kt_assert.h", "kt_std.h"], 
           "3DTransVidiaReverse" : ["tvr_reverse.h", "tvr_std.h"],
           "math_ex" : ["mx_reverse_def.h"] 
           }

    # binaries to be copied
    bin = ["3DTransVidiaKit.exe", "3DTransVidiaReverse.dll", "ikernel.dll", "ikernel_imp.dll", "kit.dll", "math.dll", "math_ap.dll", "math_ex.dll", "math_kit.dll", "modeler.dll", "modeler_ex.dll", "tr_config.dll", "tr_step.dll", "tr_xml.dll", "translator.dll", "util_lm.dll", "win_kit.dll", "win_kit_mfc.dll", "opt_ui.dll", "glew32.dll"] 

    # libraries (TODO: why for SDK reverse are copied ikernel.lib and ikernel_imp.lib but not kit.lib and math_ex.lib according to .h-files)
    libs = ["3DTransVidiaReverse.lib", "ikernel.lib", "ikernel_imp.lib" ]

    # resources from 'Data' folder
    resources = ["3dv_string.csv", "3dv_string_repair.csv", "3dv_strings_translator.csv"] 

    # configurations
    configurations = ["x64", "win32"]

    # make path to destination folder
    dst = Path(dst)
    if not dst.is_absolute() : dst = os.getcwd() / dst

    # TODO: create destination folder by SVN latest revision number
    #if dst.exists() : util.rmDir(dst)
    if dst.exists() : return False
    dst.mkdir()

    # create folders for binary and libraries 
    for cfg in configurations :
        Path(dst, "bin", cfg).mkdir(parents = True)
        Path(dst, "lib", cfg).mkdir(parents = True)

    # copy source code and corresponting .lib files
    dirCodeDst = Path(dst, "include")
    dirCodeDst.mkdir(parents = True)
    for folder in source :
        dirCodeSrc = Path(sourcecode, folder)
        # copy source code files
        for mask in source[folder] :
            for file in list(dirCodeSrc.glob(mask)) :
                util.copy(file, dirCodeDst)
                pass
        # copy corresponding .lib file
        '''
        for cfg in configurations :
            lib = Path(sourcebinaries, "bin/{0}_gold/{1}.lib".format(cfg, folder))
            if lib.exists() : util.copy(lib, Path(dst, "lib", cfg))
            pass
            '''

    for lib in libs:
        for cfg in configurations :
            file = Path(sourcebinaries, "bin/{0}_gold/{1}".format(cfg, lib))
            if file.exists() : util.copy(file, Path(dst, "lib", cfg))
            pass

    # copy binaries and resource data
    for cfg in configurations :
        dirBinDst = Path(dst, r"bin", cfg)
        dirBinSrc = Path(sourcebinaries, "bin/{0}_gold".format(cfg))
        for file in bin :
            fSrc = Path(dirBinSrc, file)
            if fSrc.exists() : util.copy(fSrc, dirBinDst)
            pass
        dirDataSrc = Path(sourcecode, "data")
        for res in resources :
            fSrc = Path(dirDataSrc, res)
            if fSrc.exists() : util.copy(fSrc, dirBinDst)
            pass

    # copy redist 
    util.copyDirs(Path(sourcecode, "install"), Path(dst, "prerequisites"), ["dotNetFx", "vcredist_*_2012"])

    # copy sample tests
    util.copyDir(Path(testfolder, r"reverse\sdk_reverse"), Path(dst, "sample"))

    # copy readme
    util.copy(Path(sourcecode, r"doc\sdk_reverse\3DTransVidiaReverseSDK_Installation.pdf"), dst.joinpath("3DTransVidiaReverseSDK_Installation.pdf"))
    pass

def copySdkBinImp(dst, sourcecode, sourcebinaries, toolkitX64, toolkitX86, testfolder) :
    # copies ths binary SDK from 'src' folder to 'dst' one. 
    # 'bGenHelp' turns on/off generating of help file
    # 'bCopyToolkit' turns on/off copying of toolkit packages
    from pathlib import Path 
    import os
    import util
    import vs

    # source files to be copied
    source = {"include": ["*.h"], 
           r"include\GL" : ["*.h"], 
           "ikernel" : [ "*.h"], 
           "ikernel_imp" : ["ii_kernel.h", "ii_std.h"],
           "math_ex" : ["mx_exam.h", "mx_std.h"], 
           "math_kit": ["mk_const.h"],
           "kit": ["kt_assert.h", "kt_exam.h", "kt_io.h", "kt_job.h", "kt_log.h", "kt_out.h", "kt_std.h", "kt_str.h", "kt_timing.h", "kt_xin.h", "kt_xml.h", "kt_xml_cfg.h", "kt_xml_elem.h", "kt_xml_out.h", "kt_test.h", "kt_xml_dom.h", "kt_tools.h", "kt_set.h"] 
           }

    # binaries to be copied
    bin = ["sample.exe", "cmd_sw.dll", "quality.dll", "win.dll", "graphics.dll", "converter.exe", "ikernel.dll", "ikernel_imp.dll", "kit.dll", "math.dll", "math_ap.dll", "math_ex.dll", "math_kit.dll", "modeler.dll", "modeler_ex.dll", "net_server_util.dll", "opt_ui.dll", "registration.exe", "toolkit.dll", "toolkit_reg.dll", "tr_asc.dll", "tr_config.dll", "tr_mesh.dll", "tr_vrml.dll", "tr_step.dll", "tr_xml.dll", "translator.dll", "util_lm.dll", "win_kit.dll", "win_kit_mfc.dll", "glew32.dll", "vi.exe", "xmlvalidate.exe", "xsl_transform.exe"] 

    # resources from 'Data' folder
    resources = ["3dv_string.csv", "3dv_string_repair.csv", "3dv_strings_translator.csv", "basic_opt.xml", "healing_env_compare.xml", "healing_env_default.xml", "sa_string.csv", "toolkit.xml", "transformRead.xsl", "transformReadLog.xsl", "transformRepairStat.xsl"] 

    # configurations
    configurations = ["x64", "win32"]

    # make path to destination folder
    dst = Path(dst)
    if not dst.is_absolute() : dst = os.getcwd() / dst

    # TODO: create destination folder by SVN latest revision number
    #if dst.exists() : util.rmDir(dst)
    if dst.exists() : return False
    dst.mkdir()

    # create folders for binary and libraries 
    for cfg in configurations :
        Path(dst, "bin", cfg).mkdir(parents = True)
        Path(dst, "lib", cfg).mkdir(parents = True)

    # copy source code and corresponting .lib files
    dirCodeDst = Path(dst, "include")
    dirCodeDst.mkdir(parents = True)
    for folder in source :
        dirCodeSrc = Path(sourcecode, folder)
        # copy source code files
        for mask in source[folder] :
            for file in list(dirCodeSrc.glob(mask)) :
                util.copy(file, dirCodeDst)
                pass
        # copy corresponding .lib file
        for cfg in configurations :
            lib = Path(sourcebinaries, "bin/{0}_gold/{1}.lib".format(cfg, folder))
            if lib.exists() : util.copy(lib, Path(dst, "lib", cfg))
            pass

    # copy binaries and resource data
    for cfg in configurations :
        dirBinDst = Path(dst, r"bin", cfg)
        dirBinSrc = Path(sourcebinaries, "bin/{0}_gold".format(cfg))
        for file in bin :
            fSrc = Path(dirBinSrc, file)
            if fSrc.exists() : util.copy(fSrc, dirBinDst)
            pass
        dirDataSrc = Path(sourcecode, "data")
        for res in resources :
            fSrc = Path(dirDataSrc, res)
            if fSrc.exists() : util.copy(fSrc, dirBinDst)
            pass

    # copy sample project
    vs.copySln(Path(sourcecode, "sample\sample_sdk.sln"), Path(dst, "sample"))

    # copy test files for sample
    util.copyTests(Path(testfolder, r"sample\_all_sdk.xml"), Path(dst, r"sample\test"))
    util.copy(Path(testfolder, r"sample\_all_sdk.xml"), Path(dst, r"sample\test"))
    util.copy(Path(testfolder, r"sample\options.xml"), Path(dst, r"sample\test"))
    util.copy(Path(testfolder, r"sample\options_auxgeom.xml"), Path(dst, r"sample\test"))

    # copy redist 
    util.copyDirs(Path(sourcecode, "install"), Path(dst, "install"), ["fonts", "dotNetFx", "vcredist_*"])
    
    # copy readme
    util.copy(Path(sourcecode, "install/doc/3DTransVidiaSDK_Installation.pdf"), dst.joinpath("3DTransVidiaSDK_Installation.pdf"))
    
    # copy help file
    # TODO:if bGenHelp : util.genHelp(dst, Path(dst, "sdk_api_bin.chm"))
    util.copy(Path(sourcecode, "doc/doxygen/sdk_api_bin.chm"), dst)

    # copy qif schema
    util.copyDirs(Path(sourcecode, "data/qif2"), Path(dst, "xsd"), ["QIFApplications", "QIFLibrary"])

    # copy toolkit
    dirDstToolkit = Path(dst, "toolkit")
    dirDstToolkit.mkdir()
    util.copy(toolkitX64, dirDstToolkit)
    util.copy(toolkitX86, dirDstToolkit)
    pass

def getSlnTmpCompiled(sln) :
    import vs
    import util
    import tempfile
    from pathlib import Path

    # temporary directory
    tempDir = tempfile.TemporaryDirectory("." + Path(sln).name + ".compiled")

    # copy solution
    if not vs.copySln(sln, tempDir.name) : 
        print("Can't copy the .sln to a temporary folder")
        return None

    sldDst = Path(tempDir.name, Path(sln).name)
    if not vs.compileSln(sldDst, "Gold", "win32") : 
        print("Can't compile the .sln Gold win32")
        return None
    if not vs.compileSln(sldDst, "Gold", "x64") : 
        print("Can't compile the .sln Gold x64")
        return None

    return tempDir

def copySdkBin(dst, sourcecode, toolkitX64, toolkitX86, testfolder, compile) :
    from pathlib import Path
    import tempfile
    import vs
    import util

    print("Copy binary SDK")
    print("  Destination folder: ", dst)
    print("  Source code folder: ", sourcecode)
    print("  x64 toolkit location: ", toolkitX64)
    print("  x86 toolkit location: ", toolkitX86)
    print("  Test folder location: ", testfolder)
    print("  Compilation mode : ", compile)

    try:
        # compile solution in the temporary directory or use binaries from the 'sourcecode' folder
        tempDir = None
        slnKernel = str(Path(sourcecode, "kernel_lic.sln"))
        if compile == 0 :
            # compile in source folder
            if not vs.compileSln(slnKernel, "Gold", "win32") : 
                print("Can't compile the kernel_lic.sln Gold win32")
                return False
            if not vs.compileSln(slnKernel, "Gold", "x64") : 
                print("Can't compile the kernel_lic.sln Gold x64")
                return False
            sourcebinaries = sourcecode
        elif compile == 1 :
            # compile in a temporary folder
            tempDir = getSlnTmpCompiled(slnKernel)
            if not tempDir :
                print("Can't copy or compile the kernel_lic.sln solution")
                return False
            sourcebinaries = tempDir.name
        else :
            # don't compile, use existing binaries from source folder
            sourcebinaries = sourcecode
            pass

        # copy sdk
        copySdkBinImp(dst, sourcecode, sourcebinaries, toolkitX64, toolkitX86, testfolder)
        pass

    except Exception as err :
        print("Can't copy SDK. An exception occured: \n {0}".format(err))
        return False
    return True

def copySdkReverse(dst, sourcecode, testfolder, compile) :
    from pathlib import Path
    import tempfile
    import vs
    import util

    print("Copy reverse SDK")
    print("  Destination folder: ", dst)
    print("  Source code folder: ", sourcecode)
    print("  Test folder location: ", testfolder)
    print("  Compilation mode : ", compile)

    try:
        # compile solution in the temporary directory or use binaries from the 'sourcecode' folder
        tempDir = None
        slnKernel = str(Path(sourcecode, "all_projects.sln"))
        if compile == 0 :
            # compile in source folder
            if not vs.compileSln(slnKernel, "Gold", "win32") : 
                print("Can't compile the all_projects.sln Gold win32")
                return False
            if not vs.compileSln(slnKernel, "Gold", "x64") : 
                print("Can't compile the all_projects.sln Gold x64")
                return False
            sourcebinaries = sourcecode
        elif compile == 1 :
            # compile in a temporary folder
            tempDir = getSlnTmpCompiled(slnKernel)
            if not tempDir :
                print("Can't copy or compile the all_projects.sln solution")
                return False
            sourcebinaries = tempDir.name
        else :
            # don't compile, use existing binaries from source folder
            sourcebinaries = sourcecode
            pass

        # copy sdk
        copySdkReverseImp(dst, sourcecode, sourcebinaries, testfolder)
        pass

    except Exception as err :
        print("Can't copy SDK. An exception occured: \n {0}".format(err))
        return False
    return True

def copyToolkitBin(src, dst) :

    from pathlib import Path
    import re
    import util

    # detect version of Visual Studio and target platform (x86/x64)
    exchange = Path(src, "exchange")
    if  not exchange.exists() : return False
    for d in exchange.glob("NT_*") :
        match = re.search(r"NT_VC(?P<vs>\d\d)_(?P<platform>\d\d).*", d.name)
        if not match : continue
        vs = match.group("vs")
        platform = match.group("platform")
        break
    else :
        return False

    dlls = "NT_VC{0}_{1}_DLL".format(vs, platform)
    
    #exchange\NT_VC11_64_DLL\code\bin\
    #exchange\redist\
    #interop\NT_VC11_64_DLL\
    #interop\NT_VC11_64_DLL_install.log
    #interop\packageid.txt
    #parasolid\
    list = [ r"exchange\{0}\code\bin".format(dlls), r"exchange\redist", r"interop\{0}".format(dlls), r"interop\{0}_install.log".format(dlls)
            , r"interop\packageid.txt", r"parasolid" ]
    print("List of files and directories to be copied:")
    for item in list : print ("\t", item)

    return util.copyList(src, dst, list)
