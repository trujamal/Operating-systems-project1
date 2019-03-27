#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./Project1 1 $i 0.06 0.01
   cp Project1.data /data/1-$i-006.data
done
#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./Project1 2 $i 0.06 0.01
   cp Project1.data /data/1-$i-006.data
done
#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./Project1 3 $i 0.06 0.01
   cp Project1.data /data/1-$i-006.data
done
#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./Project1 4 $i 0.06 0.01
   cp Project1.data /data/1-$i-006.data
done
#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./Project1 4 $i 0.06 0.2
   cp Project1.data /data/1-$i-006.data
done
