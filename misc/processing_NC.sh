#!/bin/bash
for t in $(seq 2016 1 2017)
do
	f1="${t}/*"
	f2="${t}_merged.nc"
# 	f2="out-u-${t}"
# 	paste $f1 $f2 > "out-comb-${t}"
# 	cp $f1 ./half-month/$f1
	cp $f1 ./monthly/$f1
	cdo merge $f1 $f2
done 

cdo mergetime *_*.nc merged.nc

cdo -outputtab,date,time,value -fldmean -selname,t2m merged.nc > ./t2m.csv
cdo -outputtab,date,time,value -fldmean -selname,ssrd merged.nc > ./ssrd.csv
