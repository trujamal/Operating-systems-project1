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

		self.finished_processes = 0

		self.numInreadyQ = 0
		self.count = 1
		self.end_condition = 10000

#####################################################################################

	def createEmptyEvent(self):
		return {
			'time' : None,
			'type' : None,
			'id' : None
		}

	def createProcess(self):
		serv_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.average_service_time))

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

		
		self.genReport()

#####################################################################################

	def fcfs(self):
		self.arrivaltoEventQ()
		self.count = self.count + 1
		while self.count != self.end_condition + 1:

			self.eventQ.sort(key=lambda k: k['time'])

			if self.is_busy == False: #if not busy then there is nothing in the readyQ or the cpu (IDLE/first run through)
				self.putinCPU()
			else:
				self.handleEvent()


#####################################################################################


	def hrrn(self):
		self.arrivaltoEventQ()
		self.count = self.count + 1
		while self.count != self.end_condition + 1:

			self.eventQ.sort(key=lambda k: k['time'])

			if self.is_busy == False: #if not busy then there is nothing in the readyQ or the cpu (IDLE/first run through)
				self.putinCPU()
			else:
				self.handleEvent()



#####################################################################################

	def arrivaltoEventQ(self):
			ev = self.createEmptyEvent()
			ev['time'] = self.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.lambda_val))
			ev['type'] = 'arrival'
			ev['id'] = self.count
			self.eventQ.append(ev) 		
			

	def departuretoEventQ(self, time, ID):
			ev = self.createEmptyEvent()
			ev['time'] = time
			ev['type'] = 'departure'
			ev['id'] = ID
			self.eventQ.append(ev) 

	def putinCPU(self):
		#skip readyQ since its empty & process eventQ[0]
		if (not self.readyQ):
			proc = self.createProcess()

			self.clock = self.eventQ[0]['time']
			proc['id'] = self.eventQ[0]['id']
			proc['arrival_time'] = self.clock
			del self.eventQ[0]
			self.arrivaltoEventQ()
			self.count = self.count + 1
		else:
			if scheduler == 2:
				self.calculateRatio()
			proc = self.readyQ[0] # get next event from the readyQ
			if self.clock < self.readyQ[0]['arrival_time']: # making sure time only moves forwards
				self.clock = self.readyQ[0]['arrival_time']
			del self.readyQ[0]

		proc['start_time'] = self.clock
		if scheduler == 3:
			finish_time = self.clock + proc['remaining_time']
		else:
			finish_time = self.clock + proc['service_time']
		proc['finish_time'] = finish_time

		self.CPU = copy.deepcopy(proc) #put process into cpu
		self.is_busy = True
		self.departuretoEventQ(finish_time, proc['id']) #generate departure event


	def handleEvent(self):
		#if next event is arrival but cpu is busy then put it in readyQ
		if self.eventQ[0]['type'] == 'arrival':
			# put into the readyQ
			if self.clock < self.eventQ[0]['time']: # making sure time only moves forwards
				self.clock = self.eventQ[0]['time']
			proc = self.createProcess()
			proc['arrival_time'] = self.clock
			proc['id'] = self.eventQ[0]['id']
			self.readyQ.append(copy.deepcopy(proc))
			if scheduler == 3:
				self.srtfCalculator()
			self.arrivaltoEventQ()
			self.count = self.count + 1 # maybe this instead of in line 121?

		else: #if next event is type == departure
			self.numInreadyQ += len(self.readyQ)
			self.clock = self.CPU['finish_time']
			self.history.append(copy.deepcopy(self.CPU)) #copy for debug/info
			self.CPU = None
			self.is_busy = False

		del self.eventQ[0]


	def calculateRatio(self):
		for i, ev in enumerate(self.readyQ):
			waiting = self.clock - self.readyQ[i]['arrival_time']
			self.readyQ[i]['ratio'] = (waiting + self.readyQ[i]['service_time']) / self.readyQ[i]['service_time']

		self.readyQ.sort(key=lambda k: k['ratio'], reverse=True)



	def srtf(self):
		self.arrivaltoEventQ()
		self.count = self.count + 1
		while self.count != self.end_condition + 1:

			self.eventQ.sort(key=lambda k: k['time'])
			self.readyQ.sort(key=lambda k: k["remaining_time"])

			if self.is_busy == False: #if not busy then there is nothing in the readyQ or the cpu (IDLE/first run through)
				self.putinCPU()
			else:
				self.handleEvent()


	def srtfCalculator(self):
		# find shortest remaining time in the readyQ
		self.readyQ.sort(key=lambda k: k["remaining_time"])
		#find  process in the Cpu's remaining time
		self.CPU['remaining_time'] = self.CPU["finish_time"] - self.clock

		#If a switch is necessary do it.
		if (len(self.readyQ) > 0 and self.readyQ[0]["remaining_time"] < self.CPU['remaining_time']):

			#find and remove the event in the CPU
			for i in range(len(self.eventQ)):
				if self.eventQ[i]["id"] is self.CPU["id"]:
					self.eventQ.pop(i)
			# take the old running process and put in the R.Q and make a new departure for it.
			
			self.readyQ.append(self.CPU)
			self.CPU = self.readyQ[0] #swap out cpu and readyq[0]

			self.departuretoEventQ(self.clock + self.CPU["remaining_time"], self.CPU['id'])
			





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
		if scheduler == 3:
			scheduler_value = 'SRTF()'

		average_turn_around_time = self.getAvgTurnaroundTime()
		total_throughput = self.getTotalThroughput()
		cpu_utilization = self.getCpuUtil()
		average_process_in_queue = self.getAvgNumProccessInQueue()

		# Change file name as needed:
		with open("Output.txt", "a+") as data_file:
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
		return round(total / self.end_condition, 2)

	def getTotalThroughput(self):
		return round(self.end_condition/self.clock,3)

	def getCpuUtil(self):
		total = 0
		for ev in self.history:
			total = total + ev['service_time']
		return round((total / self.clock),2)

	def getAvgNumProccessInQueue(self):
		return round(self.numInreadyQ / self.end_condition, 2)
				

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
