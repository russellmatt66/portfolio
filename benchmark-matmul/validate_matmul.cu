// #include "../include/matrix.cu"
// #include "../include/matmul.cu"

#include <stdio.h>
#include <assert.h>
#include <cuda_runtime.h>
#include <curand.h>
#include <curand_kernel.h>
#include <math.h>
#include <cstdlib>
#include <cstdint>	
#include <filesystem>
#include <fstream>
#include <iostream>
#include <string>
#include <thread>

// row-major order
#define IDX2D(i, j, N) (((i)*(N))+(j))

// Device code
__global__ void InitializeMatrices(float *C, float *A, float *B, const int N, const unsigned long long seed){
	int tidx = threadIdx.x + blockIdx.x * blockDim.x;
	int tidy = threadIdx.y + blockIdx.y * blockDim.y; 
	int xthreads = gridDim.x * blockDim.x;
	int ythreads = gridDim.y * blockDim.y; 

	// Generate random number b/w [0.0, 1.0]
    curandState_t state;
    if (tidx < N && tidy < N){
        curand_init(seed, tidx, 0, &state);
    }

	for (int i = tidx; i < N; i += xthreads){
		for (int j = tidy; j < N; j += ythreads){
			A[IDX2D(i, j, N)] = static_cast<float>(curand_uniform(&state));
			B[IDX2D(i, j, N)] = static_cast<float>(curand_uniform(&state));
			C[IDX2D(i, j, N)] = 0.0;
		}
	}
	return;
}

__global__ void MatMul(float *C, const float *A, const float *B, const int N){ 
	int tidx = threadIdx.x + blockIdx.x * blockDim.x;
	int tidy = threadIdx.y + blockIdx.y * blockDim.y; 
	int xthreads = gridDim.x * blockDim.x;
	int ythreads = gridDim.y * blockDim.y; 

	float sum;
	for (int i = tidx; i < N; i += xthreads){
		for (int j = tidy; j < N; j += ythreads){
			sum = 0.0;
			for (int k = 0; k < N; k++){
				sum += A[IDX2D(i, k, N)] * B[IDX2D(k, j, N)];
			}
			C[IDX2D(i, j, N)] = sum;
		}
	}
	return;
} 

/* Host Code */
void hostMatMul(float* C, const float *A, const float *B, const int N, const int begin, const int end){
    // row-major storage
    float sum;
    for (int i = begin; i < end; i++){ 
        for (int j = begin; j < end; j++){
            sum = 0.0;
            for (int k = 0; k < N; k++){
                sum += A[IDX2D(i, j, N)] * B[IDX2D(i, j, N)];
            }
            C[IDX2D(i, j, N)] = sum;
        }
    }
    return;
}

// Validating on host because arrays get relatively large on GPU, and it's simpler to not have to weave freeing up space with getting work done 
void hostValidate(const float* d_C, const float *h_C, const int N, bool *are_same, const int begin, const int end){
    *are_same = true; // don't want compiler optimizing its way through the validation check
    float threshold = 0.000001;
    for (int i = begin; i < end; i++){
        for (int j = begin; j < end; j++){
            if (abs(d_C[IDX2D(i, j, N)] - h_C[IDX2D(i, j, N)]) > threshold){
                std::cout << "(i,j) = (" << i << "," << j << ")" << std::endl;
                std::cout << "d_C = " << d_C[IDX2D(i, j, N)] << std::endl;
                std::cout << "h_C = " << h_C[IDX2D(i, j, N)] << std::endl;
                *are_same = false;
                break;
            }
        }
    }
    return;
}

// https://stackoverflow.com/questions/14038589/what-is-the-canonical-way-to-check-for-errors-using-the-cuda-runtime-api
#define checkCuda(ans) { gpuAssert((ans), __FILE__, __LINE__); }
inline void gpuAssert(cudaError_t code, const char *file, int line, bool abort=true)
{
   if (code != cudaSuccess) 
   {
      fprintf(stderr,"GPUassert: %s %s %d\n", cudaGetErrorString(code), file, line);
      if (abort) exit(code);
   }
}

int main(int argc, char* argv[]){
	// Accept arguments 
	// int N = atoi(argv[1]); // length of matrix side - CHECK IF THIS IS CAUSING BUG
	uint64_t N = atoll(argv[1]);
	int SM_multiplier_x = atoi(argv[2]); // used for changing number of blocks
	int SM_multiplier_y = atoi(argv[3]);
	int num_threads_per_block_x = atoi(argv[4]);
	int num_threads_per_block_y = atoi(argv[5]);

	// Allocate device matrices
	float *A, *B, *C; // flattened arrays because that is easiest with CUDA
    
	uint64_t requested_matrix_memory = N*N*sizeof(float);

	checkCuda(cudaMalloc(&A, requested_matrix_memory));
	checkCuda(cudaMalloc(&B, requested_matrix_memory));
	checkCuda(cudaMalloc(&C, requested_matrix_memory));

    // Allocate host matrices
    float *h_A, *h_B, *h_C; 

    h_A = (float*)malloc(requested_matrix_memory);
    h_B = (float*)malloc(requested_matrix_memory);
    h_C = (float*)malloc(requested_matrix_memory);

	std::cout << "Size of matrices is: " << pow(N,2) << std::endl;

    // Get device attributes 
    int deviceId;
    int numberOfSMs;

    cudaGetDevice(&deviceId);
    cudaDeviceGetAttribute(&numberOfSMs, cudaDevAttrMultiProcessorCount, deviceId);

	// Define execution configuration
	dim3 block_dimensions(num_threads_per_block_x, num_threads_per_block_y);
	dim3 grid_dimensions(numberOfSMs * SM_multiplier_x, numberOfSMs * SM_multiplier_y);

	// Set up timer
	cudaEvent_t start_search, stop_search;
    cudaEventCreate(&start_search);
    cudaEventCreate(&stop_search);
    float time_search;

	// Initialize Matrices
	InitializeMatrices<<<block_dimensions, grid_dimensions>>>(C, A, B, N, 1234); // Magic number at the end is seed for rng
	checkCuda(cudaDeviceSynchronize());

    // Copy device data to host
    checkCuda(cudaMemcpy(h_A, A, requested_matrix_memory, cudaMemcpyDeviceToHost));
    checkCuda(cudaMemcpy(h_B, B, requested_matrix_memory, cudaMemcpyDeviceToHost));
    checkCuda(cudaMemcpy(h_C, C, requested_matrix_memory, cudaMemcpyDeviceToHost));
    checkCuda(cudaDeviceSynchronize());

    // Perform Matrix Multiplication on Host
    std::thread t1(hostMatMul, h_C, h_A, h_B, N, 0, N/4);
    std::thread t2(hostMatMul, h_C, h_A, h_B, N, N/4, N/2);
	std::thread t3(hostMatMul, h_C, h_A, h_B, N, N/2, 3*N/4);
    std::thread t4(hostMatMul, h_C, h_A, h_B, N, 3*N/4, N);

    t1.join(); t2.join(); t3.join(); t4.join();

    // Perform Matrix Multiplication on Device
	cudaEventRecord(start_search, 0);
	MatMul<<<block_dimensions, grid_dimensions>>>(C, A, B, N);
	cudaEventRecord(stop_search, 0);
	cudaEventSynchronize(stop_search);
	cudaEventElapsedTime(&time_search, start_search, stop_search);

	std::cout << "Elapsed time is: " << time_search << " ms" << std::endl;

    // Validate that matrices are the same
    float *v_C; 

    v_C = (float*)malloc(requested_matrix_memory);
    checkCuda(cudaMemcpy(v_C, C, requested_matrix_memory, cudaMemcpyDeviceToHost));
    checkCuda(cudaDeviceSynchronize());

    bool are_same1, are_same2, are_same3, are_same4; // simpler than using lambdas and <future>

    std::thread v1(hostValidate, v_C, h_C, N, &are_same1, 0, N/4);
    std::thread v2(hostValidate, v_C, h_C, N, &are_same2, N/4, N/2);
    std::thread v3(hostValidate, v_C, h_C, N, &are_same3, N/2, 3*N/4);
    std::thread v4(hostValidate, v_C, h_C, N, &are_same4, 3*N/4, N);

    v1.join(); v2.join(); v3.join(); v4.join();

    if (are_same1 && are_same2 && are_same3 && are_same4){
        std::cout << "h_C and d_C are the same :) " << std::endl;
    }
    else {
        std::cout << "h_C and d_C not the same :( " << std::endl;
        std::cout << "are_same 1 = " << are_same1 << std::endl;
        std::cout << "are_same 2 = " << are_same2 << std::endl;
        std::cout << "are_same 3 = " << are_same3 << std::endl;
        std::cout << "are_same 4 = " << are_same4 << std::endl;
    }

	// Free data
	cudaFree(A);
	cudaFree(B);
	cudaFree(C);
    free(h_A);
    free(h_B);
    free(h_C);
    free(v_C);
	return 0;
}