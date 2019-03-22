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
Clock = 0.0

# Constants
AVGSERVICETIME: float
SUMSERVICETIME: float
SUMWAITTIME: float
SUMARRIVALTIME: float
ISBUSY: bool
END_CONDITION = 10000 ##  number of Processes that be processsed and stuff to terminate

lambda_value = None
average_service_time = None
processCount = None
quantum_value = None

#@dataclass  # Struct Creation
class Process:
	# service_time: float
	# arrival_time: float
	# remaining_time: float
	# completion_time: float
	# found: bool ## process being found
	# how_long_in_queue: float
	# preemptive_time: float
	# float_initial_wait: float
	# process_type: int
	# pId: int

	# Simmulator Initialization
	def initSimmulator(self):
		Clock = 0
		SUMSERVICETIME = 0
		SUMWAITTIME = 0
		SUMARRIVALTIME = 0
		ISBUSY = False

	
# Process Initialization
	def __init__(self, burst, arrivalTime, pType, processID):
		self.service_time = burst
		self.arrival_time = arrivalTime
		self.remaining_time = burst
		self.completion_time = 0
		self.found = False
		self.how_long_in_queue = 0
		self.preemptive_time = 0
		self.float_initial_wait = 0.0
		self.process_type = pType
		self.pId = processID


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
	sum_arrival_rate = 0
	sum_arrival_rate =  sum_arrival_rate + random_arrival_time

	# New Event Object
	# self, burst,arrivalTime, pType, pId
	event_process = Process(random_service_time, Clock + random_arrival_time, ARRIVAL, (processCount + 1) )
	event_Queue.append(event_process)
	print(event_Queue[0])

# Three parts in the init

def Init_Process():
	Clock = 0
	# Generate a list of processes (Arrival times, Service Time)
	End_condition = 0
	# Ready Queue (No proceses within it)
	CPU_idle = True
	# Init Event Queue w/ arrivals.
	return

def get_event():
	return


def run_Simulator(scheudler):
	proces_Count = 0


	return 0

def First_Come_First_Serve(eventQueue):
	ISBUSY = True;

	## EventQueue w/arrivales;
	counter = 0
	while ( counter < END_CONDITION):
		event = eventQueue.getEvent()
	return


		#ounter+1
# 		event = getEvent();  ## takes first event from ##event queue and /assigns it to event
# 		clock = event -> time;
# 		switch(event -> type)
# 		case
# 		arival:
# 		processArrival(event)
# 	case
# 	Dep:
# 	processDeparture(event)
#
#
# ## Round Robin Time Slice would be part arrival or departure can't remember
#
#
# processArrical(event)
# {
#
# 	If(Cpu_Idle == 1)
# {
# 	cpu_Idle = 0;
# schedule_Event(Departure, EventTime, service
# }
# else
# {
# 	## put P (process in R.Q (Ready Queue) .
# }
# }
#
# processDeparture(event)
# {
# if (R_Q == Empty)
# {
# 	Cpu_Idle = 1;
# }
# else
# {
# 	## remvove process from R.Q
# 	## Schedule event (Dep, Event Time + s
# }
# }


## START OF MAIN

if __name__ == "__main__":
	if len(sys.argv) > 4:
		scheduler = int(sys.argv[1])
		lambda_value = float(sys.argv[2])
		average_service_time = float(sys.argv[3])
		if len(sys.argv) == 5:
			quantum_value = int(sys.argv[4])
			pass
	else:
		# Run -> edit configurations -> arguments
		print("Please type in required arguments.")
		print("1st arg (Pick Scheduler 1-4)")
		print("2nd arg (Avg Arrival Time)")
		print("3rd arg (Avg Service Time)")
		try:
			if sys.argv[1] == '4':
				print("4th arg (Size of Q)")
		except IndexError:
			pass


	randomNumber = generateRandomNumber()
	# schedule_event()
	print("Program Completed")
	event_Vector = []

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