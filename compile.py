#!/usr/bin/env python3




import argparse,sys,os
#===============================================================================
# get interpreter
python = sys.executable
#===============================================================================




#===============================================================================
#  get arguments
#===============================================================================
parser = argparse.ArgumentParser()
#--------add options
parser.add_argument("--compiler", "-c", help="Set compiler, defualt is ifort")
parser.add_argument("--flag", "-f", help="Set flag to compiler")

# read arguments from the command line
args = parser.parse_args()
#----------------initiate arguments---------------
if args.compiler:
    print("Set compiler :  %s" % args.compiler)
    Compiler = args.compiler
else:
    print("Set compiler : ifort (defult) ")
    Compiler = 'ifort'

if args.flag:
    print("Set flag :  %s" % args.flag)
    Cflag = args.flag
else:
    Cflag = " "








Compiler  = Compiler
ComFlag   = Cflag
PythonArg = " ".join(sys.argv[1:])



class GetListDirectory():
    def __init__(self,dpath):
        self.path = dpath

    def GetlistdirName(self):
        return os.listdir(self.path)

    def GetlistdirNameNonehidden(self):
        l = self.GetlistdirName()
        r = []
        for jc in l:
            if not jc.startswith('.'):
                r.append(jc)
        return r

    def GetListdirNameBySuffix(self,suffix):
        r = []
        l = selfl.GetlistdirName()
        for jc in l:
            if jc.endswith(suffix):
                r.append(jc)
        return r

    def GetFullPath(self,NameList):
        r = []
        for jc in NameList:
            r.append(os.path.join(self.path, jc))
        return r


Filename = os.path.basename(__file__)
FilePath = os.path.abspath(__file__)
InstPath = os.path.dirname(FilePath)
ProjPath = os.path.dirname(InstPath)

ModsPath = os.path.join(ProjPath,'Mods')
InclPath = os.path.join(ProjPath,'Incl')
DepePath = os.path.join(ProjPath,'Depe')



#--------------------------------
#   pre-compile dependence

# get list of subproject
SubProjList = GetListDirectory(DepePath).GetlistdirNameNonehidden()
for pro in SubProjList:
    SubProPath = os.path.join(DepePath,pro)
    pyfile     = os.path.join(SubProPath,'Install',Filename)
    #-----------------------------------------------------------
    # run python file in the sub project.
    os.system( python + " " + pyfile +" " + PythonArg )
    #-----------------------------------------------------------
    # move ofile to current/Mods folders
    ObtainedOfile = pro + '.o'
    OfilePath     = os.path.join(SubProPath,ObtainedOfile)
    # Folder Mods used to temperally save all lib.o files. After final '.o' file is obtained, move them out.
    DestiPath     = os.path.join(ModsPath,ObtainedOfile)
    os.rename( OfilePath ,  DestiPath )
    #-----------------------------------------------------------
    # move all '.mod' files to main project/Mods
    SubMod      = os.path.join(SubProPath,'Mods')
    submodfiles = GetListDirectory(SubMod).GetListdirNameBySuffix('.mod')
    for jc in submodfiles:
        os.rename(  os.path.join(SubMod,jc) ,  os.path.join(ModsPath,jc)    )







f = GetListDirectory(ModsPath)
DependentOfiles = f.GetFullPath( f.GetListdirNameBySuffix('.o') )
DependentOfilesString = " ".join(DependentOfiles)
#--------------------------------
#  compile
os.chdir(ProjPath)
CompileCommand = Compiler +" -c "+ ComFlag + " -IMods "+DependentOfilesString+"  *.f90 -llapack "
os.system(CompileCommand)
ProjectModsfiles = GetListDirectory(ProjPath).GetListdirNameBySuffix('.mod')
#--------------------------------
# move mods into folder Mods
for jc in ProjectModsfiles:
    os.rename( os.path.join(ProjPath,jc) , os.path.join(ModsPath,jc)       )
#-------------------------------
#  delete dependency.o
for jc in DependentOfiles:
    os.remove(jc)
