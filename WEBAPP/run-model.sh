#!/usr/bin/sh

# usage ./run.sh /sim/sample-model/ example
RAS_LIB_PATH=/ras/libs:/ras/libs/mkl:/ras/libs/rhel_8
export LD_LIBRARY_PATH=$RAS_LIB_PATH:$LD_LIBRARY_PATH
echo $LD_LIBRARY_PATH

RAS_EXE_PATH=/ras/v61
export PATH=$RAS_EXE_PATH:$PATH
echo $PATH

#delete old p01 hdf results and copy in fixed up one 
rm example.p01.hdf
rm example.p01.tmp.hdf
cp wrk_source/example.p01.tmp.hdf .

# remove old results
rm example.dss

RasUnsteady example.c01 b01

mv example.p01.tmp.hdf example.p01.hdf