import xarray as xr
import numpy as np
import pandas as pd
import os

newpath = r'./sep_csv' 
if not os.path.exists(newpath):
    os.makedirs(newpath)

total_output_num = 212*4
node_num = 215
for file_num in range(total_output_num):
    if (file_num>1):
        skiprow_num = 6+1+node_num+(file_num-1)*(node_num+3+1)+3
    elif (file_num==1):
        skiprow_num = 6+1+node_num+3
    else:
        skiprow_num = 6
    out_data = pd.read_csv('./output.csv', skiprows=skiprow_num, nrows=node_num)
    # hs_data
    # save to a new file
    filename = "./sep_csv/output_"+str(file_num)+".csv"
    out_data.to_csv(filename, index=False)  

time_stamps_sim_0 = pd.date_range(start='2016-11-1 00:00:00', end='2017-5-1 00:00:00', freq="6h")
time_stamps_sim = pd.date_range(start='2016-11-1 00:00:00', end='2016-11-30 23:59:59', freq="6h")
num_file = len(time_stamps_sim)
# file_start = len(time_stamps_sim_0)
file_start = 1
num_file = len(time_stamps_sim)
count = 0
out_data = 0.0
for time in range(file_start, min(file_start+num_file, total_output_num), 1):
    filename = r'./sep_csv/output_'+str(time)+'.csv'
    if count==0:
        out_data = pd.read_csv(filename, skiprows=None, nrows=node_num)
    else:
        out_data += pd.read_csv(filename, skiprows=None, nrows=node_num)
    count+=1
    print(filename)

out_data /= count
out_data.to_csv(r'./11.csv', index=False)

time_stamps_sim_0 = pd.date_range(start='2016-11-1 00:00:00', end='2016-12-1 00:00:00', freq="6h")
time_stamps_sim = pd.date_range(start='2016-12-1 00:00:00', end='2016-12-31 23:59:59', freq="6h")
num_file = len(time_stamps_sim)
file_start = len(time_stamps_sim_0)
num_file = len(time_stamps_sim)
count = 0
out_data = 0.0
for time in range(file_start, min(file_start+num_file, total_output_num), 1):
    filename = r'./sep_csv/output_'+str(time)+'.csv'
    if count==0:
        out_data = pd.read_csv(filename, skiprows=None, nrows=node_num)
    else:
        out_data += pd.read_csv(filename, skiprows=None, nrows=node_num)
    count+=1
    print(filename)

out_data /= count
out_data.to_csv(r'./12.csv', index=False) 

time_stamps_sim_0 = pd.date_range(start='2016-11-1 00:00:00', end='2017-1-1 00:00:00', freq="6h")
time_stamps_sim = pd.date_range(start='2017-1-1 00:00:00', end='2017-1-31 23:59:59', freq="6h")
num_file = len(time_stamps_sim)
file_start = len(time_stamps_sim_0)
num_file = len(time_stamps_sim)
count = 0
out_data = 0.0
for time in range(file_start, min(file_start+num_file, total_output_num), 1):
    filename = r'./sep_csv/output_'+str(time)+'.csv'
    if count==0:
        out_data = pd.read_csv(filename, skiprows=None, nrows=node_num)
    else:
        out_data += pd.read_csv(filename, skiprows=None, nrows=node_num)
    count+=1
    print(filename)

out_data /= count
out_data.to_csv(r'./1.csv', index=False) 

time_stamps_sim_0 = pd.date_range(start='2016-11-1 00:00:00', end='2017-2-1 00:00:00', freq="6h")
time_stamps_sim = pd.date_range(start='2017-2-1 00:00:00', end='2017-2-28 23:59:59', freq="6h")
num_file = len(time_stamps_sim)
file_start = len(time_stamps_sim_0)
num_file = len(time_stamps_sim)
count = 0
out_data = 0.0
for time in range(file_start, min(file_start+num_file, total_output_num), 1):
    filename = r'./sep_csv/output_'+str(time)+'.csv'
    if count==0:
        out_data = pd.read_csv(filename, skiprows=None, nrows=node_num)
    else:
        out_data += pd.read_csv(filename, skiprows=None, nrows=node_num)
    count+=1
    print(filename)

out_data /= count
out_data.to_csv(r'./2.csv', index=False)

time_stamps_sim_0 = pd.date_range(start='2016-11-1 00:00:00', end='2017-3-1 00:00:00', freq="6h")
time_stamps_sim = pd.date_range(start='2017-3-1 00:00:00', end='2017-3-31 23:59:59', freq="6h")
num_file = len(time_stamps_sim)
file_start = len(time_stamps_sim_0)
num_file = len(time_stamps_sim)
count = 0
out_data = 0.0
for time in range(file_start, min(file_start+num_file, total_output_num), 1):
    filename = r'./sep_csv/output_'+str(time)+'.csv'
    if count==0:
        out_data = pd.read_csv(filename, skiprows=None, nrows=node_num)
    else:
        out_data += pd.read_csv(filename, skiprows=None, nrows=node_num)
    count+=1
    print(filename)

out_data /= count
out_data.to_csv(r'./3.csv', index=False)

time_stamps_sim_0 = pd.date_range(start='2016-11-1 00:00:00', end='2017-4-1 00:00:00', freq="6h")
time_stamps_sim = pd.date_range(start='2017-4-1 00:00:00', end='2017-4-30 23:59:59', freq="6h")
num_file = len(time_stamps_sim)
file_start = len(time_stamps_sim_0)
num_file = len(time_stamps_sim)
count = 0
out_data = 0.0
for time in range(file_start, min(file_start+num_file, total_output_num), 1):
    filename = r'./sep_csv/output_'+str(time)+'.csv'
    if count==0:
        out_data = pd.read_csv(filename, skiprows=None, nrows=node_num)
    else:
        out_data += pd.read_csv(filename, skiprows=None, nrows=node_num)
    count+=1
    print(filename)

out_data /= count
out_data.to_csv(r'./4.csv', index=False)

time_stamps_sim_0 = pd.date_range(start='2016-11-1 00:00:00', end='2017-5-1 00:00:00', freq="6h")
time_stamps_sim = pd.date_range(start='2017-5-1 00:00:00', end='2017-5-31 23:59:59', freq="6h")
num_file = len(time_stamps_sim)
file_start = len(time_stamps_sim_0)
num_file = len(time_stamps_sim)
count = 0
out_data = 0.0
for time in range(file_start, min(file_start+num_file, total_output_num), 1):
    filename = r'./sep_csv/output_'+str(time)+'.csv'
    if count==0:
        out_data = pd.read_csv(filename, skiprows=None, nrows=node_num)
    else:
        out_data += pd.read_csv(filename, skiprows=None, nrows=node_num)
    count+=1
    print(filename)

out_data /= count
out_data.to_csv(r'./5.csv', index=False)