/* Project 1
 In this project, we are going to build a discrete-time event
 simulator for a number of CPU schedulers on a single CPU system.
 The goal of this project is to compare and assess the impact of
 different schedulers on different performance metrics, and across multiple workloads.
 @authors: Jamal Rasool, Kristof York
 @date: March 21st, 2019
*/
#ifndef HEADER_H
#define HEADER_H

// Base functions
void parseArgs(char *[]);  
void init();
void run_sim();
float urand();
float genExp(float);
void generate_report();

// Scheduler Functinos
void FCFS();   // first come first serve 
void SRTF();   // shortest remaining time next  
void HRRN();   // highest response ratio next
void RR();     // round robin 

// helper functions
void scheduleArrival();
void scheduleDeparture();
void scheduleAllocation();
void schedulePreemption();
void handleArrival();
void handleDeparture();
void handleAllocation();
void handlePreemption();
void scheduleQuantumDeparture();
void scheduleQuantumAllocation();
void scheduleQuantumPreemption();
void handleQuantumAllocation();
void handleQuantumPreemption();
void handleQuantumDeparture();
float getNextQuantumClockTime();
float getNextQuantumAllocationTime();
void popReadyQHead();
void popEventQHead();
bool isPreemptive();
float cpuEstFinishTime();

// Output functions
float getAvgTurnaroundTime();
float getTotalThroughput();
float getCpuUtil();
float getAvgNumProcInQ();

#endif