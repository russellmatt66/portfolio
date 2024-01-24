'''
BACKGROUND:
I wrote this python file in order to parse benchmarking data from a process that involved calling 'perf stat' on a C binary that performed binary search.

This benchmarking process was automated using a python launcher, and a bash (.sh) core, to run the C binary with problem sizes
ranging from [(N_min, Nx_min),  (N_max, Nx_max)] where these variables represent 'log2' of the number of particles, and gridpoints, respectively.

The .sh core ran the binary on the given problem size a given number of times (nruns), using perf stat. The output of this call was placed inside a .txt file,
and these files placed at an appropriately named location that reflected the given problem. 

For example: output from running N = 1024, Nx = 1024 would be placed inside 'benchmarking-cpu/N1024/N1024_Nx1024/run{nrun}.txt'

This python file neatly parses the entire complex of output into a '.csv' for each problem size.
For (N_min, Nx_min) = (10, 10), (N_max, Nx_max) = (27, 25), and nruns=25, this represents parsing 7200 .txt files.
For this situation, I have timed this, sequential, code to run in <1 second. 

The performance is accomplished mainly by parsing the data into a 'dict', which is Python's native implementation of a hash table. A hash table is also 
the internal structure of a 'pandas.DataFrame', which makes it very fast to create, and then write, the necessary DataFrames to disk.

Secondary to this, appending the data to Python lists, which represent the values in the 'dict', is a fast way of collecting it.  
'''
'''
Process `benchmarking-cpu/`, and put raw data into subdirectories. 
Then, calculate runtime statistics from the raw data.
CPU: Intel(R) Core(TM) i5-10400F CPU @ 2.90GHz
'''
import pandas as pd
import numpy as np
import sys
import os 

'''
HELPER FUNCTIONS
'''
# Obtain a list of strings representing paths to the datafiles in a sub-sub directory
def getDataFiles(sub_sub_dir: str) -> list[str]:
    print("Getting data files from {}".format(sub_sub_dir))
    data_files = next(os.walk(sub_sub_dir))[2]
    return data_files

# Obtain N from data folder
# `perf_folder` = 'N{#N}_Nx{#Nx}/'
def getN(perf_folder: str) -> int:
    N = perf_folder.split('_Nx')[0]
    N = int(N.split('N')[1])
    return N

# Obtain Nx from data folder
# `perf_folder` = 'N{#N}_Nx{#Nx}/'
def getNx(perf_folder: str) -> int:
    Nx = perf_folder.split('_Nx')[1]
    Nx = int(Nx.split('/')[0])
    return Nx

# Obtain the number of the run from the name of the datafile
# 'perf_file' = 'run{nrun}.txt'
def getRunNum(perf_file: str) -> int:
    nrun = perf_file.split('.')[0]
    nrun = int(nrun.split('run')[1])
    return nrun

# Obtain runtime from a .txt file representing output from a call to `perf stat`
def getRuntime(perf_file: str) -> float:
    runtime = -1.0
    with open(perf_file, 'r') as data_file:
        for line in data_file:
            rtIdx = line.find("seconds time elapsed") # magic string because of perf stat output
            if (rtIdx != -1):
                runtime = float(line[:rtIdx].strip())
                break
    return runtime

# Parse the immediate sub-directories inside the data heap
# Create a csv where the columns are: [N,Nx,nrun,runtime]
def parseSubDirectory(sub_dir: str) -> pd.DataFrame:
    dict = {} # seed for creating the DataFrame
    features = ['N','Nx','nrun','runtime']
    for feature in features:
        dict[feature] = []
    sub_sub_dirs = next(os.walk(sub_dir))[1] # Read in all sub directories of sub_dir (the sub-sub directories)
    # print(sub_sub_dirs)
    # Loop through the sub directories
    for sub_sub_dir in sub_sub_dirs:     
        sub_sub_dir = sub_sub_dir + "/" # Create path
        N = getN(sub_sub_dir) 
        Nx = getNx(sub_sub_dir) 
        data_files = getDataFiles(sub_dir + sub_sub_dir)
        # print("Data files are {}".format(data_files))
        for data_file in data_files:
            nrun = getRunNum(sub_dir + sub_sub_dir + data_file) # Need to construct path out of strings
            runtime = getRuntime(sub_dir + sub_sub_dir + data_file)
            dict['N'].append(N)
            dict['Nx'].append(Nx)
            dict['nrun'].append(nrun)
            dict['runtime'].append(runtime)
    df = pd.DataFrame(dict)
    return df

'''
MAIN CODE
'''
data_heap = sys.argv[1]

# Get the immediate subdirectories inside data_heap 
particle_sizes = next(os.walk(data_heap))[1]

for particle_size in particle_sizes:
    problem_directory = data_heap + particle_size + "/"
    print(problem_directory)
    temp_df = parseSubDirectory(problem_directory)
    temp_df.to_csv(problem_directory + "raw.csv", index=False)
