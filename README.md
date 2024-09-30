# HPC Project
By Uros Zivanovic
All files for each respective exercise are located in their respective folder.

# Ex. 1
The most complicated part here is compiling the benchmarks. A script called ```compile_osu.sh``` is provided which can do so on ORFEO.
It's important that before running this script, you create an environment file called .env, where you define the ```MPI_MODULE``` variable (it should be equal to the name of the MPI module you want to use on ORFEO, e.g. ```openMPI/4.1.6/gnu/14.2.1```). 
Additionally, you need to define ```OSU_COMPILED_PATH```, which should point to the place you want the compiled prefix to be.
Once the benchmarks are compiled simply run ```run_osu.sh``` with the same .env file present.

# Ex. 2
The code here is managed through cmake. 
There is a simple compilation script which can used called ```compile.sh```. 
It also expects a .env variable with ```MPI_MODULE``` defined.
If the version of cmake has been updated on ORFEO, this script may throw an error which can be fixed by simply changing the version of cmake the script loads to the latest one.

Once the code is compiled, simply run ```test_c.sh``` and ```test_mand.sh```. 
These expect a .env file with ```MPI_MODULE``` and ```OSU_COMPILED_PATH``` present. 
Additionally, the ```MAND_LOC``` environment variable should point to the location of the compiled 2c binary and the ```TWOA_BIN``` environment variable should point to the location of the compiled 2a binary.

Once all the statistics have been computed, they are saved in json files, which can then be rendered into plots using ```plot_c.py``` and ```plot_m.py```. 
To run these with Python make sure to install numpy and matplotlib.

# Misc. Scripts
For Ex. 2, there are some additional scripts provided. 
These aren't exactly a part of the exercise, but serve as supplemantary material to extend the exercise a bit.
Specifically, ```mand_visualizer.py``` is very fun to play around with.
It allows you to specify a coordinate and zoom level, and then render either an image at that location, or even make a video zooming into that location.
The script is a bit rough, so all parameters are set at the start of the main function.
However, if you'd like to try it out, simply make sure ```MAND_LOC``` is set to the location of the 2c binary, install pillow, tqdm, matplotlib, and numpy, and run it.
