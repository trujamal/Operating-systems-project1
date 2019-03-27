import math
import random

class CPU:
    def __init__(self):
        self.clock = 0
        self.busy = False

class Process:
    def __init__(self):
        self.arrival_time = 0
        self.service_time = 0
        self.start_time = 0
        self.end_time = 0
        self.process_ID = 0
        self.type = ""

class Simulator:
    def __init__(self, scheduler, the_lambda, avg_service_time, quantum, end_condition):
        self.cpu = CPU()
        self.scheduler = scheduler
        self.the_lambda = the_lambda
        self.avg_service_time = avg_service_time
        self.quantum = quantum
        self.end_condition = end_condition
        self.number_completed_processes = 0
        self.total_turnaround_time = 0

        self.ready_queue = []
        self.event_queue = []
        self.scheduleEvent()

    def generateReport(self):
        if self.scheduler is 1:
            print("FCFS:")
        elif self.scheduler is 2:
            print("SRTF: ")
        elif self.scheduler is 3:
            print("HRRN:")
        elif self.scheduler is 4:
            print("RR:")
        else:
            print("Invalid input.")

        print("Clock: ", self.cpu.clock)
        print("Throughput: ", (self.end_condition/self.cpu.clock))
        print("Average turnaround time: ", (self.total_turnaround_time/self.end_condition))

    def FCFS(self):

        while self.number_completed_processes < self.end_condition:
            #print(self.number_completed_processes)

            self.event_queue.sort(key=lambda x: x.arrival_time)

            if self.event_queue[0].type == "ARRIVAL":
                # move the clock to the ARRIVAL and create a new event
                self.cpu.clock = self.event_queue[0].arrival_time
                self.scheduleEvent()

                if self.cpu.busy is False:
                    self.cpu.busy = True

                    # 'create' departure event
                    self.event_queue[0].type = "DEPARTURE"
                    self.event_queue[0].arrival_time = self.cpu.clock + self.event_queue[0].service_time

                else:
                    # add ARRIVAL event to ready queue
                    self.ready_queue.append(self.event_queue[0])

                    # 'create' departure event
                    self.event_queue[0].type = "DEPARTURE"
                    self.event_queue[0].arrival_time = self.cpu.clock + self.event_queue[0].service_time

            elif self.event_queue[0].type == "DEPARTURE":
                # move clock to the DEPARTURE
                self.cpu.clock = self.event_queue[0].arrival_time
                self.number_completed_processes += 1

                self.total_turnaround_time += (self.cpu.clock - self.event_queue[0].start_time)
                self.event_queue.pop(0)

                if len(self.ready_queue) == 0:
                    self.cpu.busy = False

                # if ready queue has an ARRIVAL in it, process that ARRIVAL
                else:
                    # 'create' departure event
                    self.ready_queue[0].type = "DEPARTURE"
                    self.ready_queue[0].arrival_time = self.cpu.clock + self.event_queue[0].service_time
                    self.event_queue.append(self.ready_queue[0])

                    # remove ARRIVAL from ready queue
                    self.ready_queue.pop(0)

            else:
                print('Invalid Input')

    def SRTF(self):

        pass

    def HRRN(self):
        pass

    def RR(self):
        pass

    def run(self):

        if self.scheduler is 1:
            self.FCFS()
        elif self.scheduler is 2:
            self.SRTF()
        elif self.scheduler is 3:
            self.HRRN()
        elif self.scheduler is 4:
            self.RR()
        else:
            print("Invalid input.")


    def scheduleEvent(self):
        new_process = Process()
        new_process.arrival_time = self.cpu.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.the_lambda))
        new_process.start_time = new_process.arrival_time
        new_process.service_time = math.log(1 - float(random.uniform(0, 1))) / (-self.avg_service_time)
        #new_process.process_ID = self.num_created_proc
        new_process.type = "ARRIVAL"
        self.event_queue.append(new_process)