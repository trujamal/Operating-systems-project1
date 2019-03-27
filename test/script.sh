#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./sim 1 $i 0.06 0.01
   cp sim.data /data/1-$i-006.data
done
#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./sim 2 $i 0.06 0.01
   cp sim.data /data/1-$i-006.data
done
#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./sim 3 $i 0.06 0.01
   cp sim.data /data/1-$i-006.data
done
#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./sim 4 $i 0.06 0.01
   cp sim.data /data/1-$i-006.data
done
#!/bin/bash
rm sim.data
for ((i = 1; i < 31; i++)); do
   ./sim 4 $i 0.06 0.2
   cp sim.data /data/1-$i-006.data
done
