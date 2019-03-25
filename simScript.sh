#!/bin/bash
rm sim.data
for((i = 1; i < 31; i++)); do
    ./sim $1 $i 0.06 0.01
done
if [ $1 == 1 ]; then
    cp sim.data data/FCFS-006.data
fi
if [ $1 == 2 ]; then
    cp sim.data data/SRTF-006.data
fi
if [ $1 == 3 ]; then
    cp sim.data data/HRRN-006.data
fi
if [ $1 == 4 ]; then
    cp sim.data data/RR-006.data
fi



