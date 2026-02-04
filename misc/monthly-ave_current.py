import xarray as xr
import numpy as np
import pandas as pd
import os

# time_stamps_sim = pd.date_range(start='1991-1-1 00:00:00', end='2020-12-31 00:00:00', freq="1h")
time_stamps_sim = pd.date_range(start='1991-1-1 00:00:00', end='2020-12-31 00:00:00', freq="7d")
# time_stamps_sim = pd.date_range(start='1991-1-1 00:00:00', end='1991-2-28 00:00:00', freq="1h")
# num_file = np.int16(np.floor(len(time_stamps_sim)/(24*3.0)))
num_file = len(time_stamps_sim)
year_start = 1991
year_end = 2020

node_num = 122
file_start = 1

start_timeStamp = pd.Timestamp(1991, 1, 1, 0)
final_monthly_mean = np.zeros([30, 12, node_num])
# for time in range(file_start, file_start+num_file, 1):
for time in range(num_file):
    current_time = start_timeStamp+pd.DateOffset(hours=time*24*7)
    prev_time = current_time+pd.DateOffset(hours=-(24*7))
    if (time>1):
        skiprow_num = 6+1+node_num+(time-1)*(node_num+3+1)*(24*7)+3
    elif (time==1):
        skiprow_num = 6+1+node_num+(time-1)*(node_num+3+1)*(24*7)+3
    else:
        skiprow_num = 6
    out_data = pd.read_csv('./current_thermal_hourly_output/field_output.csv', skiprows=skiprow_num, nrows=node_num, encoding='ISO-8859-1')
    if (current_time.month != prev_time.month or (current_time.year==2020 and current_time.month==12 and current_time.day==31 and current_time.hour==0)):
        # export the old data
        if (current_time.year!=1991 or current_time.month!=1):
            month_ave_container /= month_day_count
            ave_str = r'./current_thermal_hourly_output/ave_7day/'+str(prev_time.year)+"-"+str(prev_time.month)+"_7day.csv"
            month_ave_container.to_csv(ave_str, index=False)
        # do average
        month_day_count = 0
        # month_ave_container = np.zeros(1,node_num)
        month_ave_container = out_data
        month_day_count += 1
    else:
        month_ave_container += out_data
        month_day_count += 1
    print("Finished "+str(current_time))