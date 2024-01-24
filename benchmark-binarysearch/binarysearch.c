/*
Implement binary search for benchmarking
*/
#include <math.h>
#include <time.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>

#define M_PI 3.14159265358979323846

// Binary search
int binarySearch(double* particles, double* grid, const int i, const int N, const int Nx){
    int low = 0, high = Nx-1;
    int guess, count = 0;

    double particle_pos = particles[i];
    while (low <= high && count <= log2(Nx)){
        guess = (low + high) / 2;
        if (particle_pos >= grid[guess] && particle_pos < grid[guess + 1]){
            return guess;
        }
        else if (particle_pos < grid[guess]){ // to left of guess
            high = guess;
        }
        else if (particle_pos > grid[guess+1]){ // to right of guess
            low = guess;
        }
        count++;
    }
    if (particle_pos == grid[Nx-1]){ // original condition does not return guess if this is true
        return Nx - 1;
    }
    return -1;
}

void initParticles(double* particles, const int N, const double x_min, const double x_max){
    // Assign uniformly-distributed random value to particles in range [x_min, x_max]
    srand(time(NULL));
    double rand_num = (double)rand() / (double)RAND_MAX; // [0,1]
    rand_num = (x_max - x_min) * rand_num + x_min;

    for (int i = 0; i < N; i++){
        particles[i] = rand_num;
        rand_num = (double)rand() / (double)RAND_MAX;
        rand_num = (x_max - x_min) * rand_num + x_min;
    }  

    return; 
}

void initGrid(double* grid, const int Nx, const double x_min, const double x_max){
    // Assign uniformly-spaced values to cartesian grid
    double dx = (x_max - x_min) / (Nx - 1); // length of cell
    for (int j = 0; j < Nx; j++){
        grid[j] = x_min + dx * j;
    }
    return;
}

void initFound(int* found, const int N){
    // Assign all -1
    for (int i = 0; i < N; i++){
        found[i] = -1;
    }
    return;
}

void printData(double* grid, double* particles, int* found, const int N, const int Nx){
    for (int j = 0; j < Nx; j++){
        printf("Gridpoint %d has value %4.3f\n", j, grid[j]);
    }

    for (int i = 0; i < N; i++){
        printf("Particle %d, located at %4.3f, was found in cell %d\n", i, particles[i], found[i]);
    }
    return;
}

// Validate binary search
void linearSearch(const double* grid, const double* particles, int* found, const int N, const int Nx){
    for (int i = 0; i < N; i++){
        for (int j = 0; j < Nx - 1; j++){
            if (particles[i] >= grid[j] && particles[i] < grid[j+1]){
                found[i] = j;
                continue;
            }
        }
    }
    return;
}

int main(int argc, char* argv[]){
    int N = atoi(argv[1]);
    int Nx = atoi(argv[2]);

    double *particles, *grid;
    particles = (double*)malloc(N*sizeof(double));
    grid = (double*)malloc(Nx*sizeof(double));

    int *found;
    found = (int*)malloc(N*sizeof(int));
    // int *found_linear;
    // found_linear = (int*)malloc(N*sizeof(int));

    // Initialize grid: uniform, cartesian
    double x_min = -M_PI;
    double x_max = M_PI;
    initGrid(grid, Nx, x_min, x_max);

    // Initialize particles: uniform, random
    initParticles(particles, N, x_min, x_max);

    // Initialize found: all -1
    initFound(found, N);

    // Find the particles
    for (int i = 0; i < N; i++){
        found[i] = binarySearch(particles, grid, i, N, Nx);
    }

    // linearSearch(grid, particles, found_linear, N, Nx);
    // bool foundSame = true;
    // for (int i = 0; i < N; i++){ // why do this seperately? Doesn't really matter, gonna get commented out in production
    //     if (found[i] != found_linear[i]){
    //         foundSame = false;
    //         break;
    //     }
    // }

    // // Validate data via printing - only really works for small problems, I know
    // printData(grid, particles, found, N, Nx);
    // printf("Did searches find the same? %d\n", foundSame);

    free(particles);
    free(grid);
    free(found);
    // free(found_linear);

    return 0;
}
