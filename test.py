
def genTestCreateFeatures(dir) :
    from pathlib import Path

    for model in list(Path(dir).glob("*.*")) :
        model = Path(model).name
        print("<test_create_features model=\"{0}\" bVisibleOnly=\"0\" bConnectedWithPmiOnly=\"0\" bOneFeatureMode=\"1\" bValidateQif=\"1\"/>\n".format(model))
        
        xml = r"{0}\{1}.test.xml".format(dir, model)
        with open(xml, "w") as file : file.write("<test_create_features model=\"{0}\" bVisibleOnly=\"0\" bConnectedWithPmiOnly=\"0\" bOneFeatureMode=\"1\" bValidateQif=\"1\"/>\n".format(model))
        pass


#genTestCreateFeatures(r"c:\projects\Test\create_features\new")

def renameTests(dir) :
    from pathlib import Path
    import re
    
    for (index, file) in enumerate(Path(dir).glob("*.test.xml")) :
        print(index, ":", file)
        pass
    return

def genTestsDentSply(dir) :
    from pathlib import Path
    import re
    import shutil

    for subdir in Path(dir).glob("*") :
        m = re.match("^(?P<index>\d\d).*", subdir.name)
        if not m : continue
        index = m.group("index")
        for file in subdir.glob("*.stl") :
            model = r"{0}.{1}".format(index, file.name)
            xml = r"{0}\{1}.test.xml".format(dir, model)
            print(model)
            shutil.copy(str(file), str(Path(dir, model)))
            with open(xml, "w") as file : file.write('''<test_reverse_auto model="{0}" eps="0.06" density="0" bAnalytic="1" bFillets="0" filletSens="0.18" filletAreaMin="0.000144" angleSharp="40 10" angleOverlap="20" bAllowInnerSharp="1">
            <Meshes N="1">104 </Meshes>
            </test_reverse_auto>\n'''.format(model))
    pass

def genTestsProjCrvScene() :
    from pathlib import Path
    
    text = """<?xml version="1.0"?>
    <test_proj_crv_scene model="{0}" epsProj="0.1" bProjPoints="0" bDoRepair="1">
    </test_proj_crv_scene>"""
    p = Path(".")
    for (i, model) in enumerate(p.glob("*.afm")) :
        name = "{0}.test.xml".format(str(model.with_suffix("")))
        with open(str(name), "w") as f:
            f.writelines(text.format(str(model)))
        pass
    return True

#renameTests(r"c:\projects\Test\trng\trng_inject_paths")
