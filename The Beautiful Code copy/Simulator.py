import math
import random

class CPU:
    def __init__(self):
        self.clock = 0
        self.busy = False
        self.process_being_worked_on = Process()


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
    def __init__(self, scheduler, the_lambda, avg_service_time, quantum, end_condition):
        # parameters for scheduler
        self.cpu = CPU()
        self.scheduler = scheduler
        self.the_lambda = the_lambda
        self.avg_service_time = avg_service_time
        self.quantum = quantum

        # end conditions and result counters
        self.end_condition = end_condition
        self.number_completed_processes = 0
        self.total_turnaround_time = 0
        self.total_service_times = 0
        self.sum_num_of_proc_in_readyQ = 0

        # queues
        self.ready_queue = []
        self.event_queue = []

    def FCFS(self):

        first_process = self.generateProcess()
        first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
        self.event_queue.append(first_event)

        while self.number_completed_processes < self.end_condition:
            # sort the event queue so that the next occuring event appears
            self.event_queue.sort(key=lambda x: x.time)

            # remove the next event from the event queue (get the event)
            event = self.event_queue.pop(0)

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
                    self.event_queue.append(event)

                # if the arrival happens, the cpu is not busy, and the ready queue is not empty
                elif self.cpu.busy is True:
                    self.ready_queue.append(event.process)

                else:
                    print("something is wrong")

                # create a new process and attach it to an arrival event
                new_process = self.generateProcess()
                new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
                self.event_queue.append(new_arrival_event)

            # else the event type is a DEPARTURE event
            elif event.type is "DEP":

                # number of completed process goes up
                self.sum_num_of_proc_in_readyQ += len(self.ready_queue)
                self.number_completed_processes += 1
                self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)

                # if ready queue is empty, cpu goes idle and event is deleted
                if len(self.ready_queue) is 0:
                    self.cpu.busy = False

                # if ready queue is not empty, the next process is pulled and a departure event is created
                # that process will have its start time and end time set here
                else:
                    process_departing = self.ready_queue.pop(0)
                    process_departing.start_time = self.cpu.clock
                    process_departing.end_time = process_departing.start_time + process_departing.service_time
                    new_departure_event = self.generateEvent(process_departing.end_time, "DEP", process_departing)
                    self.event_queue.append(new_departure_event)
            else:
                print("Invalid Event Type")

        self.ready_queue.clear()
        self.event_queue.clear()
        self.number_completed_processes = 0

    def SRTF(self):

        first_process = self.generateProcess()
        first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
        self.event_queue.append(first_event)

        while self.number_completed_processes < self.end_condition:

            # sort the event queue so that the next occuring event appears
            self.event_queue.sort(key=lambda x: x.time)

            # remove the next event from the event queue (get the event)
            event = self.event_queue.pop(0)

            # set the clock so that it is at the time of the occuring event
            self.cpu.clock = event.time

            # determine what type of event has just been pulled from the event queue
            # The instance that the event is an arrival
            if event.type is "ARR":

                # if the arrival happens, the cpu is not busy
                if self.cpu.busy is False:

                    # make the cpu busy and and change the event from an arrival to a departure (schedule the departure)
                    self.cpu.busy = True
                    event.type = "DEP"
                    event.process.end_time = self.cpu.clock + event.process.remaining_service_time
                    event.time = event.process.end_time
                    self.event_queue.append(event)

                    self.cpu.process_being_worked_on = event.process

                # if the arrival happens, the cpu is busy
                elif self.cpu.busy is True:
                    self.ready_queue.append(event.process)
                    self.shortestRemainingTimeCalculation()

                else:
                    print("something is wrong")

                # create a new process and attach it to an arrival event
                new_process = self.generateProcess()
                new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
                self.event_queue.append(new_arrival_event)

            # else the event type is a DEPARTURE event
            elif event.type is "DEP":

                # number of completed process goes up
                self.sum_num_of_proc_in_readyQ += len(self.ready_queue)
                self.number_completed_processes += 1
                self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)
                self.cpu.process_being_worked_on = None

                # if ready queue is empty, cpu goes idle and event is deleted
                if len(self.ready_queue) is 0:
                    self.cpu.busy = False

                # if ready queue is not empty, the next process is pulled and a departure event is created
                # that process will have its start time and end time set here
                else:
                    self.ready_queue.sort(key=lambda x: x.remaining_service_time)
                    process_departing = self.ready_queue.pop(0)
                    process_departing.start_time = self.cpu.clock
                    process_departing.end_time = process_departing.start_time + process_departing.remaining_service_time

                    self.cpu.process_being_worked_on = process_departing

                    new_departure_event = self.generateEvent(process_departing.end_time, "DEP", process_departing)
                    self.event_queue.append(new_departure_event)

            else:
                print("Invalid Event Type")

        self.ready_queue.clear()
        self.event_queue.clear()
        self.number_completed_processes = 0

    def HRRN(self):

        first_process = self.generateProcess()
        first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
        self.event_queue.append(first_event)

        while self.number_completed_processes < self.end_condition:

            # sort the event queue so that the next occuring event appears
            self.event_queue.sort(key=lambda x: x.time)

            # remove the next event from the event queue (get the event)
            event = self.event_queue.pop(0)

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
                    self.event_queue.append(event)

                # if the arrival happens, the cpu is not busy, and the ready queue is not empty
                elif self.cpu.busy is True:
                    self.ready_queue.append(event.process)
                else:
                    print("something is wrong")

                # create a new process and attach it to an arrival event
                new_process = self.generateProcess()
                new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
                self.event_queue.append(new_arrival_event)

            # else the event type is a DEPARTURE event
            elif event.type is "DEP":

                # number of completed process goes up
                self.sum_num_of_proc_in_readyQ += len(self.ready_queue)
                self.number_completed_processes += 1
                self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)

                # if ready queue is empty, cpu goes idle and event is deleted
                if len(self.ready_queue) is 0:
                    self.cpu.busy = False

                # if ready queue is not empty, the next process is pulled and a departure event is created
                # that process will have its start time and end time set here
                else:
                    self.ratioCalculation()
                    self.ready_queue.sort(key=lambda x: x.response_ratio)
                    process_departing = self.ready_queue.pop(0)
                    process_departing.start_time = self.cpu.clock
                    process_departing.end_time = process_departing.start_time + process_departing.service_time

                    new_departure_event = self.generateEvent(process_departing.end_time, "DEP", process_departing)
                    self.event_queue.append(new_departure_event)
            else:
                print("Invalid Event Type")

        self.ready_queue.clear()
        self.event_queue.clear()
        self.number_completed_processes = 0

    def RR(self):
        first_process = self.generateProcess()
        first_event = self.generateEvent(first_process.arrival_time, "ARR", first_process)
        self.event_queue.append(first_event)

        while self.number_completed_processes < self.end_condition:
            # sort the event queue so that the next occuring event appears
            self.event_queue.sort(key=lambda x: x.time)

            # remove the next event from the event queue (get the event)
            event = self.event_queue.pop(0)

            # set the clock so that it is at the time of the occuring event
            self.cpu.clock = event.time
            event.process.start_time = self.cpu.clock
            # determine what type of event has just been pulled from the event queue
            # The instance that the event is an arrival

            if event.type is "ARR":
                # If Cpu is idle
                    # create a departure event
                    # add to event queue
                    # set the end to time to clock + remaining service time
                if self.cpu.busy is False:
                    self.cpu.busy = True
                    if event.process.remaining_service_time > self.quantum:
                        event.type = "SWAP"
                        event.time = self.cpu.clock + self.quantum
                        event.process.remaining_service_time -= self.quantum
                    else:
                        event.type = "DEP"
                        event.process.end_time = self.cpu.clock + event.process.remaining_service_time
                        event.time = event.process.end_time
                    self.cpu.process_being_worked_on = event.process
                    self.event_queue.append(event)

                # else if CPU is not idle and ready queue is empty
                else:
                    self.ready_queue.append(event.process)
                    # gets put back into ready queue
                    # process in cpu's new remaining service time calculated

                # create a new process and attach it to an arrival event
                new_process = self.generateProcess()
                new_arrival_event = self.generateEvent(new_process.arrival_time, "ARR", new_process)
                self.event_queue.append(new_arrival_event)

            elif event.type is "SWAP":
                if len(self.ready_queue) is 0:
                    if event.process.remaining_service_time < self.quantum:
                        event.process.remaining_service_time -= self.quantum
                        event.time += self.quantum
                        self.event_queue.append(event)
                    else:
                        event.type = "DEP"
                        event.time = event.process.remaining_service_time + self.cpu.clock
                        self.event_queue.append(event)

                else:
                    # pull process from cpu and process from front of ready queue
                    self.ready_queue.append(self.cpu.process_being_worked_on)
                    self.cpu.process_being_worked_on = None
                    process_from_front_of_ready_queue = self.ready_queue.pop(0)
                    # If process that is coming out of ready queue has a remaining service time that is less than the quantum
                    if process_from_front_of_ready_queue.remaining_service_time < self.quantum:
                        # schedule a departure event
                        sched_dep_event = self.generateEvent((self.cpu.clock + event.process.remaining_service_time), "DEP", process_from_front_of_ready_queue)
                        sched_dep_event.process.end_time = sched_dep_event.time
                        self.cpu.process_being_worked_on = sched_dep_event.process
                        self.cpu.process_being_worked_on.start_time = self.cpu.clock
                        self.event_queue.append(sched_dep_event)
                    # else
                    else:
                        # schedule another swap
                        sched_swap_event = self.generateEvent((self.cpu.clock + self.quantum), "SWAP", process_from_front_of_ready_queue)
                        sched_swap_event.process.remaining_service_time -= self.quantum
                        self.cpu.process_being_worked_on = sched_swap_event.process
                        self.cpu.process_being_worked_on.start_time = self.cpu.clock
                        self.event_queue.append(sched_swap_event)

            elif event.type is "DEP":
                self.sum_num_of_proc_in_readyQ += len(self.ready_queue)
                self.total_turnaround_time += (self.cpu.clock - event.process.arrival_time)
                self.number_completed_processes += 1
                # If ready queue is empty

                if len(self.ready_queue) is 0:
                    self.cpu.busy = False
                    # this would mean no more processes

                # else if the ready queue is not empty
                else:
                    # take the next process from the ready queue
                    next_process = self.ready_queue.pop(0)

                    # if the remaining service time is less than quantum
                    if next_process.remaining_service_time < self.quantum:
                        # schedule a departure event
                        sched_dep_event = self.generateEvent((self.cpu.clock + event.process.remaining_service_time), "DEP", next_process)
                        sched_dep_event.process.end_time = sched_dep_event.time
                        self.cpu.process_being_worked_on = sched_dep_event.process
                        self.cpu.process_being_worked_on.start_time = self.cpu.clock
                        self.event_queue.append(sched_dep_event)
                    # else
                    else:
                        # schedule another swap
                        sched_swap_event = self.generateEvent((self.cpu.clock + self.quantum), "SWAP", next_process)
                        sched_swap_event.process.remaining_service_time -= self.quantum
                        self.cpu.process_being_worked_on = sched_swap_event.process
                        self.cpu.process_being_worked_on.start_time = self.cpu.clock
                        self.event_queue.append(sched_swap_event)
            else:
                print("Invalid Event Type")

        self.ready_queue.clear()
        self.event_queue.clear()
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
        for i in range(len(self.ready_queue)):
            self.ready_queue[i].response_ratio = self.cpu.clock - self.ready_queue[i].arrival_time

    def shortestRemainingTimeCalculation(self):
        self.ready_queue.sort(key=lambda x: x.remaining_service_time)

        self.cpu.process_being_worked_on.remaining_service_time = self.cpu.process_being_worked_on.end_time - self.cpu.clock

        if len(self.ready_queue) > 0 and self.cpu.process_being_worked_on.remaining_service_time > self.ready_queue[0].remaining_service_time:
            for i in range(len(self.event_queue)):
                if self.event_queue[i].process is self.cpu.process_being_worked_on:
                    self.event_queue.pop(i)

            self.ready_queue.append(self.cpu.process_being_worked_on)

            new_event = self.generateEvent((self.cpu.clock + self.ready_queue[0].remaining_service_time), "DEP", self.ready_queue.pop(0))
            self.event_queue.append(new_event)
            self.cpu.process_being_worked_on = new_event.process

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

        if self.scheduler is 1 and self.the_lambda is 1:
            with open("results.txt", "w+") as results_file:
                results_file.write(
                    "---------\t------\t--------------\t-----------------\t----------\t--------\t--------------\t-------\n")
                results_file.write(
                    "Scheduler\tLambda\tAvgServiceTime\tAvgTurnaroundTime\tThroughput\tCPU Util\tAvg#ProcReadyQ\tQuantum\n")
                results_file.write(
                    "---------\t------\t--------------\t-----------------\t----------\t--------\t--------------\t-------\n")
                results_file.write('{:9}'.format(scheduler_label) + str("\t"))
                results_file.write('{:>6}'.format(str(self.the_lambda)) + str("\t"))
                results_file.write('{:>14}'.format(str(self.avg_service_time)) + str("\t"))
                results_file.write('{:>17}'.format(str(avg_turn_around_time)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(cpu_utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\t"))
                results_file.write('{:>7}'.format(str(self.quantum)) + str("\n"))
                results_file.close()

        elif self.the_lambda is 1:
            with open("results.txt", "a+") as results_file:
                results_file.write(
                    "Scheduler\tLambda\tAvgServiceTime\tAvgTurnaroundTime\tThroughput\tCPU Util\tAvg#ProcReadyQ\tQuantum\n")
                results_file.write(
                    "---------\t------\t--------------\t-----------------\t----------\t--------\t--------------\t-------\n")
                results_file.write('{:9}'.format(scheduler_label) + str("\t"))
                results_file.write('{:>6}'.format(str(self.the_lambda)) + str("\t"))
                results_file.write('{:>14}'.format(str(self.avg_service_time)) + str("\t"))
                results_file.write('{:>17}'.format(str(avg_turn_around_time)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(cpu_utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\t"))
                results_file.write('{:>7}'.format(str(self.quantum)) + str("\n"))
                results_file.close()

        elif self.the_lambda is 30:
            with open("results.txt", "a+") as results_file:
                results_file.write('{:9}'.format(scheduler_label) + str("\t"))
                results_file.write('{:>6}'.format(str(self.the_lambda)) + str("\t"))
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
                results_file.write('{:>6}'.format(str(self.the_lambda)) + str("\t"))
                results_file.write('{:>14}'.format(str(self.avg_service_time)) + str("\t"))
                results_file.write('{:>17}'.format(str(avg_turn_around_time)) + str("\t"))
                results_file.write('{:>10}'.format(str(throughput)) + str("\t"))
                results_file.write('{:>8}'.format(str(cpu_utilization)) + str("\t"))
                results_file.write('{:>14}'.format(str(avg_num_processes_in_readyQ)) + str("\t"))
                results_file.write('{:>7}'.format(str(self.quantum)) + str("\n"))
                results_file.close()

    def generateProcess(self):

        process = Process()
        process.arrival_time = self.cpu.clock + (math.log(1 - float(random.uniform(0, 1))) / (-self.the_lambda))
        process.service_time = math.log(1 - float(random.uniform(0, 1))) / (-(1/self.avg_service_time))
        process.remaining_service_time = process.service_time
        process.end_time = process.arrival_time + process.service_time
        self.total_service_times += process.service_time

        return process

    def generateEvent(self, time, type, process):

        event = Event()
        event.time = time
        event.type = type
        event.process = process

        return event