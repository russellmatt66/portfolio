import sys
import os
import subprocess
import math

# Create benchmarking directory and data folders
benchmarking_path = "./benchmarking-cpu/"
try:
    os.mkdir(benchmarking_path)
    print(f"Directory '{benchmarking_path}' created successfully.")
except FileExistsError:
    print(f"Directory '{benchmarking_path}' already exists.")
except Exception as e:
    print(f"An error occurred: {e}")

N_max = int(sys.argv[1]) # largest N benchmarked = 2**N_max
Nx_max = int(sys.argv[2]) # largest Nx benchmarked = 2**Nx_max

N_sizes = [2**i for i in range(10, N_max + 1)]
Nx_sizes = [2**j for j in range(10, Nx_max + 1)]

# print(N_sizes)
# print(Nx_sizes)

problem_sizes = []
for N in N_sizes:
    for Nx in Nx_sizes:
        problem_sizes.append((N,Nx))

# print(problem_sizes)

''' Create a subdirectory for each of the given problem sizes '''
# Create folders for each N
for N in N_sizes:
    data_directory = benchmarking_path + "N" + str(N) + "/"
    try:
        os.mkdir(data_directory)
        print(f"Directory '{data_directory}' created successfully.")
    except FileExistsError:
        print(f"Directory '{data_directory}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Create subdirectories for each problem size
for problem_size in problem_sizes:
    (N, Nx) = problem_size
    data_folder = benchmarking_path + "N" + str(N) + "/" + "N" + str(N) + "_Nx" + str(Nx) + "/"
    try:
        os.mkdir(data_folder)
        print(f"Directory '{data_folder}' created successfully.")
    except FileExistsError:
        print(f"Directory '{data_folder}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")
    
# Run bash script that executes `perf stat ./cpu-bs N Nx` an adequate number of times for each of the possible problem sizes 
num_runs = int(sys.argv[3])

if len(sys.argv) == 4: # starting fresh
    print("Starting fresh")
    for problem_size in problem_sizes:
        (N, Nx) = problem_size
        data_folder = benchmarking_path + "N" + str(N) + "/" + "N" + str(N) + "_Nx" + str(Nx) + "/"
        subprocess.run(["./benchmarking-cpu.sh", str(N), str(Nx), str(1), str(num_runs), data_folder])

# Process error state using string, e.g., 
# `./machine-learning/benchmarking-cpu/N4194304/N4194304_Nx65536/run16.txt`
if len(sys.argv) == 5: # Error occurred and benchmarking needs to restart from a specific place
    error_string = sys.argv[4]
    error_string = error_string.split('.txt')[0]  
    nrun_error = error_string.split('run')[1]
    N_error = error_string.split('/N')[1]
    Nx_error = error_string.split('_Nx')[1]
    Nx_error = Nx_error.split('/')[0]
    Nx_sizes_error = [2**j for j in range(int(math.log2(int(Nx_error))), Nx_max + 1)]
    N_sizes_error = [2**i for i in range(int(math.log2(int(N_error))) + 1, N_max + 1)]
    problem_sizes_error = []
    for N in N_sizes_error:
        for Nx in Nx_sizes:
            problem_sizes_error.append((N,Nx))

# print(N_sizes_error)
# print(Nx_sizes_error)
# print(problem_sizes_error)

# print(len(sys.argv))
# print(Nx_error)
# print(N_error)

# N_error_exp = int(math.log2(int(N_error)))

if len(sys.argv) == 5: # separate processing the state of the error from restarting the benchmarking 
    # Complete work starting from problem that had error
    for Nx in Nx_sizes_error:
        if (Nx == int(Nx_error)):
            print("Restarting from where error occurred in {}".format(error_string))
            # print("Calling `./benchmarking-cpu.sh` with N = {}, Nx = {}, init_run = {}, num_runs = {}".format(N_error, Nx, nrun_error, num_runs))
            data_folder = benchmarking_path + "N" + str(N_error) + "/" + "N" + str(N_error) + "_Nx" + str(Nx) + "/"
            subprocess.run(["./benchmarking-cpu.sh", str(N_error), str(Nx), nrun_error, str(num_runs), data_folder])
        else:
            # print("Calling `./benchmarking-cpu.sh` with N = {}, Nx = {}, init_run = {}, num_runs = {}".format(N_error, Nx, 1, num_runs))
            data_folder = benchmarking_path + "N" + str(N_error) + "/" + "N" + str(N_error) + "_Nx" + str(Nx) + "/"
            subprocess.run(["./benchmarking-cpu.sh", str(N_error), str(Nx), str(1), str(num_runs), data_folder])
     # Complete rest of work
    for problem_size in problem_sizes_error:
        (N, Nx) = problem_size
        data_folder = benchmarking_path + "N" + str(N) + "/" + "N" + str(N) + "_Nx" + str(Nx) + "/"
        # print("Calling `./benchmarking-cpu.sh` with N = {}, Nx = {}, init_run = {}, num_runs = {}".format(N, Nx, 1, num_runs))
        subprocess.run(["./benchmarking-cpu.sh", str(N), str(Nx), str(1), str(num_runs), data_folder])
