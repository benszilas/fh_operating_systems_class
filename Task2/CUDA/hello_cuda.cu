#include <iostream>
#include <math.h>
 
// Kernel function to add the elements of two arrays
__global__
void add(int n, float *x, float *y)
{
  int index = blockIdx.x * blockDim.x + threadIdx.x;
  int stride = blockDim.x * gridDim.x;
  for (int i = index; i < n; i += stride)
    y[i] = x[i] + y[i];
}
 
int main(void)
{
 int N = 1<<20;
 float *x, *y;
 
 // Allocate Unified Memory – accessible from CPU or GPU
 cudaError_t err;;
 if ((err = cudaMallocManaged(&x, N*sizeof(float))) || (err = cudaMallocManaged(&y, N*sizeof(float)))) {
   std::cout << "allocation error : " << err;
    return err;
 }

//  // Prefetch the x and y arrays to the GPU
//   if ((err = cudaMemPrefetchAsync(x, N*sizeof(float), (cudaMemLocation){cudaMemLocationTypeDevice, 0}, 0, 0)) || (err = cudaMemPrefetchAsync(y, N*sizeof(float), (cudaMemLocation){cudaMemLocationTypeDevice, 0}, 0, 0))) {
//    std::cout << "allocation error : " << err;
//     return err;
//  }

 // initialize x and y arrays on the host
 for (int i = 0; i < N; i++) {
   x[i] = 1.0f;
   y[i] = 2.0f;
 }
 
 // Run kernel on 1M elements on the GPU
  int blockSize = 256;
  int numBlocks = (N + blockSize - 1) / blockSize;
  add<<<numBlocks, blockSize>>>(N, x, y);
 
 // Wait for GPU to finish before accessing on host
 cudaDeviceSynchronize();
 
 // Check for errors (all values should be 3.0f)
 float maxError = 0.0f;
 for (int i = 0; i < N; i++) {
   maxError = fmax(maxError, fabs(y[i]-3.0f));
 }
 std::cout << "Max error: " << maxError << std::endl;
 
 // Free memory
 cudaFree(x);
 cudaFree(y);
  return 0;
}