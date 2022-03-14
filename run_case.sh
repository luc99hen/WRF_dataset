#!/bin/bash

set -ex

HOST_PATH="/wrf/host"
RUN_PATH="/wrf/WRF/run"
start_month=${START_M:-01}
start_day=${START_D:-01}
end_month=${END_M:-01}
end_day=${END_D:-02}

# generate namelist.input
cd /wrf
sed -i "s/\$start_month/${start_month}/" ./namelist.input
sed -i "s/\$start_day/${start_day}/" ./namelist.input
sed -i "s/\$end_month/${end_month}/" ./namelist.input
sed -i "s/\$end_day/${end_day}/" ./namelist.input
cp ./namelist.input $RUN_PATH

# prepare input files (assume running for 1 day)
ln -sf "${HOST_PATH}/WPS_Output/met_em.d01.2021-${start_month}-${start_day}"* "${RUN_PATH}/"
ln -sf "${HOST_PATH}/WPS_Output/met_em.d01.2021-${end_month}-${end_day}_00:00:00.nc" "${RUN_PATH}/"

cd $RUN_PATH
# run ./real.exe
./real.exe

# run ./wrf.exe
mpirun --allow-run-as-root -n 4 wrf.exe

# collect output results
rm "wrfout_d01_2021-${start_month}-${start_day}_00:00:00" # abandon the first output (empty)
mkdir $HOST_PATH/WRF_Output/"${start_month}_${start_day}"
mv wrfout* $HOST_PATH/WRF_Output/"${start_month}_${start_day}"

# process output
cd $HOST_PATH
/usr/bin/python3 process_out.py
rm -rf $HOST_PATH/WRF_Output/"${start_month}_${start_day}"
