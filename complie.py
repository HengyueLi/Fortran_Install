#!/usr/bin/env python3




import os,sys

Compiler = sys.argv[1]
ComFlag  = sys.argv[2]

def listdir_nohidden(path):
    for f in os.listdir(path):
        if not f.startswith('.'):
            yield f

def GetListdirBySuffix(path,suffix):
    r = []
    for file in os.listdir(path):
        if file.endswith(suffix):
            r.append(  os.path.join(path, file) )
    return r







FilePath = os.path.abspath(__file__)
InstPath = os.path.dirname(FilePath)
ProjPath = os.path.dirname(InstPath)

ModsPath = os.path.join(ProjPath,'Mods')
InclPath = os.path.join(ProjPath,'Incl')
DepePath = os.path.join(ProjPath,'Depe')




SubProjList = listdir_nohidden(DepePath)





#--------------------------------
#   pre-compile dependence
for pro in SubProjList:
    SubProPath = os.path.join(DepePath,pro)
    pyfile     = os.path.join(SubProPath,'Install','compile.py')
    #-----------------------------------------------------------
    # run python file in the sub project.
    os.system( 'python3 '+ pyfile + sys.argv[1] + sys.argv[2])
    #-----------------------------------------------------------
    # move ofile to current/Mods folders
    ObtainedOfile = pro + '.o'
    OfilePath     = os.path.join(SubProPath,OfilePath)
    # Folder Mods used to temperally save all lib.o files. After final '.o' file is obtained, delete them.
    DestiPath     = os.path.join(ModsPath,ObtainedOfile)
    os.rename( OfilePath ,  DestiPath )
    #-----------------------------------------------------------
    # move all .mod file to main project/Mods
    SubMod = os.path.join(SubProPath,'Mods')
    os.system( 'mv '+SubMod+" *.mod "+ ModsPath  )


#--------------------------------
#  compile
DependentOfiles = GetListdirBySuffix(ModsPath,'.o')
DependentOfilesString = " ".join(DependentOfiles)
os.chdir(ProjPath)
CompileCommand = Compiler +" -c "+ ComFlag + " -IMods "+DependentOfilesString+"  *.f90 -llapack "
print(CompileCommand)
os.system(CompileCommand)
os.system('mv *.mod ./Mods')
#-------------------------------
#  delete dependency.o
for jc in DependentOfiles:
    os.remove(jc)
