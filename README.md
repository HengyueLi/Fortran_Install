# License
Please ignore all the License information IN THE SOURCE CODE.
# Documents
Recently the documents are not well prepared. The module can do much more than what has been shown in the example code. If one has some problem with how to use it, please leave messages.
# Preparation --python3.
The code used the syntax of Fortran(2003). Therefore an newly version of fortran compiler is required.
Even though there is only one f90 file in the project, there are (maybe) many dependencies. One should follow steps. This code, in principle, can be used in any OS. But here I write a python script to make the code become easier to use. So a python3 intepretation should have been installed. This script, in principle, can only run on a Unix-like OS. If you use windows, try to make command tool to be used ( basically to make sure the command like:

      gfortran main.f90 -o run.exe
 can be called.). If you do not use the script, you can abstract all the f90 file in /Depe (recursively).

# Structure of the code.
In the project one may see 5 folders: /Depe, /Incl, /Mods, /Ofil and /Install. When download the project, one need to make sure all the dependencies in /Depe are also downloaded recursively. Otherwise it maybe empty. Especially, there are always some in /Install. If it is empty, one have not downloaded it correctly. The problem may be cuased by the submodule in git. Consider use something like 'git clone --recursive YOUR-GIT-REPO-URL' or other software to download it. Or search 'How to git clone including submodules' on internet.

# Compile
Directly run

    python3 compile.py

 in command line where compile.py is in /Install. In such case, a defult choice of compiler (ifort) is assumed. If you want to use other compiler, say gfortran:

    python3 compile.py -c gfortran

One can check detailes of other options by

    python3 compile.py -h



# How to use.
After the compiling, one can found many '.o' files in /Ofil and '.mod' in /Mods. Only this object files can be used. For instance one may use the lib in his own code 'main.f90', then compile the code by command( ifort for example):

    ifort /Ofil/*.o -IMods main.f90 -o run.exe

In case some modules are lapack dependent, use:

    ifort /Ofil/*.o -IMods main.f90 -o run.exe -llapack

One should notice that the chosen compiler should be the same as the previous one in [Compile](https://github.com/HengyueLi/Fortran_Install#compile). The default chosen compiler is ifort as mentioned.

# Obligation (will update):
People whose research is benefited from this code would be asked to CONSIDER to cite the papers below:

*
