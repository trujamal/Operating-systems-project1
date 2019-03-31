#!/bin/bash

#for ((i = 1; i < 31; i++)); do
#python3 thisistheoneipromise.py 1 $i 0.06 0
#done

#for ((i = 1; i < 31; i++)); do
#python3 thisistheoneipromise.py 2 $i 0.06 0
#done

#for ((i = 1; i < 31; i++)); do
#python3 thisistheoneipromise.py 3 $i 0.06 0
#done

for ((i = 1; i < 31; i++)); do
python3 thisistheoneipromise.py 4 $i 0.06 0.01
done

for ((i = 1; i < 31; i++)); do
python3 thisistheoneipromise.py 4 $i 0.06 0.2
done
