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
  // printf(" inside sum_vector problem_setup, N=%lld \n", N);
  for (int i = 0; i < N; i++)
    A[i] = i;
}

int64_t
sum(int64_t N, uint64_t A[])
{
  // printf(" inside sum_vector perform_sum, N=%lld \n", N);
  int64_t answer = 0;
  for (int i = 1; i < N; i++)
    answer += A[i];
  return answer;
}

