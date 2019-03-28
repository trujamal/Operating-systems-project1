 /* main.cpp
 In this project, we are going to build a discrete-time event
 simulator for a number of CPU schedulers on a single CPU system.
 The goal of this project is to compare and assess the impact of
 different schedulers on different performance metrics, and across multiple workloads.
 @authors: John Daloni, Jamal Rasool, Kristof York, Fernando Valdes, Elliot Esponda
 @date: March 21st, 2019
*/ 

#ifndef HEADER_H
#define HEADER_H

// Creation of initialization functions.
void parseArgs(char *[]);  
void init();
void run_sim();
float urand();
float genExp(float);
void generate_report();

// Simmulator Functions
void FCFS();   
void SRTF();   
void HRRN();   
void RR();     

// Helper functions
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

// Report helper functinos
float getAvgTurnaroundTime();
float getTotalThroughput();
float getCpuUtil();
float getAvgNumProcInQ();

#endif