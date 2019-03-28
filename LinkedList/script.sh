#!/bin/bash
for ((i = 1; i < 31; i++)); do
   ./project_one_simmulator 1 $i 0.06 0.01
done
for ((i = 1; i < 31; i++)); do
   ./project_one_simmulator 2 $i 0.06 0.01
done
for ((i = 1; i < 31; i++)); do
   ./project_one_simmulator 3 $i 0.06 0.01
done
for ((i = 1; i < 31; i++)); do
   ./project_one_simmulator 4 $i 0.06 0.01
done
for ((i = 1; i < 31; i++)); do
   ./project_one_simmulator 4 $i 0.06 0.2
done