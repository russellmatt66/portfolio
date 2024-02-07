# Overview
Code written as part of a project to implement a CUDA kernel that performs Matrix Multiplication (`matmul`), and then benchmark it. 

# Directory Structure
validate_matmul.cu
- CUDA code that validates `matmul` kernel
- Uses `<thread>` to parallelize CPU code with 4 threads 
- `nvcc -o val_mm validate_matmul.cu`
- `./val_mm N SM_multiplier_x SM_multiplier_y num_threads_per_blk_x num_threads_per_blk_y`
