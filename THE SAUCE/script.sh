#!/bin/bash
rm results.txt

for ((i = 1; i < 31; i++)); do
   python3 main.py 1 $i 0.06 0
   cp results.txt data/1-$i-006.data
done

for ((i = 1; i < 31; i++)); do
   python3 main.py 2 $i 0.06 0
   cp results.txt data/2-$i-006.data
done

for ((i = 1; i < 31; i++)); do
   python3 main.py 3 $i 0.06 0
   cp results.txt data/3-$i-006.data
done

for ((i = 1; i < 31; i++)); do
   python3 main.py 4 $i 0.06 0.01
   cp results.txt data/4-$i-006-001.data
done

for ((i = 1; i < 31; i++)); do
   python3 main.py 4 $i 0.06 0.2
   cp results.txt data/4-$i-006-02.data
done