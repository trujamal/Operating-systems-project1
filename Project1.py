import random
import sys
import math
#from dataclasses import dataclass


# Project 1
# In this project, we are going to build a discrete-time event
# simulator for a number of CPU schedulers on a single CPU system.
# The goal of this project is to compare and assess the impact of
# different schedulers on different performance metrics, and across multiple workloads.
# @authors: John Daloni, Jamal Rasool, Kristof York, Fernando Valdez, Elliot Esponda
# @date: March 21st, 2019


## Global Variables
event_Queue = []
ARRIVAL = 1
DEPARTURE = 2
QUANTUM = 3
Clock =  0.0
average_service_time = 10  ## Input argu
lambda_value = .5  ## Second Argument from main
sum_arrival_rate = 0
processCount = 0
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


	def __init__(self,burst, arrivalTime, pType, processID):
		service_time = burst
		arrival_time = arrivalTime
		remaining_time = burst
		completion_time = 0
		found = False  ## process being found
		how_long_in_queue =  0
		preemptive_time = 0
		float_initial_wait = 0.0
		process_type =  pType
		pId = processID

class Event:
	time: float
	type: type
	kind: type
	#next_event: Event


def generateExp(chickenLambda):
	x = 0
	while(x == 0):
		random_Number = generateRandomNumber()
		x = (-1/chickenLambda)*math.log(random_Number)
	return x


def generateRandomNumber():
	our_randomNumber = float(random.randint(0, sys.maxsize))
	our_randomNumber = our_randomNumber / sys.maxsize
	return our_randomNumber

#Testing  Changes 2
def schedule_event():
	print("Scheduling Event Beings")  # creates a new event and places it in the event queue based on its time.
	random_service_time = generateExp(1 / average_service_time)
	random_arrival_time = generateExp(lambda_value)

	sum_arrival_rate =+ random_arrival_time

	# New Event Object
	# self, burst,arrivalTime, pType, pId

	chicken_deluxe = Process(random_service_time, (Clock + random_arrival_time), ARRIVAL, processCount+1)

	event_Queue.append(chicken_deluxe)






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
	randomNumber = generateRandomNumber()
	schedule_event()




	print("Program Completed")





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