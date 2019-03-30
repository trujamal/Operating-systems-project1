import math
import random

class CPU:
    def __init__(self):
        self.clock = 0
        self.busy = False
        self.current_process = Process()


class Process:
    def __init__(self):
        self.arrival_time = 0
        self.service_time = 0
        self.start_time = 0
        self.end_time = 0
        self.response_ratio = 0
        self.remaining_service_time = 0


class Event:
    def __init__(self):
        self.time = 0
        self.type = ""
        self.process = Process()

class Simulator:
    def __init__(self, scheduler, lambda_val, avg_service_time, quantum, end_condition):
        # parameters for scheduler
        self.cpu = CPU()
        self.scheduler = scheduler
        self.lambda_val = lambda_val
        self.avg_service_time = avg_service_time
        self.quantum = quantum

        # end conditions and result counters
        self.end_condition = end_condition
        self.number_completed_processes = 0
        self.total_turnaround_time = 0
        self.total_service_times = 0
        self.sum_num_of_proc_in_readyQ = 0

        # queues
        self.readyQueue = []
        self.eventQueue = []

    def FCFS(self):

        first_process = self.generateProcess()
        first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
        self.eventQueue.append(first_event)

        while self.number_completed_processes < self.end_condition:
            # sort the event queue so that the next occuring event appears
            self.eventQueue.sort(key=lambda x: x.time)

            # remove the next event from the event queue (get the event)
            event = self.eventQueue.pop(0)

            # set the clock so that it is at the time of the occuring event
            self.cpu.clock = event.time

            # determine what type of event has just been pulled from the event queue
            # The instance that the event is an arrival
            if event.type is "ARR":

                # if the arrival happens, the cpu is not busy, and the ready queue is empty
                if self.cpu.busy is False:

                    # make the cpu busy and and change the event from an arrival to a departure (schedule the departure)
                    self.cpu.busy = True
                    event.type = "DEP"
                    event.process.end_time = self.cpu.clock + event.process.service_time
                    event.time = event.process.end_time

                    # add back to event queue
                    self.eventQueue.append(event)

                # if the arrival happens, the cpu is not busy, and the ready queue is not empty
                elif self.cpu.busy is True:
                    self.readyQueue.append(event.process)

                else:
                    print("something is wrong")

                # create a new process and attach it to an arrival event
                new_process = self.generateProcess()
                new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
                self.eventQueue.append(new_arrival_event)

            # else the event type is a DEPARTURE event
            elif event.type is "DEP":

                # number of completed process goes up
                self.sum_num_of_proc_in_readyQ += len(self.readyQueue)
                self.number_completed_processes += 1
                self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)
                self.total_service_times += event.process.service_time

                # if ready queue is empty, cpu goes idle and event is deleted
                if len(self.readyQueue) is 0:
                    self.cpu.busy = False

                # if ready queue is not empty, the next process is pulled and a departure event is created
                # that process will have its start time and end time set here
                else:
                    process_departing = self.readyQueue.pop(0)
                    process_departing.start_time = self.cpu.clock
                    process_departing.end_time = process_departing.start_time + process_departing.service_time
                    new_departure_event = self.generateEvent(process_departing.end_time, "DEP", process_departing)
                    self.eventQueue.append(new_departure_event)
            else:
                print("Invalid Event Type")

        self.readyQueue.clear()
        self.eventQueue.clear()
        self.number_completed_processes = 0

    def SRTF(self):

        first_process = self.generateProcess()
        first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
        self.eventQueue.append(first_event)

        while self.number_completed_processes < self.end_condition:

            # sort the event queue so that the next occuring event appears
            self.eventQueue.sort(key=lambda x: x.time)

            # get the next event
            event = self.eventQueue.pop(0)

            # move the clock to this event
            self.cpu.clock = event.time

            if event.type is "ARR":

                # if the CPU is idle
                if self.cpu.busy is False:

                    # make the cpu busy and make a departure for the process
                    self.cpu.busy = True
                    event.type = "DEP"
                    event.process.end_time = self.cpu.clock + event.process.remaining_service_time
                    event.time = event.process.end_time
                    self.eventQueue.append(event)

                    # set the current process in the CPU
                    self.cpu.current_process = event.process

                # if the CPU is busy, add the event to the readyQueue and
                # calculate the process with the shortest remaining time to completion
                elif self.cpu.busy is True:
                    self.readyQueue.append(event.process)
                    self.shortestRemainingTimeCalculation()

                else:
                    print("something is wrong")

                # create a new process and attach it to an arrival event
                new_process = self.generateProcess()
                new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
                self.eventQueue.append(new_arrival_event)

            elif event.type is "DEP":

                # increment stat keeper variables, and set the current CPU process to none
                self.number_completed_processes += 1
                self.sum_num_of_proc_in_readyQ += len(self.readyQueue)
                self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)
                self.total_service_times += event.process.service_time
                self.cpu.current_process = None

                # if readyQueue is empty the cpu goes idle
                if len(self.readyQueue) is 0:
                    self.cpu.busy = False

                # if the readyQueue isnt empty find the event with the shortest remaing service time and schedule it in
                # the events as a departure and in the current CPU process
                else:
                    self.readyQueue.sort(key=lambda x: x.remaining_service_time)
                    process_departing = self.readyQueue.pop(0)
                    process_departing.start_time = self.cpu.clock
                    process_departing.end_time = process_departing.start_time + process_departing.remaining_service_time
                    self.cpu.current_process = process_departing
                    new_departure_event = self.generateEvent(process_departing.end_time, "DEP", process_departing)
                    self.eventQueue.append(new_departure_event)

            else:
                print("Invalid Event Type")

        self.readyQueue.clear()
        self.eventQueue.clear()
        self.number_completed_processes = 0

    def HRRN(self):

        first_process = self.generateProcess()
        first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
        self.eventQueue.append(first_event)

        while self.number_completed_processes < self.end_condition:

            # sort the event queue so that the next occuring event appears
            self.eventQueue.sort(key=lambda x: x.time)

            # get the next event
            event = self.eventQueue.pop(0)

            # move forward ot the event
            self.cpu.clock = event.time

            if event.type is "ARR":

                # if the CPU is idle
                if self.cpu.busy is False:

                    # make the cpu busy and make a departure for the process
                    self.cpu.busy = True
                    event.type = "DEP"
                    event.process.end_time = self.cpu.clock + event.process.service_time
                    event.time = event.process.end_time
                    self.eventQueue.append(event)

                # if the CPU is busy add the process to the readyQueue
                elif self.cpu.busy is True:
                    self.readyQueue.append(event.process)
                else:
                    print("something is wrong")

                # create a new process and put it in an arrival event in the eventQueue
                new_process = self.generateProcess()
                new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
                self.eventQueue.append(new_arrival_event)

            elif event.type is "DEP":

                # increment stat keeper variables
                self.number_completed_processes += 1
                self.sum_num_of_proc_in_readyQ += len(self.readyQueue)
                self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)
                self.total_service_times += event.process.service_time

                # if ready queue is empty cpu goes idle
                if len(self.readyQueue) is 0:
                    self.cpu.busy = False

                # if ready queue is not empty, calculate response ratio and choose the highest one
                #
                else:
                    self.ratioCalculation()
                    self.readyQueue.sort(key=lambda x: x.response_ratio, reverse=True)
                    process_departing = self.readyQueue.pop(0)
                    process_departing.start_time = self.cpu.clock
                    process_departing.end_time = process_departing.start_time + process_departing.service_time

                    # attach the process to a departure event
                    new_departure_event = self.generateEvent(process_departing.end_time, "DEP", process_departing)
                    self.eventQueue.append(new_departure_event)
            else:
                print("Invalid Event Type")

        self.readyQueue.clear()
        self.eventQueue.clear()
        self.number_completed_processes = 0

    def RR(self):
        first_process = self.generateProcess()
        first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
        self.eventQueue.append(first_event)

        while self.number_completed_processes < self.end_condition:

            # sort the event queue so that the next occuring event appears
            self.eventQueue.sort(key=lambda x: x.time)

            # get the event
            event = self.eventQueue.pop(0)

            # move clock up to the current time
            self.cpu.clock = event.time
            event.process.start_time = self.cpu.clock

            if event.type is "ARR":

                # if the CPU is idle, make it busy
                if self.cpu.busy is False:
                    self.cpu.busy = True

                    # if process needs more than one quantum to finish create a swap event
                    if event.process.remaining_service_time > self.quantum:
                        event.type = "SWAP"
                        event.time = self.cpu.clock + self.quantum
                        event.process.remaining_service_time -= self.quantum

                    # if the process can finish in a quantum or less schedule a departure event
                    else:
                        event.type = "DEP"
                        event.process.end_time = self.cpu.clock + event.process.remaining_service_time
                        event.time = event.process.end_time

                    # put the process in the CPU current process and event in the eventQueue
                    self.cpu.current_process = event.process
                    self.eventQueue.append(event)

                # if the CPU is busy put the event in the readyQueue
                else:
                    self.readyQueue.append(event.process)

                # create a new process and attach it to an arrival event
                new_process = self.generateProcess()
                new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
                self.eventQueue.append(new_arrival_event)

            # if the event is a swap, meaning it needs more quantums to finish running
            elif event.type is "SWAP":

                # if the readyQueue is empty
                if len(self.readyQueue) is 0:

                    # if process needs more than one quantum to finish reduce the remaining service time
                    # and put back in eventQueue
                    if event.process.remaining_service_time > self.quantum:
                        event.process.remaining_service_time -= self.quantum
                        event.time += self.quantum
                        self.eventQueue.append(event)

                    # if the process can finish in under a quantum schedule a departure event
                    else:
                        event.type = "DEP"
                        event.time = event.process.remaining_service_time + self.cpu.clock
                        self.eventQueue.append(event)

                # if the readyQueue has processes in it
                else:

                    # put the current process in the back of the readyQueue and get the next process in the readyQueue
                    self.readyQueue.append(self.cpu.current_process)
                    self.cpu.current_process = None
                    next_process = self.readyQueue.pop()

                    # if the process form the front of the readyQueue can finish in one quantum or less schedule a departure event
                    if next_process.remaining_service_time < self.quantum:

                        # schedule a departure event
                        dep_event = self.generateEvent((self.cpu.clock + event.process.remaining_service_time), "DEP", next_process)
                        dep_event.process.end_time = dep_event.time
                        self.cpu.current_process = dep_event.process
                        self.cpu.current_process.start_time = self.cpu.clock
                        self.eventQueue.append(dep_event)

                    # if the process cant finish in a quantum
                    else:

                        # schedule another swap
                        swap_event = self.generateEvent((self.cpu.clock + self.quantum), "SWAP", next_process)
                        swap_event.process.remaining_service_time -= self.quantum
                        self.cpu.current_process = swap_event.process
                        self.cpu.current_process.start_time = self.cpu.clock
                        self.eventQueue.append(swap_event)

            elif event.type is "DEP":

                self.number_completed_processes += 1
                self.sum_num_of_proc_in_readyQ += len(self.readyQueue)
                self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)
                self.total_service_times += event.process.service_time

                # if the readyQueue is empty, make the cpu not busy
                if len(self.readyQueue) is 0:
                    self.cpu.busy = False
                    #self.cpu.current_process = None

                # if the ready queue is not empty
                else:

                    # take the next process from the ready queue
                    next_process = self.readyQueue.pop(0)

                    # if the process can finish in under a quantum
                    if next_process.remaining_service_time < self.quantum:

                        # schedule a departure event
                        dep_event = self.generateEvent((self.cpu.clock + event.process.remaining_service_time), "DEP", next_process)
                        dep_event.process.end_time = dep_event.time
                        self.cpu.current_process = dep_event.process
                        self.cpu.current_process.start_time = self.cpu.clock
                        self.eventQueue.append(dep_event)

                    # if the process needs more than one quantum to finish schedule a swap event
                    else:
                        # schedule another swap
                        swap_event = self.generateEvent((self.cpu.clock + self.quantum), "SWAP", next_process)
                        swap_event.process.remaining_service_time -= self.quantum
                        self.cpu.current_process = swap_event.process
                        self.cpu.current_process.start_time = self.cpu.clock
                        self.eventQueue.append(swap_event)
            else:
                print("Invalid Event Type")

        self.readyQueue.clear()
        self.eventQueue.clear()
        self.number_completed_processes = 0

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

    def ratioCalculation(self):
        for i in range(len(self.readyQueue)):
            self.readyQueue[i].response_ratio = ((self.cpu.clock - self.readyQueue[i].arrival_time) + self.readyQueue[i].service_time) / self.readyQueue[i].service_time

    def shortestRemainingTimeCalculation(self):

        # find the process with the shortest remaining time in the readyQueue
        self.readyQueue.sort(key=lambda x: x.remaining_service_time)

        # find out the current process remaining service time
        self.cpu.current_process.remaining_service_time = self.cpu.current_process.end_time - self.cpu.clock

        # if the readyQueue isnt empty and the current process has a remaining time that is greater than the smallest
        # remaining time in the readyQueue, switch the two processes
        if len(self.readyQueue) > 0 and self.cpu.current_process.remaining_service_time > self.readyQueue[0].remaining_service_time:

            # find the departure event matched with the current process in the CPU and get rid of it
            for i in range(len(self.eventQueue)):
                if self.eventQueue[i].process is self.cpu.current_process:
                    self.eventQueue.pop(i)

            # put the current process back in the readyQueue and create a new departure event for that process
            self.readyQueue.append(self.cpu.current_process)
            new_event = self.generateEvent((self.cpu.clock + self.readyQueue[0].remaining_service_time), "DEP", self.readyQueue.pop(0))
            self.eventQueue.append(new_event)

            # set the current process in the CPU to the one in the readyQueue with the SRT left
            self.cpu.current_process = new_event.process

    def generateReport(self):

        if self.scheduler is 1:
            scheduler_label = "FCFS"
        elif self.scheduler is 2:
            scheduler_label = "SRTF"
        elif self.scheduler is 3:
            scheduler_label = "HRRN"
        elif self.scheduler is 4:
            scheduler_label = "RR"
        else:
            print("Invalid input.")

        avg_turn_around_time = round((self.total_turnaround_time / self.end_condition), 3)
        throughput = round((self.end_condition / self.cpu.clock), 3)
        cpu_utilization = round(self.total_service_times / self.cpu.clock, 3)
        avg_num_processes_in_readyQ = round(self.sum_num_of_proc_in_readyQ / self.end_condition, 3)

        if self.scheduler is 1 and self.lambda_val is 1:
            with open("results.txt", "w+") as results_file:
                results_file.write(
                    "---------\t------\t--------------\t-----------------\t----------\t--------\t--------------\t-------\n")
                results_file.write(
                    "Scheduler\tLambda\tAvgServiceTime\tAvgTurnaroundTime\tThroughput\tCPU Util\tAvg#ProcReadyQ\tQuantum\n")
                results_file.write(
                    "---------\t------\t--------------\t-----------------\t----------\t--------\t--------------\t-------\n")
                results_file.write('{:9}'.format(scheduler_label) + str("\t"))
                results_file.write('{:>6}'.format(str(self.lambda_val)) + str("\t"))
                results_file.write('{:>14}'.format(str(self.avg_service_time)) + str("\t"))
                results_file.write('{:>17}'.format(str(avg_turn_around_time)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(cpu_utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\t"))
                results_file.write('{:>7}'.format(str(self.quantum)) + str("\n"))
                results_file.close()

        elif self.lambda_val is 1:
            with open("results.txt", "a+") as results_file:
                results_file.write(
                    "Scheduler\tLambda\tAvgServiceTime\tAvgTurnaroundTime\tThroughput\tCPU Util\tAvg#ProcReadyQ\tQuantum\n")
                results_file.write(
                    "---------\t------\t--------------\t-----------------\t----------\t--------\t--------------\t-------\n")
                results_file.write('{:9}'.format(scheduler_label) + str("\t"))
                results_file.write('{:>6}'.format(str(self.lambda_val)) + str("\t"))
                results_file.write('{:>14}'.format(str(self.avg_service_time)) + str("\t"))
                results_file.write('{:>17}'.format(str(avg_turn_around_time)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(cpu_utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\t"))
                results_file.write('{:>7}'.format(str(self.quantum)) + str("\n"))
                results_file.close()

        elif self.lambda_val is 30:
            with open("results.txt", "a+") as results_file:
                results_file.write('{:9}'.format(scheduler_label) + str("\t"))
                results_file.write('{:>6}'.format(str(self.lambda_val)) + str("\t"))
                results_file.write('{:>14}'.format(str(self.avg_service_time)) + str("\t"))
                results_file.write('{:>17}'.format(str(avg_turn_around_time)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(cpu_utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\t"))
                results_file.write('{:>7}'.format(str(self.quantum)) + str("\n"))
                results_file.write(
                    "---------\t------\t--------------\t-----------------\t----------\t--------\t--------------\t-------\n")
                results_file.close()

        else:
            with open("results.txt", "a+") as results_file:
                results_file.write('{:9}'.format(scheduler_label) + str("\t"))
                results_file.write('{:>6}'.format(str(self.lambda_val)) + str("\t"))
                results_file.write('{:>14}'.format(str(self.avg_service_time)) + str("\t"))
                results_file.write('{:>17}'.format(str(avg_turn_around_time)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(cpu_utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\t"))
                results_file.write('{:>7}'.format(str(self.quantum)) + str("\n"))
                results_file.close()

    def generateProcess(self):

        process = Process()
        process.arrival_time = self.cpu.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.lambda_val))
        process.service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.avg_service_time))
        process.remaining_service_time = process.service_time
        process.end_time = process.arrival_time + process.service_time
        process.start_time = 0

        return process

    def generateEvent(self, time, type, process):

        event = Event()
        event.time = time
        event.type = type
        event.process = process

        return event