import math
import random
from dataclasses import dataclass


# Project 1
# In this project, we are going to build a discrete-time event
# simulator for a number of CPU schedulers on a single CPU system.
# The goal of this project is to compare and assess the impact of
# different schedulers on different performance metrics, and across multiple workloads.
# @authors: John Daloni, Jamal Rasool, Kristof York, Fernando Valdez, Elliot Esponda
# @date: March 21st, 2019


@dataclass  # Struct Creation
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





class Event(object):
	pass


class Event:
	time: float
	type: type
	kind: type
	next_event: Event



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
