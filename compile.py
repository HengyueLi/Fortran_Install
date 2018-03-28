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
parser.add_argument("--compiler", "-c", help="Set compiler, defualt is ifort"    )
parser.add_argument("--flag"    , "-f", help="Set flag to compiler"              )
parser.add_argument("--clib"    , "-l", help="add lib when compilering",nargs='*')

# read arguments from the command line
args = parser.parse_args()
#----------------initiate arguments---------------
if args.compiler:
    print("Set compiler :  %s" % args.compiler)
    Compiler = args.compiler
else:
    #print("Set compiler : ifort (defult) ")
    Compiler = 'ifort'

if args.flag:
    print("Set flag :  %s" % args.flag)
    Cflag = args.flag
else:
    Cflag = " "

if args.clib:
    CLib = " ".join([" -l"+jc for jc in args.clib])
else:
    CLib = " "








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
        l = self.GetlistdirName()
        for jc in l:
            if jc.endswith(suffix):
                r.append(jc)
        return r

    def GetFullPath(self,NameList):
        r = []
        for jc in NameList:
            r.append(os.path.join(self.path, jc))
        return r


def MoveFileBySuffix(SourceFolder,DestinyFolder,suffix):
    sources = GetListDirectory(SourceFolder).GetListdirNameBySuffix(suffix)
    for jc in sources:
        os.rename( os.path.join(SourceFolder,jc) , os.path.join(DestinyFolder,jc)  )



Filename = os.path.basename(__file__)
FilePath = os.path.abspath(__file__)
InstPath = os.path.dirname(FilePath)
ProjPath = os.path.dirname(InstPath)

ModsPath = os.path.join(ProjPath,'Mods')
OfilPath = os.path.join(ProjPath,'Ofil')
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
    # move ofile to current/Ofiles folders
    SubOfil = os.path.join( SubProPath , 'Ofil' )
    MoveFileBySuffix(SourceFolder=SubOfil,DestinyFolder=OfilPath,suffix='.o')
    #-----------------------------------------------------------
    # move all '.mod' files to main project/Mods
    SubMod      = os.path.join(SubProPath,'Mods')
    MoveFileBySuffix(SourceFolder=SubMod,DestinyFolder=ModsPath,suffix='.mod')




#--------------------------------
# scan all o-files
# f = GetListDirectory(ModsPath)
# DependentOfiles = f.GetFullPath( f.GetListdirNameBySuffix('.o') )
# DependentOfilesString = " ".join(DependentOfiles)
f = GetListDirectory(OfilPath)
DependentOfiles = f.GetFullPath( f.GetListdirNameBySuffix('.o') )
DependentOfilesString = " ".join(DependentOfiles)

#--------------------------------
# scan all include files
f     = GetListDirectory(InclPath)
Iflag = " ".join( [" -I" + jc + " " for jc in f.GetFullPath(   f.GetlistdirNameNonehidden() )] )

#--------------------------------
#  compile
os.chdir(ProjPath)
CompileCommand = Compiler +" -c "+ ComFlag + " -IMods " + Iflag +DependentOfilesString+"  *.f90 "+CLib
os.system(CompileCommand)
#--------------------------------
# move mods into folder Mods
MoveFileBySuffix(SourceFolder=ProjPath,DestinyFolder=ModsPath,suffix='.mod')
#-------------------------------
# move wanted ofile into Ofil
MoveFileBySuffix(SourceFolder=ProjPath,DestinyFolder=OfilPath,suffix='.o')
