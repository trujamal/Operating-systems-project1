#!/bin/bash
for ((i = 1; i < 31; i++)); do
   ./main 1 $i 0.06 0.01
done
for ((i = 1; i < 31; i++)); do
   ./main 2 $i 0.06 0.01
done
for ((i = 1; i < 31; i++)); do
   ./main 3 $i 0.06 0.01
done
for ((i = 1; i < 31; i++)); do
   ./main 4 $i 0.06 0.01
done
for ((i = 1; i < 31; i++)); do
   ./main 4 $i 0.06 0.2
done
