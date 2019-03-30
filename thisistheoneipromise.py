import random
import sys
import math
import copy
from collections import deque
import bisect


#####################################################################################
class Simmulator: 

	def __init__(self, scheduler, lambda_val, average_service_time, quantum_value):
		self.clock = 0
		self.CPU = {}
		self.is_busy = False

		self.readyQ = []
		self.eventQ = []

		#used to store all events when finished, for report and debugging
		self.history = []

		self.scheduler = scheduler
		self.lambda_val = lambda_val
		self.average_service_time = average_service_time
		self.quantum_value = quantum_value

		self.count = 1
		self.end_condition = 10000

#####################################################################################

	def createEmptyEvent(self):
		return {
			'time' : None,
			'type' : None,
			'id' : None
		}

## NEed a little clarification.
	def createProcess(self):
		serv_time = generateExp(1 / average_service_time)
		
		return {
			'arrival_time' : 0,
			'service_time' : serv_time,
			'remaining_time' : serv_time,
			'start_time' : 0,
			'finish_time' : 0,
			'id' : 0,
			'ratio' : 0
		}

	def run(self):
		if scheduler == 1:
			self.fcfs() 
		if scheduler == 2:
			self.hrrn()
		if scheduler == 3:
			self.srtf()

			# print (self.history)
		
		self.genReport()

#####################################################################################

## Feel Like we should round times before calculations?

	def fcfs(self):
		self.arrivaltoEventQ()
		self.count = self.count + 1
		while self.count != self.end_condition + 1:

			self.eventQ.sort(key=lambda k: k['time'])
			##  EXPLAIN Does this if Makes sense? And line up right with the else? Think might have an indent errpr can you explain
			#readyq stuff
			if self.is_busy == False: #if not busy then there is nothing in the readyQ or the cpu (IDLE/first run through)
			
				#skip readyQ since its empty & process eventQ[0]
				if (not self.readyQ):
					proc = self.createProcess()
				
					self.clock = self.eventQ[0]['time']
					proc['id'] = self.eventQ[0]['id']
					proc['arrival_time'] = self.clock
					del self.eventQ[0]
					self.arrivaltoEventQ()
					self.count = self.count + 1 #????????
				else:
				
					proc = self.readyQ[0] #get next event from the readyQ
					self.clock = self.readyQ[0]['arrival_time']
					del self.readyQ[0]
				
				proc['start_time'] = self.clock 
				finish_time = self.clock + proc['service_time']
				proc['finish_time'] = finish_time
				
				#put process into cpu
				self.CPU = copy.deepcopy(proc)
				self.is_busy = True
				self.departuretoEventQ(finish_time, proc['id']) #generate departure event
				# self.count = self.count + 1 
				
			else:
				#if next event is arrival but cpu is busy then put it in readyQ 
				if self.eventQ[0]['type'] == 'arrival':
					# put into the readyQ
					if self.clock < self.eventQ[0]['time']: #making sure time only moves forwards
						self.clock = self.eventQ[0]['time']
					proc = self.createProcess()
					proc['arrival_time'] = self.clock
					proc['id'] = self.eventQ[0]['id']
					self.readyQ.append(copy.deepcopy(proc))
					self.arrivaltoEventQ()
					self.count = self.count + 1 # maybe this instead of in line 121?
	
				else: #if next event is type == departure 
					self.clock = self.CPU['finish_time']
					self.history.append(copy.deepcopy(self.CPU)) #copy for debug/info
					self.CPU = None
					self.is_busy = False

				del self.eventQ[0]
				

			# self.count = self.count + 1 #updating end condition	
			print (self.count)
				

	def arrivaltoEventQ(self):
			ev = self.createEmptyEvent()
			ev['time'] = generateExp(lambda_val) + self.clock
			ev['type'] = 'arrival'
			ev['id'] = self.count
			self.eventQ.append(ev) 		
			
        
	def departuretoEventQ(self, time, ID):
			ev = self.createEmptyEvent()
			ev['time'] = time
			ev['type'] = 'departure'
			ev['id'] = ID
			self.eventQ.append(ev) 

	
	def hrrn(self):
		self.arrivaltoEventQ()
		self.count = self.count + 1
		while self.count != self.end_condition + 1:

			self.eventQ.sort(key=lambda k: k['time'])

			#readyq stuff
			if self.is_busy == False: #if not busy then there is nothing in the readyQ or the cpu (IDLE/first run through)
			
				#skip readyQ since its empty & process eventQ[0]
				if (not self.readyQ):
					proc = self.createProcess()
				
					self.clock = self.eventQ[0]['time']
					proc['id'] = self.eventQ[0]['id']
					proc['arrival_time'] = self.clock
					del self.eventQ[0]
					self.arrivaltoEventQ()
				else:
					self.calculateRatio()
					proc = self.readyQ[0] #get next event from the readyQ
					self.clock = self.readyQ[0]['arrival_time']
					del self.readyQ[0]
				
				proc['start_time'] = self.clock 
				finish_time = self.clock + proc['service_time']
				proc['finish_time'] = finish_time
				
				#put process into cpu
				self.CPU = copy.deepcopy(proc)
				self.is_busy = True
				self.departuretoEventQ(finish_time, proc['id']) #generate departure event
				self.count = self.count + 1
				
			else:
				#if next event is arrival but cpu is busy then put it in readyQ 
				if self.eventQ[0]['type'] == 'arrival':
					# put into the readyQ
					if self.clock < self.eventQ[0]['time']: #making sure time only moves forwards
						self.clock = self.eventQ[0]['time']
					proc = self.createProcess()
					proc['arrival_time'] = self.clock
					proc['id'] = self.eventQ[0]['id']
					self.readyQ.append(copy.deepcopy(proc))
					self.arrivaltoEventQ()
					self.count = self.count + 1 # maybe this instead of in line 121?
	
				else: #if next event is type == departure 
					self.clock = self.CPU['finish_time']
					self.history.append(copy.deepcopy(self.CPU)) #copy for debug/info
					self.CPU = None
					self.is_busy = False

				del self.eventQ[0]
				

			# self.count = self.count + 1 #updating end condition	
			print (self.count)


	def calculateRatio(self):
		for i, ev in enumerate(self.readyQ):
			waiting = self.clock - self.readyQ[i]['arrival_time']
			self.readyQ[i]['ratio'] = (waiting + self.readyQ[i]['service_time']) / self.readyQ[i]['service_time']

		self.readyQ.sort(key=lambda k: k['ratio'], reverse=True)


#####################################################################################
#####################################################################################
############################## REPORT STUFFS ########################################
#####################################################################################
#####################################################################################

	def genReport(self):
		if scheduler == 1:
			scheduler_value = 'FCFS()'
		if scheduler == 2:
			scheduler_value = 'HRRN()'

		average_turn_around_time = self.getAvgTurnaroundTime()
		total_throughput = self.getTotalThroughput()
		cpu_utilization = self.getCpuUtil()
		average_process_in_queue = self.getAvgNumProccessInQueue()

		# Change file name as needed:
		with open("Output.txt", "w+") as data_file:
			print("Output is writing to: ", data_file.name)

			# if lambda_value == 10:
			data_file.write("Scheduler\tLambda\t\tAvgST\tAvgTA\tTotalTP\tCPU Util\tAvg#ProcsInQ \tQuantum\n")
			data_file.write("------------------------------------------------------------------------------------\n")

			data_file.write(scheduler_value + str("\t\t"))
			data_file.write(str(self.lambda_val) + str("\t\t"))
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
		total = 0 
		for ev in self.history:
			total = total + (ev['finish_time'] - ev["arrival_time"])
		print (len(self.history))
		return round(total / self.end_condition, 2)

	def getTotalThroughput(self):
		return round(self.end_condition/self.clock,3)
		#return round(len(self.history)/ self.clock, 2)

	def getCpuUtil(self):
		total = 0
		for ev in self.history:
			total = total + ev['service_time']
		return round((total / self.clock),2)

	def getAvgNumProccessInQueue(self):
		return 0 #round(self.numInQueue / self.count)
				

#####################################################################################
#####################################################################################
############################## DONT CROSS THIS ######################################
#####################################################################################
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
## START OF MAIN
if __name__ == "__main__":
	if len(sys.argv) >= 4:
		scheduler = int(sys.argv[1])
		lambda_val = float(sys.argv[2])
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

	sim = Simmulator(scheduler, lambda_val, average_service_time, quantum_value)
	sim.run()
#####################################################################################
