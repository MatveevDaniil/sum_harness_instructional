#include <algorithm>
#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>
#include <string.h>



void 
setup(int64_t N, uint64_t A[])
{
  //  printf(" inside sum_indirect problem_setup, N=%lld \n", N);
  std::vector<bool> visited(N);
  for (int i = 0; i < N; i++)
    A[i] = i;
  std::random_device rd;
  std::mt19937 gen(rd()); 
  for (int64_t pivot = 0; pivot < N - 1; pivot++) {
    std::uniform_int_distribution<> dis(pivot + 1, N - 1);
    int64_t rnd_idx = dis(gen);
    std::swap(A[pivot], A[rnd_idx]);
  }
  // verification step
  for (int i = 0; i < N; i++)
    visited[i] = false;
  int64_t idx = 0;
  for (int64_t i = 0; i < N; i++) {
    visited[idx] = true;
    idx = A[idx];
  }
  for (int i = 0; i < N; i++) {
    if (!visited[i])
      throw "Error in setup method for N=" + std::to_string(N);
  }
}

int64_t
sum(int64_t N, uint64_t A[])
{
  //  printf(" inside sum_indirect perform_sum, N=%lld \n", N);
  int64_t answer = 0;
  for (int64_t i = A[0]; i != 0; i = A[i])
    answer += i;
  return answer;
}