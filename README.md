# Preparation --python3.
Even though there is only one f90 file in the project, there are (maybe) many dependencies. One should follow steps. This code, in principle, can only be used in Unix like system. And a python3 intepretation should have been installed.

# Structure of the code.
In the project one may see 5 folders: /Depe, /Incl, /Mods, /Ofil and /Install. When download the project, one need to make sure all the dependencies in /Depe are also downloaded recursively. Otherwise it maybe empty. Especially, there are always some in /Install. If it is empty, one have not downloaded it correctly. The problem may be cuased by the submodule in git. Consider use something like 'git clone --recursive YOUR-GIT-REPO-URL' or other software to download it. Or search 'How to git clone including submodules' on internet.

# Compile.
run "python3 compile.py [o]" in command line where compile.py is in /Install.
[o] represent options while can be empty. One can check detailes by "python3 compile.py -h".

## Some illusrtations:
* -c : set compiler .  "python3 compile.py -c gfortran" for instance. The defult compiler is 'ifort'
* -f : set some flag to compiler.
* -l : add some lib path to compiler. The syntax is the same in general compilers. For example '-llapack' to use lapack.

# How to use.
After the compiling, one can found many '.o' files in /Ofil and '.mod' in /Mods. Only this object files can be used. For instance one may use the lib in his own code 'main.f90', then compile the code by use 'gfortran /Ofil/*.o -IMods main.f90 -o run.exe'.
One should notice that the chosen compiler should be the same as the previous using.
