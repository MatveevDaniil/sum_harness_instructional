"""

E. Wes Bethel, Copyright (C) 2022

October 2022

Description: This code loads a .csv file and creates a 3-variable plot

Inputs: the named file "sample_data_3vars.csv"

Outputs: displays a chart with matplotlib

Dependencies: matplotlib, pandas modules

Assumptions: developed and tested using Python version 3.8.8 on macOS 11.6

"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df_direct = pd.read_csv("build/sum_direct.csv")
df_vector = pd.read_csv("build/sum_vector.csv")
df_indirect = pd.read_csv("build/sum_indirect.csv")

assert df_vector.problem_size.equals(df_direct.problem_size)
assert df_indirect.problem_size.equals(df_direct.problem_size)

dfs = {
  "direct": df_direct,
  "vector": df_vector,
  "indirect": df_indirect
}

def kernel_time(kernel_type):
  # measuring time = runtime(sec)
  return dfs[kernel_type].elapsed_time

def mflops(kernel_type):
  # measuring MFLOP/s = ops/time, where
  # ops = number of operations/1M
  # time = runtime(sec)
  time = kernel_time(kernel_type)
  mflop = dfs[kernel_type].problem_size / 10 ** 6
  return mflop / time

# theoretical peak memory bandwidth of vm I am using
# capacity = 281.6 * 2 ** 30 # bytes/sec

# theoretical peak memory bandwidth of my laptop
memory_speed = 2400 * 10 ** 6 # Hz
bus_width = 8 # bytes
channels_num = 2
capacity = memory_speed * bus_width * channels_num # bytes/sec 38.400.000.000

def bandwidth(kernel_type):
  # measuring % of memory bandwidth utilized = (bytes/time) / (capacity), where
  # bytes = number of memory bytes accessed by your program
  # time = runtime of your program (secs)
  # capacity = theoretical peak memory bandwidth of the system
  time = kernel_time(kernel_type)
  if kernel_type == 'direct':
    bytes = 0
  else:
    bytes = dfs[kernel_type].problem_size * 8
  return (bytes / time) / capacity

def latency(kernel_type):
  # measuring Avg memory latency = time/accesses, where
  # time = runtime(sec) 
  # accesses = number of program memory accesses
  time = kernel_time(kernel_type)
  if kernel_type == 'direct':
    accesses = 0
  else:
    accesses = dfs[kernel_type].problem_size
  return time / accesses

if not os.path.exists("images"):
  os.mkdir(f"images")
for metric, metric_compute, units in [
  ('time', kernel_time, 'sec'),
  ('mflops', mflops, 'MFLOP/s'),
  ('bandwidth', bandwidth, '% Bandwidth'),
  ('latency', latency, 'sec per access')
]:
  plt.title("Comparison of ways to compute 0 + 1 + ... + N-1")

  problem_sizes = dfs['direct'].problem_size
  xlocs = range(len(problem_sizes))
  x_labels = [f'$2^{{{int(np.log2(size))}}}$' for size in problem_sizes] 
  plt.xticks(xlocs, x_labels)

  direct_res = metric_compute('direct')
  vector_res = metric_compute('vector')
  indirect_res = metric_compute('indirect')
  print(f'{metric} vector/indirect = {(vector_res / indirect_res).mean():.4f}')
  print(direct_res.to_list(), direct_res.mean())
  print(vector_res.to_list(), vector_res.mean())
  print(indirect_res.to_list(), indirect_res.mean())
  print('=' * 50)
  plt.plot(direct_res, "r-o")
  plt.plot(vector_res, "b-x")
  plt.plot(indirect_res, "g-^")

  #plt.xscale("log")
  plt.yscale("log")

  plt.xlabel("Problem Sizes")
  plt.ylabel(f"{metric} ({units})")

  varNames = ['direct sum', 'vector sum', 'indirect sum']
  plt.legend(varNames, loc="best")

  plt.grid(axis='both')

  plt.savefig(f"images/{metric}.png", dpi=300)
  plt.clf()

# EOF
