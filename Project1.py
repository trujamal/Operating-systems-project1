import random
import sys
import math
import copy


# Project 1
# In this project, we are going to build a discrete-time event
# simulator for a number of CPU schedulers on a single CPU system.
# The goal of this project is to compare and assess the impact of
# different schedulers on different performance metrics, and across multiple workloads.
# @authors: John Daloni, Jamal Rasool, Kristof York, Fernando Valdes, Elliot Esponda
# @date: March 21st, 2019

#####################################################################################

class Simmulator:
	# Simmulator Initialization
	def __init__(self, scheduler, lambda_value, average_service_time, quantum_value):
		self.__clock = 0
		self.__sum_service_time = 0
		self.__sum_wait_time = 0
		self.__sum_arrival_time = 0
		self.__is_busy = False
		self.__scheduler = scheduler
		self.__quantum_value = quantum_value
		self.__end_condition = 10

		self.events = Event()
		self.events.createEvents(lambda_value, average_service_time, self.__clock, self.__end_condition)

		self.readyQ = ReadyQueue()

		self.__CPU = None

	def run(self):
		# print (self.events.event_Queue)

		if scheduler == 1:
			# First Come First Serve
			self.fcfs()  # @todo fully implement this function
		elif scheduler == 2:
			self.srtf()  # @todo fully implement this function
			pass
		elif scheduler == 3:
			self.hrrn()  # @todo fully implement this function
			pass
		elif scheduler == 4:
			self.rr()  # @todo fully implement this function
			pass
		else:
			print('bad args')

	def fcfs(self):

		self.events.event_Queue.sort(key=lambda k: k['arrival_time'])
		count = 0
		head_event = self.events.event_Queue[count]
		are_we_done = 0
		while are_we_done != self.__end_condition:  # getting next event
			try:
				head_event = self.events.event_Queue[count]

				if (head_event['arrival_time'] >= self.__clock and self.__is_busy == False): # put in ready que
					print("PID " + str(head_event['pId']))
					self.processArrival(self.readyQ, head_event)
					are_we_done = are_we_done + 1 
					print("Faster than clock ")
					
				elif (self.__is_busy == False):
					print("PID " + str(head_event['pId']))
					self.processArrival(self.readyQ, head_event)
					are_we_done = are_we_done + 1 
					print('Slower than clock and CPU not busy')

				elif (self.readyQ.readyQ[0]['process_status'] == 'departed' and self.__is_busy == True):
					count = count + 1
					print("PID " + str(head_event['pId']))
					self.processDeparture(self.readyQ, head_event)
					are_we_done = are_we_done + 1
					print('Farewell, Fernando')

			# print(str(self.__clock) + (str(self.readyQ.readyQ[0])) + '\n')
			except IndexError:
				print('index error: ' + str(count) + '\n')
				pass




	def srtf(self): #195
		self.events.event_Queue.sort(key=lambda k: k['arrival_time'])
		count = 0
		head_event = self.events.event_Queue[0]
		are_we_done = 0
		while are_we_done != self.__end_condition:

			if(not self.readyQ.readyQ and self.__is_busy == False): #if ready queue is empty cpu not bust
				self.processArrival(self.readyQ, head_event) # put in Cpu
				self.__clock = head_event['arrival_time']
				self.__CPU = copy.deepcopy(head_event)
				self.__is_busy = True
				self.__CPU['cpu_arrival_time'] = self.__clock
				self.__CPU['process_status'] = 'running'
				count = count + 1
				head_event = self.events.event_Queue[count]
				are_we_done = are_we_done + 1
			if(not self.readyQ.readyQ and self.__is_busy == True):
				# check ready Q.readyQ if an error
				self.readyQ.readyQ.append(head_event)
				if (head_event['remaining_time'] == head_event['service_time']): ## First time being processed
					self.__clock = head_event['arrival_time']
					self.__CPU['remaining_time'] =  self.__CPU['remaining_time'] - self.__clock
				else:
					self.__clock = 0
					self.__CPU['remaining_time'] = 0 ## Calculate this
				temp = copy.deepcopy(self.__CPU)
				self.readyQ.readyQ.append(temp)
				self.__CPU = None
				self.__is_busy = False
				self.readyQ.sortQ()
				self.__CPU = copy.deepcopy(self.readyQ.readyQ[0])
				self.__CPU['cpu_arrival_time'] = 0 # figure this out
				self.__is_busy = True
				del self.readyQ.readyQ[0]


				## cpu is busy and ready Queue empty
				# put incoming event into ready queue

				# Take Event from CPU and add it to ready queue, and then sort ready queue
				# readyqueue[0] goes into cpu.

				self.processArrival(self.readyQ, head_event) ## put in ready Queue
				count = count + 1
				head_event = self.events.event_Queue[count]
				are_we_done = are_we_done + 1
			if (self.readyQ.readyQ and self.__is_busy == True):
				## check ready queue and Cpu and put in cpu srtf and put order ready queue

				self.processArrival(self.readyQ, head_event) ## put in CPU
				self.processArrival(self.readyQ, head_event) ## Put in Ready Queue

				# ready queue parameter might be wrong

			
			
















			# print("PID Arrival " + str(head_event['pId']) + ' ' + str(head_event['remaining_time']))
			# self.processArrival(self.readyQ, head_event)
			# self.readyQ.sortQ()


			# if(head_event['remaining_time'] < shortest_event['remaining_time']):
			# 	print("PID departure " + str(head_event['pId']) + str(head_event['remaining_time']))
			# 	self.processDeparture(self.readyQ,head_event)
			# 	print("PID Arrival After Departure" + str(shortest_event['pId']) + str(head_event['remaining_time']))
			# 	self.processArrival(self.readyQ, shortest_event)
			# 	are_we_done = are_we_done + 1
			# 	count = count + 1
			# else:
			# 	print("Hitting Else")



			#Set clock
			#sort remaining time of events.
			#take event[0] from Event Queue and put in Reeady queue
			#update remaining times of EventQueue
			# resort remaining times,
			#process arrival from event [0] from event queue.

			count = count + 1



			pass

	def hrrn(self):

		#  shortest response time first w (waiting time)+s(service time) / (service time)
		self.events.event_Queue.sort(key=lambda k: k['arrival_time'])
		count = 0
		head_event = self.events.event_Queue[count]
		are_we_done = 0

		for i in range(0, len(self.events.event_Queue)):
			print(self.events.event_Queue[i]['pId'])
			print(self.events.event_Queue[i]['arrival_time'])
			print(self.events.event_Queue[i]['service_time'])

		while are_we_done != self.__end_condition:  # getting next event
			try:
				head_event = self.events.event_Queue[count]
				if (head_event['ratio'] >= self.__sum_wait_time and self.__is_busy == False):  # put in ready que
					print("PID " + str(head_event['pId']))
					self.processArrival(self.readyQ, head_event)
					are_we_done = are_we_done + 1
					self.__sum_wait_time = self.__sum_wait_time + self.__clock  # This is to help get the ratio wait time.
					print("HRRN- Faster than clock ")

				elif (self.__is_busy == False):
					print("PID " + str(head_event['pId']))
					self.processArrival(self.readyQ, head_event)
					are_we_done = are_we_done + 1
					self.__sum_wait_time = self.__sum_wait_time + self.__clock  # This is to help get the ratio wait time.
					print('HRRN- Slower than clock and CPU not busy')

				elif (self.readyQ.readyQ[0]['process_status'] == 'departed' and self.__is_busy == True):
					count = count + 1
					print("PID " + str(head_event['pId']))
					self.processDeparture(self.readyQ, head_event)
					are_we_done = are_we_done + 1
					self.__sum_wait_time = self.__sum_wait_time + self.__clock  # This is to help get the ratio wait time.
					print('HRRN- Farewell, Fernando')

				# print(str(self.__clock) + (str(self.readyQ.readyQ[0])) + '\n')
				pass
			except IndexError:
				print('index error: ' + str(count) + '\n')
			pass

	def rr(self):
		self.events.event_Queue.sort(key=lambda k: k['remaining_time'])
		count = 0
		head_event = self.events.event_Queue[count]
		are_we_done = 0
		while count != self.__end_condition:
			pass

	def processArrival(self, readyQ, event):
		self.__clock = event['arrival_time']  # setting the clock

		# FCFS
		if scheduler == 1:
			if not self.__is_busy:
				self.__is_busy = True
				self.__CPU = copy.deepcopy(event)
				readyQ.scheduleEvent('departed', event, self.__clock)
			else:
				readyQ.scheduleEvent('arrived', event, self.__clock)

		# SRTF --Temporary Code for the basis run to work
		if scheduler == 2:
			if (self.__is_busy == False): # if there is no line, go straight in
				readyQ.scheduleEvent('departed', event, self.__clock)
			else:
				# if its busy it will get interrupted
				readyQ.scheduleEvent('arrived', event, self.__clock) #put process in the queue
				self.processDeparture(self.readyQ, self.__CPU) # take process out of the cpu and into the queue
				readyQ.sortQ() #srtf is at index [0] in readyQ
				
				self.__is_busy = True
				self.__CPU = copy.deepcopy(readyQ[0]) # put srtf in the cpu
				readyQ[0]['cpu_arrival_time'] = self.__clock
				readyQ.scheduleEvent('departed', readyQ[0], self.__clock) #schedule when it finishes

		# HRRN
		if scheduler == 3:
			if not self.__is_busy:
				self.__is_busy = True
				self.__CPU = copy.deepcopy(event)
				readyQ.scheduleEvent('departed', event, self.__clock)
			else:
				readyQ.scheduleEvent('arrived', event, self.__clock)

		# RR --Temporary Code for the basis run to work
		if scheduler == 4:
			if not self.__is_busy:
				self.__is_busy = True
				self.__CPU = copy.deepcopy(event)
				readyQ.scheduleEvent('departed', event, self.__clock)
			else:
				readyQ.scheduleEvent('arrived', event, self.__clock)

		# readyQ.scheduleEvent('arrival', event, time)  # used to keep 1 arrival coming into the ready queue

	def processDeparture(self, readyQ, event):

		# FCFS
		if scheduler == 1:
			self.__clock = self.__clock + event['remaining_time']

			event['completion_time'] = self.__clock
			self.readyQ.removeEvent(event)
			self.__is_busy = False
			self.__CPU = None

		# SRTF @todo
		if scheduler == 2:
			if(event['remaining_time'] == event['service_time']): ## First time it a process is processed
				event['remaining_time'] = event['remaining_time'] -  event['cpu_arrival_time']
			else:
				event['remaining_time'] = event['remaining_time'] - (self.__clock + event['cpu_arrival_time'])
			if event['remaining_time'] == 0: # if the process is done 
				self.readyQ.removeEvent(event)
				# event['completion_time'] = self.__clock
			else: 
				readyQ.scheduleEvent('arrived', event, self.__clock)
			self.__is_busy = False
			self.__CPU = None


		# HRRN
		if scheduler == 3:
			event['waiting_time'] = self.__clock - event['arrival_time']
			event['completion_time'] = self.__clock
			self.hrrnRatio(self.readyQ.readyQ)
			self.readyQ.removeEvent(event)
			self.__is_busy = False
			self.__CPU = None

		# RR @todo
		if scheduler == 4:
			pass

	def hrrnRatio(self, ready_queue):
		for event in ready_queue:
			event['ratio'] = (event['waiting_time'] + event['service_time']) / event['service_time']
		self.events.event_Queue.sort(key=lambda k: k['ratio'],
		                             reverse=True)  # Not sorting the queue or updating it with useful info

#####################################################################################

class Event:

	def __init__(self):
		self.event_Queue = []

	def createEvents(self, lambda_value, average_service_time, clock, end_condition):
		print("Scheduling Event Beings")  # creates a new event and places it in the event queue based on its time.

		for process_count in range(end_condition):
			random_service_time = generateExp(1 / average_service_time)
			random_arrival_time = generateExp(lambda_value)
			self.event_Queue.append(
				self.eventArrival(random_service_time, clock + random_arrival_time, process_count + 1, ))

	# Generate random service time and arrival time
	# random_service_time = generateExp(1 / average_service_time)
	# random_arrival_time = generateExp(lambda_value)
	# self.__sum_arrival_time = self.__sum_arrival_time + random_service_time

	def eventArrival(self, service_time, arrival_time, process_count):
		return {
			'pId': process_count,
			'service_time': service_time,
			'arrival_time': arrival_time,
			'remaining_time': service_time,
			'completion_time': 0,
			'found': False,
			'waiting_time': 0,
			'preemptive_time': None,
			'float_initial_wait': None,
			'process_status': 'arrived',
			'ratio': 0,
			'cpu_arrival_time' : 0
		}


#####################################################################################
class ReadyQueue:

	def __init__(self):
		self.readyQ = []

	def isempty(self):
		return (len(self.readyQ) == 0)

	def front(self):
		return next(iter(self.readyQ), None)
	
	def sortQ(self): # sorts the readyQ 
		if scheduler == 1:
			self.readyQ.sort(key=lambda k: k['arrival_time'])
		elif scheduler == 2:
			self.readyQ.sort(key=lambda k: k['remaining_time'])

	def scheduleEvent(self, Event_type, event, time):

		# Generate random service time and arrival time
		# random_service_time = generateExp(1 / average_service_time)
		# random_arrival_time = generateExp(lambda_value)
		# self.__sum_arrival_time = self.__sum_arrival_time + random_service_time

		event['process_status'] = Event_type

		# FCFS
		if scheduler == 1:
			if Event_type == 'departed':
				event['completion_time'] = time + event['service_time']

		# SRTF
		if scheduler == 2:
			if Event_type == 'departed':
				pass
				# event['remaining_time'] = event['remaining_time'] - time
				# event['remaining_time'] = event['service_time'] - time
				# brain = on()

		# HRRN
		if scheduler == 3:
			if Event_type == 'departed':
				event['completion_time'] = time + event[
					'service_time']  # Want to implement it to where it does the ratio response here

		# RR
		if scheduler == 4:
			if Event_type == 'departed':
				event['completion_time'] = time + event['service_time']

		newEvent = copy.deepcopy(event)
		self.readyQ.append(newEvent)
		self.sortQ()

	def removeEvent(self, event):
		del self.readyQ[0]
		self.sortQ()


#####################################################################################

def generateExp(chickenLambda):
	x = 0
	while (x == 0):
		random_Number = generateRandomNumber()
		x = (-1 / chickenLambda) * math.log(random_Number)
	return x


def generateRandomNumber():
	our_randomNumber = float(random.randint(0, sys.maxsize))
	our_randomNumber = our_randomNumber / sys.maxsize
	return our_randomNumber


#####################################################################################


#####################################################################################
## START OF MAIN
if __name__ == "__main__":
	if len(sys.argv) >= 4:
		scheduler = int(sys.argv[1])
		lambda_value = float(sys.argv[2])
		average_service_time = float(sys.argv[3])
		if len(sys.argv) == 5:
			quantum_value = int(sys.argv[4])
		else:
			quantum_value = None
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

	sim = Simmulator(scheduler, lambda_value, average_service_time, quantum_value)
	sim.run()

	print("Program Completed")

#####################################################################################
