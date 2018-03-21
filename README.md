# ddeels_script
Python script to initialize some ddeels input parameters

runs with python 2.7

To see options, execute "python init_ddeels.py -h" in terminal

To run ddeels, stick the ddeels.in and ag_palik_eps.dat file in a directory, and run the "python init_ddeels <options>" in there.  

Then you can run "ddeels.exe < ddeels.in" and gnuplot ag_cube.gnu to get the picture of the spectrum.


Quirks from hard coding stuff/Features coming soon:

Only designed to work for single element samples

Impars are placed at midpoint of a side and on corner. 
