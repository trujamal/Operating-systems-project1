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
		self.__end_condition = 10000

		self.__lambda_val = lambda_value
		self.__average_service_time = average_service_time
		self.__quantum_value = quantum_value

		self.events = Event()
		self.readyQ = ReadyQueue()
		self.count = 0

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

	def generate_report(self):

		# scheduler_value: str

		if scheduler == 1:
			scheduler_value = "FCFS()"
		elif scheduler == 2:
			scheduler_value = "SRTF()"
		elif scheduler == 3:
			scheduler_value = "HRRN()"
		elif scheduler == 4:
			scheduler_value = "RR()"

		average_turn_around_time = self.getAvgTurnaroundTime()
		total_throughput = self.getTotalThroughput()
		cpu_utilization = self.getCpuUtil()
		average_process_in_queue = self.getAvgNumProccessInQueue()

		# Change file name as needed:
		with open("Output.txt", "w+") as data_file:
			print("Output is writing to: ", data_file.name)

			if lambda_value == 10:
				data_file.write("Scheduler\tLambda\t\tAvgST\tAvgTA\tTotalTP\tCPU Util\tAvg#ProcsInQ \tQuantum\n")
				data_file.write(
					"------------------------------------------------------------------------------------------------------------------------\n")

			data_file.write(scheduler_value + str("\t\t"))
			data_file.write(str(lambda_value) + str("\t\t"))
			data_file.write(str(average_service_time) + str("\t\t"))
			data_file.write(str(average_turn_around_time) + str("\t"))
			data_file.write(str(total_throughput) + str("\t"))
			data_file.write(str(cpu_utilization) + str("\t\t\t"))
			data_file.write(str(average_process_in_queue) + str("\t\t\t\t"))
			if scheduler == 4:
				data_file.write(str(quantum_value) + str("\n"))
			else:
				data_file.write("0")

		print("Program Completed")
		pass

	# metric computation functions @todo implement functions
	def getAvgTurnaroundTime(self):
		ta = 0
		for ev in self.events.event_Queue:
			ta = ta + ev['arrival_time'] - ev['completion_time'] 
			# print (ev['completion_time'])		
		return round(ta / self.__end_condition, 3)



	def getTotalThroughput(self):
		return round(self.count / self.__clock, 3)

	def getCpuUtil(self):
		# busy time / total time
		busy_time = 0
		for ev in self.events.event_Queue:
			busy_time = busy_time + ev['service_time']
		return round(busy_time / self.__clock, 3)

	def getAvgNumProccessInQueue(self):

		return  # self.

	#  Scheduling Algorithms

	def fcfs(self):
		self.numInQueue = 0
		self.events.event_Queue.sort(key=lambda k: k['arrival_time'])
		self.count = 0
		are_we_done = 0
		self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock, self.__end_condition,
		                         are_we_done)
		while self.count != self.__end_condition:  # getting next event
			try:
				head_event = self.events.event_Queue[self.count]

				#if cpu is not busy
				if (self.__is_busy == False):
					self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock, self.__end_condition, are_we_done)
				
					if (len(self.readyQ.readyQ)):
						self.schedArrival(self.readyQ, head_event)
			
				#cpu not busy
				else:
					self.schedDeparture(self.readyQ, self.readyQ.readyQ[0])

				#anycase - handle next event
				if head_event[type] == 1: #arrival
					self.processArrival(self.readyQ, head_event)
					self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,
					                         self.__end_condition, are_we_done)

				# 	if (head_event['arrival_time'] >= self.__clock):  # put in ready que
				# 		are_we_done = are_we_done + 1						

				# else:
				# 	if (self.readyQ.readyQ[0]['process_status'] == 'departed'):
				# 		self.count = self.count + 1
				# 		self.processDeparture(self.readyQ, self.readyQ.readyQ[0])
				# 		# are_we_done = are_we_done + 1 

				# self.numInQueue = self.numInQueue + len(self.readyQ.readyQ)

			except IndexError:
				print('index error: ' + str(self.count) + '\n')
				pass

		# while are_we_done != self.__end_condition:  # getting next event
		# 	try:
		# 		head_event = self.events.event_Queue[self.count]

		# 		if (self.__is_busy == False):
		# 			if (head_event['arrival_time'] >= self.__clock):  # put in ready que
		# 				are_we_done = are_we_done + 1						
		# 			self.processArrival(self.readyQ, head_event)
		# 			self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock, self.__end_condition, are_we_done)

		# 		else:
		# 			if (self.readyQ.readyQ[0]['process_status'] == 'departed'):
		# 				self.count = self.count + 1
		# 				self.processDeparture(self.readyQ, self.readyQ.readyQ[0])
		# 				# are_we_done = are_we_done + 1 

		# 		self.numInQueue = self.numInQueue + len(self.readyQ.readyQ)

		# 	except IndexError:
		# 		print('index error: ' + str(self.count) + '\n')
		# 		pass


	def srtf(self):  # 195
		self.events.event_Queue.sort(key=lambda k: k['arrival_time'])
		self.count = 0
		self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock, self.__end_condition,
		                         self.count)
		head_event = self.events.event_Queue[self.count]
		while self.count != self.__end_condition:
			## If Ready Q is empty and the CPU is Idle
			if (not self.readyQ.readyQ and self.__is_busy == False):
				self.readyQ.readyQ.append(copy.deepcopy(head_event))

				# sets the clock to the head event ( the first event in the event Queue)
				self.__clock = head_event['arrival_time']
				# put the first event from the event queue, ( head event) in the cpu and make it busy.
				self.__CPU = copy.deepcopy(head_event)
				self.__is_busy = True
				# The cpu arrival time of the head event will meow be equal to the clock beacuse it was first event.
				self.__CPU['cpu_arrival_time'] = self.__clock
				# Make sure you remove the event from the ready Q  Process Departure does this I beleive, will clean up later.
				del self.readyQ.readyQ[0]

				self.count = self.count + 1
				self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,
				                         self.__end_condition, self.count)
				head_event = self.events.event_Queue[self.count]
				continue

			#  ## Something in Cpu and nothing in Ready Queue
			if (not self.readyQ.readyQ and self.__is_busy == True):
				self.appendToReadyQ(head_event)
				# First time an event is coming from the event queue and checking the ready q and cpu is busy
				if (self.readyQ.readyQ[0]['remaining_time'] == self.readyQ.readyQ[0]['service_time']):
					# This would be correct becasue its' the first time
					self.__clock = head_event['arrival_time']

					# the current clock set above was the last process that was in there if you subtract that from the arrival time you
					# get the processing time.
					self.__CPU['cpu_processing_time'] = self.__clock - self.__CPU['cpu_arrival_time']
					# this is then uused to figure out remaining time. Checked out white board should be good.
					self.__CPU['remaining_time'] = self.__CPU['remaining_time'] - self.__CPU['cpu_processing_time']

					if (self.__CPU['remaining_time'] <= 0):
						self.__CPU['completion_time'] = self.__CPU['cpu_processing_time'] - self.__CPU[
							'cpu_arrival_time']
						self.changeCPUprocess()
						del self.readyQ.readyQ[0]
						self.count = self.count + 1
						self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,
						                         self.__end_condition, self.count)
						head_event = self.events.event_Queue[self.count]
						continue
					else:
						head_event = self.events.event_Queue[self.count]  ## Check this When shit breaks
						self.appendToReadyQ(self.__CPU)
						# The event that is first should be the shortest event and we set that in the CPU
						# If the CPU did change processes. Put the new one into the CPU
						if (self.__CPU != self.readyQ.readyQ[0]):
							self.changeCPUprocess()
							self.__CPU['cpu_arrival_time'] = self.__clock
							del self.readyQ.readyQ[0]
							# TODO figure out if this head event is right
							self.count = self.count + 1
							self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,
							                         self.__end_condition, self.count)
							head_event = self.events.event_Queue[self.count]
							continue
						# If not switching processes just keep the new process in ready queue and keep the CPU going like a champ.
						else:
							del self.readyQ.readyQ[0]
							self.count = self.count + 1
							self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,
							                         self.__end_condition, self.count)
							head_event = self.events.event_Queue[self.count]
							continue

			# if ready q has something in it and CPU has something in it.
			if (self.readyQ.readyQ and self.__is_busy == True):
				self.appendToReadyQ(head_event)

				# First time a process comes in, update the clocks to its arrival time,
				# also update the one that's been in the CPU processing time with the new clock data
				# The reamining time ius what is left./
				if (self.readyQ.readyQ[0]['remaining_time'] == self.readyQ.readyQ[0][
					'service_time']):  ## First time being processed
					self.__clock = self.readyQ.readyQ[0]['arrival_time']
					self.__CPU['cpu_processing_time'] = self.__clock - self.__CPU['cpu_arrival_time']
					self.__CPU['remaining_time'] = self.__CPU['remaining_time'] - self.__CPU['cpu_processing_time']

				# TODO make sure this is right if it not the first time.
				else:
					# Set the clock to how long the process in the CPU has been going.
					self.__clock = self.__clock + self.__CPU['cpu_processing_time']
					# Update the processing time of what was in the CPU with the new clock based off when it arrived.
					self.__CPU['cpu_processing_time'] = self.__clock - self.__CPU['cpu_arrival_time']
					# Remaining Time is self explanatory
					self.__CPU['remaining_time'] = self.__CPU['remaining_time'] - self.__CPU['cpu_processing_time']

				# TODO Make sure this is right. When process ends
				if (self.__CPU['remaining_time'] <= 0):
					self.__CPU['completion_time'] = self.__CPU['cpu_processing_time'] - self.__CPU['cpu_arrival_time']
					self.readyQ.sortQ()
					self.changeCPUprocess()
					del self.readyQ.readyQ[0]

					self.count = self.count + 1
					self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,
					                         self.__end_condition, self.count)
					head_event = self.events.event_Queue[self.count]
					continue
				else:
					self.appendToReadyQ(self.__CPU)
					# The event that is first should be the shortest event and we set that in the CPU
					# If the CPU did change processes. Put the new one into the CPU
					if (self.__CPU != self.readyQ.readyQ[0]):
						self.changeCPUprocess()
						self.__CPU['cpu_arrival_time'] = self.__clock
						del self.readyQ.readyQ[0]

						self.count = self.count + 1
						self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,
						                         self.__end_condition, self.count)
						head_event = self.events.event_Queue[self.count]
						continue
					# If not switching processes just keep the new process in ready queue and keep the CPU going like a champ.
					else:
						del self.readyQ.readyQ[0]
						self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,
						                         self.__end_condition, self.count)
						head_event = self.events.event_Queue[self.count]
						continue

	def changeCPUprocess(self):
		self.__CPU = None
		self.__is_busy = False
		self.__CPU = copy.deepcopy(self.readyQ.readyQ[0])
		self.__is_busy = True

	def appendToReadyQ(self, event):
		self.readyQ.readyQ.append(copy.deepcopy(event))
		self.readyQ.sortQ()

	#####################################################################################################################

	def hrrn(self):
		#  shortest response time first w (waiting time)+s(service time) / (service time)
		self.events.event_Queue.sort(key=lambda k: k['arrival_time'])
		self.count = 0
		are_we_done = 0
		self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock, self.__end_condition, are_we_done)
		while are_we_done != self.__end_condition:  # getting next event
			try:
				head_event = self.events.event_Queue[self.count]
				if self.__is_busy == False:
					if head_event['arrival_time'] >= self.__clock:  # put in ready que
						are_we_done = are_we_done + 1
					self.processArrival(self.readyQ, head_event)
					self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,self.__end_condition, are_we_done)
				else:
					if (self.readyQ.readyQ[0]['process_status'] == 'departed'):
						self.count = self.count + 1
						self.processDeparture(self.readyQ, self.readyQ.readyQ[0])
						are_we_done = are_we_done + 1
				self.processArrival(self.readyQ, head_event)
				are_we_done = are_we_done + 1
				self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock, self.__end_condition, are_we_done)
				self.readyQ.sortQ()

			except IndexError:
				print('index error: ' + str(self.count) + '\n')
				pass

	def rr(self):
		# Initial Sort Of Nothing In Queue
		self.events.event_Queue.sort(key=lambda k: k['arrival_time'])
		self.count = 0
		is_done_yet = 0
		self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock, self.__end_condition, is_done_yet)
		while is_done_yet != self.__end_condition:  # getting next event
			try:
				head_event = self.events.event_Queue[self.count]
				if self.__is_busy == False:
					if head_event['arrival_time'] >= self.__clock:  # put in ready que
						is_done_yet = is_done_yet + 1
					self.processArrival(self.readyQ, head_event)
					self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock,self.__end_condition, is_done_yet)
				else:
					if (self.readyQ.readyQ[0]['process_status'] == 'departed'):
						self.count = self.count + 1
						self.processDeparture(self.readyQ, self.readyQ.readyQ[0])
						is_done_yet = is_done_yet + 1
				self.processArrival(self.readyQ, head_event)
				is_done_yet = is_done_yet + 1
				self.events.createEvents(self.__lambda_val, self.__average_service_time, self.__clock, self.__end_condition, is_done_yet)
				self.readyQ.sortQ()

			except IndexError:
				print('index error: ' + str(self.count) + '\n')
				pass
		pass

	def round_robin_helper(self, event):
		# Process id's
		n = len(event)
		burst_time = [].append(event['service_time'])
		quantum = self.__quantum_value
		wt = [0] * n
		tat = [0] * n
		remaining_burst_time = [0] * n
		for i in range(n):
			remaining_burst_time[i] = burst_time[i]
		t = 0  # Current time
		while 1:
			done = True
			for i in range(n):
				if remaining_burst_time[i] > 0:
					done = False  # There is a pending process
					if remaining_burst_time[i] > quantum:
						t += quantum
						remaining_burst_time[i] -= quantum
					else:
						t = t + remaining_burst_time[i]
						wt[i] = t - burst_time[i]
						remaining_burst_time[i] = 0
			if done:
				break
		for i in range(n):
			tat[i] = burst_time[i] + wt[i]
		print("Processes    Burst Time     Waiting Time    Turn-Around Time")
		total_wt = 0
		total_tat = 0
		for i in range(n):
			total_wt = total_wt + wt[i]
			total_tat = total_tat + tat[i]
			print(" ", i + 1, "\t\t", burst_time[i], "\t\t", wt[i], "\t\t", tat[i])
		print("\nAverage waiting time = %.5f " % (total_wt / n))
		print("Average turn around time = %.5f " % (total_tat / n))

	def processArrival(self, readyQ, event):
		if self.__clock < event['arrival_time']:
			self.__clock = event['arrival_time']  # setting the clock
		# FCFS
		if scheduler == 1:
			if not self.__is_busy:
				self.__is_busy = True
				self.__CPU = copy.deepcopy(event)
				event['process_status'] = 'departed'
				# event['completion_time'] = self.__clock + event['service_time']
			else:
				event['process_status'] = 'arrived'

			self.readyQ.readyQ.append(copy.deepcopy(event))
			self.readyQ.sortQ()

		# SRTF --Temporary Code for the basis run to work
		if scheduler == 2:
			if not self.__is_busy:  # if there is no line, go straight in
				readyQ.scheduleEvent('departed', event, self.__clock)
			else:
				# if its busy it will get interrupted
				readyQ.scheduleEvent('arrived', event, self.__clock)  # put process in the queue
				self.processDeparture(self.readyQ, self.__CPU)  # take process out of the cpu and into the queue
				readyQ.sortQ()  # srtf is at index [0] in readyQ

				self.__is_busy = True
				self.__CPU = copy.deepcopy(readyQ.readyQ[0])  # put srtf in the cpu
				readyQ.readyQ[0]['cpu_arrival_time'] = self.__clock
				readyQ.scheduleEvent('departed', readyQ.readyQ[0], self.__clock)  # schedule when it finishes

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
				self.round_robin_helper(event, self.__clock)


	def processDeparture(self, readyQ, event):
		# FCFS
		if scheduler == 1:
			self.__clock = self.__clock + event['service_time']

			event['completion_time'] = self.__clock
			self.events.event_Queue[self.count]['completion_time'] = self.__clock
			self.readyQ.removeEvent(event)

			self.__is_busy = False  # clear the cpu
			self.__CPU = None

		# SRTF
		if scheduler == 2:
			if (event['remaining_time'] == event['service_time']):  ## First time it a process is processed
				event['remaining_time'] = event['remaining_time'] - event['cpu_arrival_time']
			else:
				event['remaining_time'] = event['remaining_time'] - (self.__clock + event['cpu_arrival_time'])
			if event['remaining_time'] == 0:  # if the process is done
				self.readyQ.removeEvent(event)
			# event['completion_time'] = self.__clock
			else:
				readyQ.scheduleEvent('arrived', event, self.__clock)
			self.__is_busy = False
			self.__CPU = None

		# HRRN
		if scheduler == 3:
			service_time_value = event['service_time']
			waiting_time_value = self.__clock - event['arrival_time']
			ratio_value = (waiting_time_value + service_time_value) / service_time_value
			event['completion_time'] = self.__clock
			event['ratio'] = ratio_value
			self.readyQ.removeEvent(event)
			self.__is_busy = False
			self.__CPU = None

		# RR @todo
		if scheduler == 4:
			pass


#####################################################################################

class Event:

	def __init__(self):
		self.event_Queue = []

	def createEvents(self, lambda_value, average_service_time, clock, end_condition, count):
		print("Scheduling Event PID:  " + str(
			count))  # creates a new event and places it in the event queue based on its time.

		random_service_time = generateExp(1 / average_service_time)
		random_arrival_time = generateExp(lambda_value)
		self.event_Queue.append(self.eventArrival(random_service_time, clock + random_arrival_time, count + 1))

	# hard coding in events for debugging
	# if count >= 5:
	# 	self.event_Queue.append(self.eventArrival(random_service_time, clock + random_arrival_time, count + 1))
	# elif count == 0:
	# 	self.event_Queue.append(self.eventArrival(3, 0, 'A'))
	# elif count == 1:
	# 	self.event_Queue.append(self.eventArrival(4, 1, 'B'))
	# elif count == 2:
	# 	self.event_Queue.append(self.eventArrival(3, 3, 'C'))
	# elif count == 3:
	# 	self.event_Queue.append(self.eventArrival(2, 6, 'D'))
	# elif count == 4:
	# 	self.event_Queue.append(self.eventArrival(5, 12, 'E'))

	def eventArrival(self, service_time, arrival_time, process_count):
		return {
			'pId': process_count,
			'service_time': service_time,
			'arrival_time': arrival_time,
			'remaining_time': service_time,
			'cpu_processing_time': 0,
			'completion_time': 0,
			'waiting_time': 0,
			'process_status': 'arrived',
			'ratio': 0,
			'cpu_arrival_time': 0
		}


#####################################################################################
class ReadyQueue:

	def __init__(self):
		self.readyQ = []

	def isempty(self):
		return len(self.readyQ) == 0

	def front(self):
		return next(iter(self.readyQ), None)

	def sortQ(self):  # sorts the readyQ
		if scheduler == 1:
			self.readyQ.sort(key=lambda k: k['arrival_time'])
		elif scheduler == 2:
			self.readyQ.sort(key=lambda k: k['remaining_time'])
		elif scheduler == 3:
			self.readyQ.sort(key=lambda k: k['ratio'], reverse=True)

	def scheduleEvent(self, Event_type, event, time):

		event['process_status'] = Event_type

		# FCFS
		if scheduler == 1:
			if Event_type == 'departed':
				event['completion_time'] = time + event['service_time']

		# SRTF
		if scheduler == 2:
			if Event_type == 'departed':
				pass

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
		lambda_value = float(sys.argv[2]) # 1 - 30
		average_service_time = float(sys.argv[3])
		if len(sys.argv) == 5:
			quantum_value = float(sys.argv[4])
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
	sim.generate_report()

#####################################################################################
