#!/bin/bash
#PBS -V
#PBS -S /bin/bash
#PBS -l nodes=1:ppn=2:gpus=1:titan
#PBS -l walltime=40:00:00
#PBS -l mem=16GB
#PBS -N rfnbusriocaffe
#PBS -M rfn216@nyu.edu
 
module purge
module load caffe/intel/20150115
RUNDIR=$SCRATCH/test/run-${PBS_JOBID/.*}
mkdir -p $RUNDIR
#DATADIR=$SCRATCH/my_project/data
cd $RUNDIR

caffe.bin train -gpu 0 -weights=/work/rfn216/bus_rio/busrio7_iter_2000000.caffemodel -solver=/home/rfn216/BusRio/solver8.prototxt > out.log 2>&1

exit
