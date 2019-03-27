import sys
from Simulator import Simulator


def main():
    if len(sys.argv) <= 5:
        scheduler = int(sys.argv[1])
        the_lambda = float(sys.argv[2])
        average_service_time = float(sys.argv[3])
        if len(sys.argv) == 5:
            quantum = int(sys.argv[4])
        else:
            quantum = 0
    end_condition = 10000

    sim = Simulator(scheduler, the_lambda, average_service_time, quantum, end_condition)

    sim.run()
    sim.generateReport()




if __name__ == "__main__":
    main()


"""

number_of_processes = 0
end_condition = 0
sum_of_arrival_times = 0.0
clock = 0
i = 0

process = createProcess()

while i < number_of_processes:
    if i == 0:
        y = float(random.uniform(0, 1))

#this will hold the interval between arrivals
arrival_times = []
#this will holds how the service length of each arrival
service_times = []
#this holds the time when the next arrival occurs in the queue
arrival_times_on_clock = []
#this holds the departure time of each process
departure_times = []

#the ready queue
event_queue = deque()

#generate an arrival 1 by 1
#4 y metrics: CPU utilization, turn around time, queue size, throughput
#x axis is 1-30 lambda
#Ts = .06 => mew = 16.666

#get the arrival times and place them in list
for i in range(0, number_of_processes):
    y = float(random.uniform(0, 1))
    arrival_times.append(math.log(1 - y)/(-my_lambda))

#get service length and place in list
for i in range(0, number_of_processes):
    y = float(random.uniform(0, 1))
    service_times.append(math.log(1 - y)/(-my_service))

#find the next time an arrival shows up to the ready queue
arrival_times_on_clock.append(arrival_times[0])
for i in range(1, number_of_processes):
    arrival_times_on_clock.append(arrival_times[i] + arrival_times_on_clock[i-1])

#find the next departure of the ready queue
for i in range(0, number_of_processes):
    departure_times.append(arrival_times_on_clock[i] + service_times[i])



#The next function will search through both lists that hold when the next arrival occurs in the ready queue
#as well as when the next departure occurs.

#It will insert the next event (either a departure or arrival) and insert it respectively, as well as give a label
#to what type of event it was
i = 0
j = 0
finished = False
counter = 0

while i < number_of_processes and j < number_of_processes:
    event = Event()
    if float(arrival_times_on_clock[i]) < float(departure_times[j]):
        
        process_arrival(time_now) {
            if(cpu_idle)
               schedule_event(departure)
            else
               put in ready queue (processes that are waiting for CPU to be free)
            
            schedule_new_event(ARR) (schedule your next arrival)
        }
 
        event.event_time = arrival_times_on_clock[i]
        event.event_type = "ARR"
        event_queue.insert(counter, event)
        i += 1
        counter += 1
    else:
        event.event_time = departure_times[j]
        event.event_type = "DEP"
        event_queue.insert(counter, event)
        j += 1
        counter += 1

    if(i < j):
        print("More Departures than Arrivals")

for i in range(0, len(event_queue)):
    print(event_queue[i].event_type)


number_in_ready_queue = 0
for i in range(0, len(event_queue)):
    if(event_queue[i].event_type == "ARR"):
        number_in_ready_queue += 1
    else:
        number_in_ready_queue -= 1

    if(i == 1000 or i == 2000 or i == 3000 or i == 4000 or i == 5000 or i == 6000 or i == 7000 or i == 8000 or i == 9000 or i == 10000):
        print(number_in_ready_queue)

#The initialization should be completed at this point


"""





