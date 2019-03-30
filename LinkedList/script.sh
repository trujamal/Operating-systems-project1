#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./project1 1 $i 0.06 0.01
   cp sim.data /data/1-$i-006.data
done
for ((i = 1; i < 31; i++)); do
   ./project1 2 $i 0.06 0.01
   cp sim.data /data/1-$i-006.data
done
for ((i = 1; i < 31; i++)); do
   ./project1 3 $i 0.06 0.01
   cp sim.data /data/1-$i-006.data
done
for ((i = 1; i < 31; i++)); do
   ./project1 4 $i 0.06 0.01
   cp sim.data /data/1-$i-006.data
done
for ((i = 1; i < 31; i++)); do
   ./project1 4 $i 0.06 0.2
   cp sim.data /data/1-$i-006.data
done
