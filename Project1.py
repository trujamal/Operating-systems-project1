import math
import random
#from dataclasses import dataclass


# Project 1
# In this project, we are going to build a discrete-time event
# simulator for a number of CPU schedulers on a single CPU system.
# The goal of this project is to compare and assess the impact of
# different schedulers on different performance metrics, and across multiple workloads.
# @authors: John Daloni, Jamal Rasool, Kristof York, Fernando Valdez, Elliot Esponda
# @date: March 21st, 2019


## GLobal Variables
event_Queue = []

#@dataclass  # Struct Creation
class Process:
	service_time: float
	arrival_time: float
	remaining_time: float
	completion_time: float
	found: bool ## process being found
	how_long_in_queue: float
	preemptive_time: float
	float_initial_wait: float
	process_type: int
	pId: int

def __init__(self, burst,arrivalTime, pType, pId):
	service_time = burst
	arrival_time = arrivalTime
	remaining_time = burst
	completion_time = 0
	found = False  ## process being found
	how_long_in_queue =  0
	preemptive_time = 0
	float_initial_wait: float
	process_type =  pType
	self.pId =  int








class Event:
	time: float
	type: type
	kind: type
	#next_event: Event



#Testing  Changes 2
def schedule_event(type, time, other_val):
	print("Scheduling Event Beings")
	#creates a new event and places it in the event queue based on its time.

	return
# Three parts in the init

def Init_Process():
	clock = 0
	# Generate a list of processes (Arrival times, Service Time)
	End_condition = 0
	# Ready Queue (No proceses within it)
	CPU_idle = True
	# Init Event Queue w/ arrivals.
	return

def get_event():
	return




## START OF MAIN
def main():
	print("GOOGLE IT ELLIOT")

	event_Vector = []




main()


# def process_arrival(event):
# 	# Checking to see if its true
# 	if (CPU_idle == 1):
# 		CPU_idle == 0
# 		schedule_event(dep, event_time + service_time)
# 	else
# 		#Place P in Ready queue
#
# def process_departure(event):
# 	if(readqueue == 0) # Check to see if ready queue is empty
# 		CPU_idle = 1
# 	else
# 		remove_process(from_readqueue)
# 		schedule_event(dep, event_time + s);
#
#
# while (!End_condition):
# 	event = get_event()
# 	clock = event -> time
#
# 	switch(event->type):
# 		case ARR:
# 			# Arrival case call function
# 	process_arrival(event)
# 		case DEP:
# 			# Arrival case call function
# process_depature(event)


import random
import sys
import math

# Using the rand() function
# (that returns a random number uniformly distributed between
# 0 and RANDM AX), write a simple program the generates the arrival
# times of 1000 processes (i.e., when each process arrives) that follow a
# Poisson distribution with an average arrival rate poisson of 10 processes per
# second. Submit the arrival times of the first 10 processes and the actual
# average arrival rate over the 1000 processes. [Hint 1: A Poisson arrivals
# means Exponential inter-arrival times. Hint 2: Use the CDF of Exponential
# Distribution.] [10 pts]

# Initialize array
largerValArr = []
smallerValArr = []
sizeL = 1000
sizeS = 10


# Function for calculating the CDF in which we solve for x
def mathHandler(random_number, lambda_value):
	return -math.log(1 - random_number) / lambda_value


# Run the 10 cases
for i in range(0, sizeS):
	our_randomNumber = float(random.randint(0, sys.maxsize))
	our_randomNumber = our_randomNumber / sys.maxsize
	smallerValArr.append(mathHandler(our_randomNumber, 10))

# Running 1000 cases then taking the average.
for i in range(0, sizeL):
	our_randomNumber = float(random.randint(0, sys.maxsize))
	our_randomNumber = our_randomNumber / sys.maxsize
	largerValArr.append(mathHandler(our_randomNumber, 10))

resultingavg = (sum(largerValArr) / sizeL) * 100

# Formatting
print("Arrival Times")
print
print(smallerValArr)
print
print("Average Arrival Rate")
print
print(resultingavg)
print

print("Program Completed")
