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
		while count != self.__end_condition:
			head_event = self.events.event_Queue[count]  # getting next event
			try:


				if (head_event['arrival_time'] >= self.__clock): # put in ready que
					self.processArrival(self.readyQ, head_event)
				elif (not self.checkifbusy() and self.readyQ.readyQ[0]["process_status"] != None ):
					self.processArrival(self.readyQ, head_event)

			#put this in try catch
			#to avoid index errors if readyyq is empty and system is idle

				if (self.readyQ.readyQ[count]['process_status'] == 'departed'):
					self.processDeparture(self.readyQ, head_event)
					print ('pros dep')
				elif (self.readyQ.readyQ[0]['process_status'] == 'arrived'):
					self.processDeparture(self.readyQ, head_event)
					print('pros arrival')



				print ( str(self.__clock) + (str(self.readyQ.readyQ[count])) + '\n')
			except IndexError:
				print (str(count) + '\n')
				pass
			count = count + 1



	def srtf(self):
		count = 0
		while count != self.__end_condition:
			pass

	def hrrn(self):
		pass
		# count = 0
		# __event_Queue_Size = len(self.events.event_Queue)

		# while count != self.__end_condition:

		# 	if self.events.event_Queue[count]['process_status'] == 'arrived':
		# 		self.readyQ.scheduleEvent(self.events['process_status'], self.events, self.events['service_time'])
		# 		if self.__is_busy == False:
		# 			self.__is_busy = True
		# 			self.events.event_Queue[count]['process_status'] = 'departed'
		# 			self.events.event_Queue[count]['arrival_time'] = self.__clock + self.events.event_Queue[count][
		# 				'service_time']
		# 		else:
		# 			self.events.event_Queue.pop(0)
		# 	# self.readyQ.erase(self)

		# 	if self.events.event_Queue[count]['process_status'] == 'departed':
		# 		__priority_Level = float(0)
		# 		count = count + 1
		# 		pass

	def rr(self):
		count = 0
		while count != self.__end_condition:
			pass

	def processArrival(self, readyQ, event):
		self.__clock = event['arrival_time']  # setting the clock

		if (self.checkifbusy()):
			readyQ.scheduleEvent('arrived', event, self.__clock)
		else:
			event["completion_time"] = self.__clock + event['remaining_time']
			self.__CPU = copy.deepcopy(event)

			readyQ.scheduleEvent('departed', event, self.__clock)

		

		# readyQ.scheduleEvent('arrival', event, time)  # used to keep 1 arrival coming into the ready queue

	def processDeparture(self, readyQ, event):
		self.__clock = self.__clock + event['remaining_time'] # setting the clock

		if event['completion_time'] > 0:
			self.__CPU = None
		else:
			readyQ.scheduleEvent('arrived', event, self.__clock)

		self.readyQ.removeEvent(event)
		



	def checkifbusy(self):
		return (self.__CPU != None) #returns true if busy



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

	def eventArrival(self, service_time, arrival_time, process_count):
		return {
			'pId': process_count,
			'service_time': service_time,
			'arrival_time': arrival_time,
			'remaining_time': service_time,
			'completion_time': 0,
			'found': False,
			'how_long_in_queue': None,
			'preemptive_time': None,
			'float_initial_wait': None,
			'process_status': 'arrived'
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
		self.readyQ.sort(key=lambda k: k['arrival_time'])

	def scheduleEvent(self, Event_type, event, time):

		# Generate random service time and arrival time
		# random_service_time = generateExp(1 / average_service_time)
		# random_arrival_time = generateExp(lambda_value)
		# self.__sum_arrival_time = self.__sum_arrival_time + random_service_time

		event['process_status'] = Event_type

		if scheduler == 1:
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
