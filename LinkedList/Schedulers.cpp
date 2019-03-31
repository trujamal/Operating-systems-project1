/* Project 1
 In this project, we are going to build a discrete-time event
 simulator for a number of CPU schedulers on a single CPU system.
 The goal of this project is to compare and assess the impact of
 different schedulers on different performance metrics, and across multiple workloads.
 @authors: Jamal Rasool, Kristof York
 @date: March 21st, 2019
*/

#include "header.h"
#include <cmath>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <fstream>
#include <string>
#include <iomanip>
using namespace std;

struct cpuNode
{
   float clock;
   bool cpuIsBusy;
   struct procListNode *pLink;
};

struct readyQNode
{
   struct procListNode *pLink;
   struct readyQNode *rNext;
};

struct eventQNode
{
   float time;
   int type;

   struct eventQNode *eNext;
   struct procListNode *pLink;
};

struct procListNode
{
   float arrivalTime;
   float startTime;
   float reStartTime;
   float finishTime;
   float serviceTime;
   float remainingTime;
   struct procListNode *pNext;
};

// Global Variables
int schedulerType;
int lambda;
float avgTs;
float quantum;
int stopCond = 10000;
float mu = 0.0;
float quantumClock;
eventQNode *eHead;
procListNode *pHead;
readyQNode *rHead;
cpuNode *cpuHead;
int countSomething = 0;

// Initializations
void insertIntoEventQ(eventQNode *);
float getResponseRatioValue(procListNode *);
procListNode *getSRTProcess();
procListNode *getHRRProcess();

// Take inputs from command line / script
void parseArgs(char *argv[])
{
   schedulerType = atoi(argv[1]);
   lambda = atoi(argv[2]);
   avgTs = (float)atof(argv[3]);
   quantum = (float)atof(argv[4]);
}

// Setting default values.
void init()
{
   mu = (float)1.0 / avgTs;
   quantumClock = 0.0;
   cpuHead = new cpuNode;
   cpuHead->clock = 0.0;
   cpuHead->cpuIsBusy = false;
   cpuHead->pLink = NULL;
   pHead = new procListNode;
   pHead->arrivalTime = genExp((float)lambda);
   pHead->startTime = 0.0;
   pHead->reStartTime = 0.0;
   pHead->finishTime = 0.0;
   pHead->serviceTime = genExp(mu);
   pHead->remainingTime = pHead->serviceTime;
   pHead->pNext = NULL;
   eHead = new eventQNode;
   eHead->time = pHead->arrivalTime;
   eHead->type = 1;
   eHead->eNext = NULL;
   eHead->pLink = pHead;
}

void run_sim()
{
   switch (schedulerType)
   {
   case 1:
      cout << "The sim is running FCFS. . . " << endl
           << endl;
      FCFS();
      break;
   case 2:
      cout << "The sim is running SRTF. . . " << endl
           << endl;
      SRTF();
      break;
   case 3:
      cout << "The sim is running HRRN. . . " << endl
           << endl;
      HRRN();
      break;
   case 4:
      cout << "The sim is running RR. . . " << endl
           << endl;
      RR();
      break;
   default:
      cout << "Error in run_sim(). . . " << endl;
   }
}

// First Come First Serve Service
void FCFS()
{
   int departureCount = 0;
   int arrivalCount = 0;
   int allocationCount = 0;

   while (departureCount < stopCond)
   {

      if (cpuHead->cpuIsBusy == false)
      {
         scheduleArrival();
         if (rHead != NULL)
         {
            scheduleAllocation();
         }
      }
      else
         scheduleDeparture();

      if (eHead->type == 1)
      {
         handleArrival();
         arrivalCount++;
      }
      else if (eHead->type == 2)
      {
         handleDeparture();
         departureCount++;
      }
      else if (eHead->type == 3)
      {
         handleAllocation();
         allocationCount++;
      }
   }
   cout << "Arrival Count: " << arrivalCount << endl;
   cout << "Departure Count: " << departureCount << endl;
   cout << "Allocation Count: " << allocationCount << endl;
}

// Shortest Remaining Time First
void SRTF()
{
   int arrivalCount = 0;
   int departureCount = 0;
   int allocationCount = 0;

   while (departureCount < stopCond)
   {

      if (arrivalCount < (stopCond * 1.20))
      {
         scheduleArrival();
         arrivalCount++;
      }

      if (cpuHead->cpuIsBusy == false)
      {
         if (rHead != NULL)
            scheduleAllocation();
      }
      else
      {
         if (eHead->type == 1)
         {

            if (eHead->time > cpuEstFinishTime())
            {
               scheduleDeparture();
            }
            else if (isPreemptive())
            {
               schedulePreemption();
            }
         }
      }

      if (eHead->type == 1)
         handleArrival();
      else if (eHead->type == 2)
      {
         handleDeparture();
         departureCount++;
      }
      else if (eHead->type == 3)
      {
         handleAllocation();
         allocationCount++;
      }
      else if (eHead->type == 4)
         handlePreemption();
   }
   cout << "Arrival Count: " << arrivalCount << endl;
   cout << "Departure Count: " << departureCount << endl;
   cout << "Allocation Count: " << allocationCount << endl;
}

// Highest Response Ratio Next
void HRRN()
{
   int departureCount = 0;
   while (departureCount < stopCond)
   {

      if (cpuHead->cpuIsBusy == false)
      {
         scheduleArrival();
         if (rHead != NULL)
         {
            scheduleAllocation();
         }
      }
      else
         scheduleDeparture();

      if (eHead->type == 1)
         handleArrival();
      else if (eHead->type == 2)
      {
         handleDeparture();
         departureCount++;
      }
      else if (eHead->type == 3)
         handleAllocation();
   }
}

// Round Robin Service
void RR()
{
   int arrivalCount = 0;
   int departureCount = 0;
   while (departureCount < stopCond)
   {

      if (arrivalCount < (stopCond * 1.20))
      {
         scheduleArrival();
         arrivalCount++;
      }

      if (cpuHead->cpuIsBusy == false)
      {
         scheduleArrival();
         if (rHead != 0)
         {
            scheduleQuantumAllocation();
         }
      }
      else
      {

         if (cpuEstFinishTime() < getNextQuantumClockTime())
         {
            scheduleQuantumDeparture();
         }
         else
         {
            if (rHead != 0)
            {
               if (rHead->pLink->arrivalTime > cpuEstFinishTime())
               {
                  scheduleQuantumDeparture();
               }
               else
               {
                  scheduleQuantumPreemption();
               }
            }
         }
      }

      if (eHead->type == 1)
         handleArrival();
      else if (eHead->type == 2)
      {
         handleQuantumDeparture();
         departureCount++;

         if (rHead != 0 && (rHead->pLink->arrivalTime < cpuHead->clock))
         {
            scheduleQuantumAllocation();
         }
      }
      else if (eHead->type == 3)
         handleQuantumAllocation();
      else if (eHead->type == 4)
         handleQuantumPreemption();
   }
}

float cpuEstFinishTime()
{
   float estFinish;
   float startTime = cpuHead->pLink->startTime;
   float reStartTime = cpuHead->pLink->reStartTime;
   float remainingTime = cpuHead->pLink->remainingTime;

   if (reStartTime == 0)
      estFinish = startTime + remainingTime;
   else
      estFinish = reStartTime + remainingTime;

   return estFinish;
}

bool isPreemptive()
{

   float cpuFinishTime = cpuEstFinishTime();
   float cpuRemainingTime = cpuFinishTime - eHead->time;

   if ((eHead->time < cpuFinishTime) && (eHead->pLink->remainingTime < cpuRemainingTime))
   {
      return true;
   }
   else
      return false;
}

void scheduleArrival()
{

   procListNode *pIt = pHead;
   while (pIt->pNext != NULL)
   {
      pIt = pIt->pNext;
   }
   pIt->pNext = new procListNode;
   pIt->pNext->arrivalTime = pIt->arrivalTime + genExp((float)lambda);
   pIt->pNext->startTime = 0.0;
   pIt->pNext->reStartTime = 0.0;
   pIt->pNext->finishTime = 0.0;
   pIt->pNext->serviceTime = genExp(mu);
   pIt->pNext->remainingTime = pIt->pNext->serviceTime;
   pIt->pNext->pNext = NULL;

   eventQNode *nuArrival = new eventQNode;
   nuArrival->time = pIt->pNext->arrivalTime;
   nuArrival->type = 1;
   nuArrival->pLink = pIt->pNext;
   nuArrival->eNext = NULL;

   insertIntoEventQ(nuArrival);
}

void handleArrival()
{

   readyQNode *nuReady = new readyQNode;
   nuReady->pLink = eHead->pLink;
   nuReady->rNext = NULL;

   if (rHead == NULL)
      rHead = nuReady;
   else
   {
      readyQNode *rIt = rHead;
      while (rIt->rNext != 0)
      {
         rIt = rIt->rNext;
      }
      rIt->rNext = nuReady;
   }

   popEventQHead();
}

void scheduleAllocation()
{

   eventQNode *nuAllocation = new eventQNode;

   procListNode *nextProc;
   if (schedulerType == 1)
      nextProc = rHead->pLink;
   else if (schedulerType == 2)
   {
      if (cpuHead->clock > rHead->pLink->arrivalTime)
      {
         nextProc = getSRTProcess();
      }
      else
      {
         nextProc = rHead->pLink;
      }
   }
   else if (schedulerType == 3)
   {
      nextProc = getHRRProcess();
   }

   if (cpuHead->clock < nextProc->arrivalTime)
   {
      nuAllocation->time = nextProc->arrivalTime;
   }
   else
   {
      nuAllocation->time = cpuHead->clock;
   }

   nuAllocation->type = 3;
   nuAllocation->eNext = NULL;
   nuAllocation->pLink = nextProc;

   insertIntoEventQ(nuAllocation);
}

void handleAllocation()
{

   cpuHead->pLink = eHead->pLink;

   if (schedulerType == 2 || schedulerType == 3)
   {

      readyQNode *rIt = rHead->rNext;
      readyQNode *rItPrev = rHead;
      if (rItPrev->pLink->arrivalTime != eHead->pLink->arrivalTime)
      {
         while (rIt != 0)
         {
            if (rIt->pLink->arrivalTime == eHead->pLink->arrivalTime)
            {
               rItPrev->rNext = rIt->rNext;
               rIt->rNext = rHead;
               rHead = rIt;
               break;
            }
            rIt = rIt->rNext;
            rItPrev = rItPrev->rNext;
         }
      }
   }

   popReadyQHead();
   popEventQHead();

   cpuHead->cpuIsBusy = true;

   if (cpuHead->clock < cpuHead->pLink->arrivalTime)
   {
      cpuHead->clock = cpuHead->pLink->arrivalTime;
   }

   if (cpuHead->pLink->startTime == 0)
   {
      cpuHead->pLink->startTime = cpuHead->clock;
   }
   else
   {
      cpuHead->pLink->reStartTime = cpuHead->clock;
   }
}

void scheduleDeparture()
{

   eventQNode *nuDeparture = new eventQNode;
   nuDeparture->type = 2;
   nuDeparture->eNext = 0;
   nuDeparture->pLink = cpuHead->pLink;

   if (schedulerType == 1 || schedulerType == 3)
   {
      nuDeparture->time = cpuHead->pLink->startTime + cpuHead->pLink->remainingTime;
   }
   else if (schedulerType == 2)
   {
      if (cpuHead->pLink->reStartTime == 0)
      {
         nuDeparture->time = cpuHead->pLink->startTime + cpuHead->pLink->remainingTime;
      }
      else
      {
         nuDeparture->time = cpuHead->pLink->reStartTime + cpuHead->pLink->remainingTime;
      }
   }

   insertIntoEventQ(nuDeparture);
}

void handleDeparture()
{

   cpuHead->clock = eHead->time;

   cpuHead->pLink->finishTime = cpuHead->clock;
   pHead->finishTime = cpuHead->pLink->finishTime;

   cpuHead->pLink->remainingTime = 0.0;
   cpuHead->pLink = NULL;

   cpuHead->cpuIsBusy = false;

   popEventQHead();
}

void schedulePreemption()
{
   eventQNode *nuPreemption = new eventQNode;
   nuPreemption->time = eHead->time;
   nuPreemption->type = 4;
   nuPreemption->eNext = 0;
   nuPreemption->pLink = eHead->pLink;

   popEventQHead();

   insertIntoEventQ(nuPreemption);
}

void handlePreemption()
{

   procListNode *preemptedProcPtr = cpuHead->pLink;

   cpuHead->pLink->remainingTime =
       cpuEstFinishTime() - eHead->time;

   cpuHead->pLink = eHead->pLink;
   cpuHead->clock = eHead->time;
   if (cpuHead->pLink->reStartTime == 0.0)
   {
      cpuHead->pLink->startTime = eHead->time;
   }
   else
   {
      cpuHead->pLink->reStartTime = eHead->time;
   }

   eventQNode *preemptedProcArrival = new eventQNode;
   preemptedProcArrival->time = eHead->time;
   preemptedProcArrival->type = 1;
   preemptedProcArrival->eNext = 0;
   preemptedProcArrival->pLink = preemptedProcPtr;

   popEventQHead();

   insertIntoEventQ(preemptedProcArrival);
}

void scheduleQuantumAllocation()
{

   eventQNode *nuAllocation = new eventQNode;

   procListNode *nextProc;
   nextProc = rHead->pLink;

   if (rHead != 0)
   {
      if (rHead->pLink->arrivalTime < cpuHead->clock)
      {
         nuAllocation->time = cpuHead->clock;
      }
      else
      {

         cpuHead->clock = rHead->pLink->arrivalTime;

         float nextQuantumTime = quantumClock;
         while (nextQuantumTime < cpuHead->clock)
         {
            nextQuantumTime += quantum;
         }
         quantumClock = nextQuantumTime;

         nuAllocation->time = getNextQuantumAllocationTime();
      }
   }
   else
   {
      cout << "Error in scheduleQuantumAllocation()" << endl;
   }

   nuAllocation->type = 3;
   nuAllocation->eNext = 0;
   nuAllocation->pLink = nextProc;

   insertIntoEventQ(nuAllocation);
}

void handleQuantumAllocation()
{

   cpuHead->pLink = eHead->pLink;

   cpuHead->cpuIsBusy = true;

   if (cpuHead->pLink->startTime == 0)
   {
      cpuHead->pLink->startTime = eHead->time;
   }
   else
   {
      cpuHead->pLink->reStartTime = eHead->time;
   }

   popReadyQHead();
   popEventQHead();
}

void scheduleQuantumDeparture()
{

   eventQNode *nuDeparture = new eventQNode;
   nuDeparture->type = 2;
   nuDeparture->eNext = 0;
   nuDeparture->pLink = cpuHead->pLink;

   if (cpuHead->pLink->reStartTime == 0)
   {
      nuDeparture->time = cpuHead->pLink->startTime + cpuHead->pLink->remainingTime;
   }
   else
   {
      nuDeparture->time = cpuHead->pLink->reStartTime + cpuHead->pLink->remainingTime;
   }

   insertIntoEventQ(nuDeparture);
}

void handleQuantumDeparture()
{

   cpuHead->pLink->finishTime = eHead->time;
   cpuHead->pLink->remainingTime = 0.0;
   cpuHead->pLink = 0;
   cpuHead->clock = eHead->time;
   cpuHead->cpuIsBusy = false;

   popEventQHead();
}

void scheduleQuantumPreemption()
{

   eventQNode *nuPreemption = new eventQNode;
   nuPreemption->type = 4;
   nuPreemption->eNext = 0;

   cpuHead->clock = rHead->pLink->arrivalTime;

   float nextQuantumTime = quantumClock;
   while (nextQuantumTime < cpuHead->clock)
   {
      nextQuantumTime += quantum;
   }
   quantumClock = nextQuantumTime;

   nuPreemption->time = getNextQuantumClockTime();

   nuPreemption->pLink = rHead->pLink;

   insertIntoEventQ(nuPreemption);
}

void handleQuantumPreemption()
{

   procListNode *preemptedProcPtr = cpuHead->pLink;

   cpuHead->pLink->remainingTime = cpuEstFinishTime() - eHead->time;

   cpuHead->pLink = eHead->pLink;
   cpuHead->clock = eHead->time;
   if (cpuHead->pLink->startTime == 0.0)
   {
      cpuHead->pLink->startTime = eHead->time;
   }
   else
   {
      cpuHead->pLink->reStartTime = eHead->time;
   }

   float nextQuantumTime = quantumClock;
   while (nextQuantumTime < eHead->time)
   {
      nextQuantumTime += quantum;
   }
   quantumClock = nextQuantumTime;

   eventQNode *preemptedProcArrival = new eventQNode;
   preemptedProcArrival->time = eHead->time;
   preemptedProcArrival->type = 1;
   preemptedProcArrival->eNext = 0;
   preemptedProcArrival->pLink = preemptedProcPtr;

   popEventQHead();

   popReadyQHead();

   insertIntoEventQ(preemptedProcArrival);
}

float getNextQuantumClockTime()
{
   return quantumClock + quantum;
}

float getNextQuantumAllocationTime()
{
   float nextQuantumTime = quantumClock;
   while (nextQuantumTime < rHead->pLink->arrivalTime)
   {
      nextQuantumTime += quantum;
   }
   return nextQuantumTime;
}

float smallrand()
{

   return ((float)rand() / RAND_MAX);
}

// Generating random values
float genExp(float val)
{
   float u, y;
   y = 0;
   while (y == 0)
   {
      u = smallrand();
      y = (-1 / val) * log(u);
   }
   return y;
}
// Helper Function
void insertIntoEventQ(eventQNode *nuEvent)
{

   if (eHead == 0)
      eHead = nuEvent;
   else if (eHead->time > nuEvent->time)
   {
      nuEvent->eNext = eHead;
      eHead = nuEvent;
   }
   else
   {
      eventQNode *eIt = eHead;
      while (eIt != 0)
      {
         if ((eIt->time < nuEvent->time) && (eIt->eNext == 0))
         {
            eIt->eNext = nuEvent;
            break;
         }
         else if ((eIt->time < nuEvent->time) && (eIt->eNext->time > nuEvent->time))
         {
            nuEvent->eNext = eIt->eNext;
            eIt->eNext = nuEvent;
            break;
         }
         else
         {
            eIt = eIt->eNext;
         }
      }
   }
}
// Helper Function
void popEventQHead()
{
   eventQNode *tempPtr = eHead;
   eHead = eHead->eNext;
   delete tempPtr;
}

// Helper Function
void popReadyQHead()
{
   readyQNode *tempPtr = rHead;
   rHead = rHead->rNext;
   delete tempPtr;
}

procListNode *getSRTProcess()
{

   readyQNode *rIt = rHead;
   procListNode *srtProc = rIt->pLink;
   float srt = rIt->pLink->remainingTime;
   while (rIt != 0)
   {
      if (rIt->pLink->remainingTime < srt)
      {
         srt = rIt->pLink->remainingTime;
         srtProc = rIt->pLink;
      }
      rIt = rIt->rNext;
   }
   return srtProc;
}

procListNode *getHRRProcess()
{
   readyQNode *rIt = rHead;
   procListNode *hrrProc = rIt->pLink;
   float hrr = getResponseRatioValue(hrrProc);

   while (rIt != 0)
   {
      if (getResponseRatioValue(rIt->pLink) > hrr)
      {
         hrr = getResponseRatioValue(rIt->pLink);
         hrrProc = rIt->pLink;
      }
      rIt = rIt->rNext;
   }

   return hrrProc;
}

// HRRN Helper Function
float getResponseRatioValue(procListNode *thisProc)
{
   float HRR = ((cpuHead->clock - thisProc->arrivalTime) + thisProc->serviceTime) / thisProc->serviceTime;
   return HRR;
}

// Generation Functions
float getAvgTurnaroundTime()
{
   float totTurnaroundTime = 0.0;
   float totalServicetime = 0.0;
   int count = 0;
   int count2 = 0;
   procListNode *pIt = pHead;
   while (pIt->pNext != NULL)
   {

      if (pIt->finishTime == 0)
      {

         count2++;
      }
      else
      {
         totTurnaroundTime += (pIt->finishTime - pIt->arrivalTime);
         count++;
      }

      totalServicetime += pIt->serviceTime;

      pIt = pIt->pNext;
   }
   return (totTurnaroundTime / stopCond);
}

float getTotalThroughput()
{
   procListNode *pIt = pHead;
   float finTime = 0.0;
   int count = 0;

   while (pIt->pNext != NULL)
   {

      if (pIt->finishTime == 0)
      {
         count++;
      }
      else
      {
         finTime = pIt->finishTime;
      }
      pIt = pIt->pNext;
   }
   cout << "totalTime: " << finTime << endl;
   return ((float)stopCond / finTime);
}

float getCpuUtil()
{
   procListNode *pIt = pHead;
   float busyTime = 0.0;
   float finTime = 0.0;
   int count = 0;
   while (pIt->pNext != NULL)
   {
      if (pIt->finishTime == 0)
      {
         count++;
      }
      else
      {
         busyTime += pIt->serviceTime;
         finTime = pIt->finishTime;
      }
      pIt = pIt->pNext;
   }
   cout << "Busy Time: " << busyTime << endl;
   cout << "finTime: " << finTime << endl;
   cout << "number of 0 finish time's in CPU util: " << count << endl;
   return (busyTime / finTime);
}

float getAvgNumProcInQ()
{

   float timeNmin1 = 0.0;
   int count = 0;
   procListNode *pIt = pHead;
   while (pIt->pNext != NULL)
   {
      if (pIt->finishTime == 0)
      {
         count++;
      }
      else
      {
         timeNmin1 = pIt->finishTime;
      }
      pIt = pIt->pNext;
   }
   int timeN = static_cast<int>(timeNmin1) + 1;

   pIt = pHead;
   int time = 0;
   ;
   int numProcsInQ = 0;
   for (time = 0; time < timeN; time++)
   {
      while (pIt->finishTime != 0)
      {
         if ((pIt->arrivalTime < time && pIt->startTime > time) ||
             (pIt->arrivalTime > time && pIt->arrivalTime < (time + 1)))
         {
            numProcsInQ++;
         }
         pIt = pIt->pNext;
      }
      pIt = pHead;
   }

   return ((float)numProcsInQ / timeN);
}

void generate_report()
{
   string scheduler;

   if (schedulerType == 1)
      scheduler = "FCFS()";
   else if (schedulerType == 2)
      scheduler = "SRTF()";
   else if (schedulerType == 3)
      scheduler = "HRRN()";
   else if (schedulerType == 4)
      scheduler = "RR()";

   if (lambda == 1)
   {
      ofstream report("report.txt", ios::out | ios::app);
      report << endl
             << "Scheduler \tLambda \t\tAvgTs\t AvgTurnaround \tTotalThruput\tCPU Util\tAvg#ProcsInQ \tQuantum" << endl
             << "---------------------------------------------------------------------------------------------------------------"
             << endl;
   }

   ofstream report("report.txt", ios::out | ios::app);
   report << scheduler << "\t\t"
          << setprecision(7)
          << lambda << "     \t\t"
          << avgTs << "\t"
          << getAvgTurnaroundTime() << "\t"
          << getTotalThroughput() << "\t"
          << getCpuUtil() << "\t"
          << getAvgNumProcInQ() << "\t"
          << quantum
          << endl;
   report.close();
   cout << endl
        << "Program completed. "
        << "Results written to <report.txt> in the .exe folder" << endl;
}