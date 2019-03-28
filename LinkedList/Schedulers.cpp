 /* Schedulers.cpp
 In this project, we are going to build a discrete-time event
 simulator for a number of CPU schedulers on a single CPU system.
 The goal of this project is to compare and assess the impact of
 different schedulers on different performance metrics, and across multiple workloads.
 @authors: John Daloni, Jamal Rasool, Kristof York, Fernando Valdes, Elliot Esponda
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

struct cpuNode{
   float clock;                   
   bool cpuIsBusy;                
   struct procListNode* pLink;    
};

struct readyQNode{
   struct procListNode* pLink;    
   struct readyQNode* rNext;      
};

struct eventQNode{
   float time;
   int type;                      
                                  
   struct eventQNode* eNext;      
   struct procListNode* pLink;    
};

struct procListNode{
   float arrivalTime;
   float startTime;
   float reStartTime;
   float finishTime;
   float serviceTime;
   float remainingTime;
   struct procListNode* pNext;    
};


int schedulerType;               
int lambda;                      
float avgTs;                     
float quantum;                   
int stopCond = 10000;           
float mu;                        
float quantumClock;              
eventQNode* eHead;               
procListNode* pHead;             
readyQNode* rHead;               
cpuNode* cpuHead;                


void insertIntoEventQ(eventQNode*);
float getResponseRatioValue(procListNode*);
procListNode* getSRTProcess();
procListNode* getHRRProcess();




void parseArgs(char *argv[]){
   schedulerType = atoi( argv[1] );
   lambda = atoi( argv[2] );
   avgTs = (float)atof( argv[3] );
   quantum = (float)atof( argv[4] );
}


void init(){
   
   mu = (float)1.0/avgTs;

   
   quantumClock = 0.0;

   
   cpuHead = new cpuNode;
   cpuHead->clock = 0.0;
   cpuHead->cpuIsBusy = 0;   
   cpuHead->pLink = 0;

   
   
   pHead = new procListNode;
   pHead->arrivalTime = genExp((float)lambda);
   pHead->startTime = 0.0;
   pHead->reStartTime = 0.0;
   pHead->finishTime = 0.0;
   pHead->serviceTime = genExp(mu);
   pHead->remainingTime = pHead->serviceTime;
   pHead->pNext = 0;

   
   eHead = new eventQNode;
   eHead->time = pHead->arrivalTime;
   eHead->type = 1;
   eHead->eNext = 0;
   eHead->pLink = pHead;
}

void run_sim(){
   switch ( schedulerType ){
     case 1:
        cout << "The sim is running FCFS. . . " << endl;
        FCFS();
        break;
     case 2:
        cout << "The sim is running SRTF. . . " << endl;
        SRTF();
        break;
     case 3:
        cout << "The sim is running HRRN. . . " << endl;
        HRRN();
        break;
     case 4:
        cout << "The sim is running RR. . . " << endl;
        RR();
        break;
     default:
        cout << "Error in run_sim(). . . " << endl;
   }
}

void FCFS(){
   int departureCount = 0;
   while( departureCount < stopCond ){
      
      if( cpuHead->cpuIsBusy == false ){
         scheduleArrival();
         if( rHead != 0 ){
            scheduleAllocation();
         }
		  }
      
      else scheduleDeparture();

      
      if( eHead->type == 1 ) handleArrival();
      else if( eHead->type == 2 ){
         handleDeparture();
         departureCount++;
      }
      else if( eHead->type == 3 ) handleAllocation();
   } 
}

void SRTF(){
   int arrivalCount = 0;
   int departureCount = 0;
   while( departureCount < stopCond ){
      
      if( arrivalCount < ( stopCond * 1.20 ) ){
         scheduleArrival();
         arrivalCount++;
      }
      
      if( cpuHead->cpuIsBusy == false ){
         if( rHead != 0 ) scheduleAllocation();
      }
      
      else{
         
         if( eHead->type == 1 ){
            
            if( eHead->time > cpuEstFinishTime() ){
               scheduleDeparture();
            }
            
            else if( isPreemptive() ){
               schedulePreemption();
            }
         }
      }
      
      if( eHead->type == 1) handleArrival();
      else if( eHead->type == 2 ){
         handleDeparture();
         
         departureCount++;
      }
      else if( eHead->type == 3 ) handleAllocation();
      else if( eHead->type == 4 ) handlePreemption();
   } 
}

void HRRN(){
   int departureCount = 0;
   while( departureCount < stopCond ){
      
      if( cpuHead->cpuIsBusy == false ){
         scheduleArrival();
         if( rHead != 0 ){
            scheduleAllocation(); 
         }
       }
       
       else scheduleDeparture();

       
       if( eHead->type == 1 ) handleArrival();
       else if( eHead->type == 2 ){
          handleDeparture();
          departureCount++;
       }
       else if( eHead->type == 3 ) handleAllocation();
   } 
}

void RR(){
   int arrivalCount = 0;
   int departureCount = 0;
   while( departureCount < stopCond ){
      
      if( arrivalCount < ( stopCond * 1.20 ) ){
         scheduleArrival();
         arrivalCount++;
      }
      
      if( cpuHead->cpuIsBusy == false ){
         scheduleArrival();
         if( rHead != 0 ){
            scheduleQuantumAllocation();
         }
      }
      
      else{
         
         if( cpuEstFinishTime() < getNextQuantumClockTime() ){
            scheduleQuantumDeparture();
         }
         else{
            if( rHead != 0 ){
               if( rHead->pLink->arrivalTime > cpuEstFinishTime() ){
                  scheduleQuantumDeparture();
               }
               else{
                  scheduleQuantumPreemption();
               }
            }
         }
      }
   
   if( eHead->type == 1 ) handleArrival();
   else if( eHead->type == 2 ){
      handleQuantumDeparture();
      departureCount++;

      
      
      if( rHead != 0 && ( rHead->pLink->arrivalTime <
                          cpuHead->clock) ){
         scheduleQuantumAllocation();
      }
   }
   else if( eHead->type == 3 ) handleQuantumAllocation();
   else if( eHead->type == 4 ) handleQuantumPreemption();
   } 
}

float cpuEstFinishTime(){
   float estFinish;
   float startTime = cpuHead->pLink->startTime;
   float reStartTime = cpuHead->pLink->reStartTime;
   float remainingTime = cpuHead->pLink->remainingTime;

   if( reStartTime == 0 ) estFinish = startTime + remainingTime;
   else estFinish = reStartTime + remainingTime;

   return estFinish;
}

bool isPreemptive(){
   
   float cpuFinishTime = cpuEstFinishTime();

   
   float cpuRemainingTime = cpuFinishTime - eHead->time;

   
   
   if( ( eHead->time < cpuFinishTime ) &&
       ( eHead->pLink->remainingTime <
         cpuRemainingTime ) ){
      return true;
   }
   else return false;
}



void scheduleArrival(){
   
   procListNode* pIt = pHead;
   while( pIt->pNext !=0 ){
      pIt = pIt->pNext;
   }
   pIt->pNext = new procListNode;
   pIt->pNext->arrivalTime = pIt->arrivalTime + genExp((float)lambda);
   pIt->pNext->startTime = 0.0;
   pIt->pNext->reStartTime = 0.0;
   pIt->pNext->finishTime = 0.0;
   pIt->pNext->serviceTime = genExp(mu);
   pIt->pNext->remainingTime = pIt->pNext->serviceTime;
   pIt->pNext->pNext = 0;

   
   eventQNode* nuArrival = new eventQNode;
   nuArrival->time = pIt->pNext->arrivalTime;
   nuArrival->type = 1;
   nuArrival->pLink = pIt->pNext;
   nuArrival->eNext = 0;

   
   insertIntoEventQ(nuArrival);
}


void handleArrival(){
   
   readyQNode* nuReady = new readyQNode;
   nuReady->pLink = eHead->pLink;
   nuReady->rNext = 0;

   
   if( rHead == 0 ) rHead = nuReady;
   else{
      readyQNode* rIt = rHead;
      while( rIt->rNext != 0 ){
         rIt = rIt->rNext;
      }
      rIt->rNext = nuReady;
   }

   
   popEventQHead();
}


void scheduleAllocation(){
   
   eventQNode* nuAllocation = new eventQNode;

   
   procListNode* nextProc;
   if( schedulerType == 1 ) nextProc = rHead->pLink;          
   else if( schedulerType == 2 ){			      
      if( cpuHead->clock > rHead->pLink->arrivalTime ){
         nextProc = getSRTProcess();
      }
      else{
         nextProc = rHead->pLink;
      }
   }
   else if( schedulerType == 3 ){                             
      nextProc = getHRRProcess();
   }

   
   if( cpuHead->clock < nextProc->arrivalTime ){
      nuAllocation->time = nextProc->arrivalTime;
   }
   else{
      nuAllocation->time = cpuHead->clock;
   }

   
   nuAllocation->type = 3;
   nuAllocation->eNext = 0;
   nuAllocation->pLink = nextProc;

   
   insertIntoEventQ( nuAllocation );
}


void handleAllocation(){
   
   cpuHead->pLink = eHead->pLink;

   if( schedulerType == 2 ||      
      schedulerType == 3 ){       
      
      
      readyQNode* rIt = rHead->rNext;
      readyQNode* rItPrev = rHead;
      if( rItPrev->pLink->arrivalTime != eHead->pLink->arrivalTime ){
         while( rIt != 0 ){
	    if( rIt->pLink->arrivalTime ==
		   eHead->pLink->arrivalTime ){
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

   
   if( cpuHead->clock < cpuHead->pLink->arrivalTime ){
      
      cpuHead->clock = cpuHead->pLink->arrivalTime;
   }

   
   if( cpuHead->pLink->startTime == 0 ){
      cpuHead->pLink->startTime = cpuHead->clock;
   }
   else{
      cpuHead->pLink->reStartTime = cpuHead->clock;
   }
}


void scheduleDeparture(){
   
   eventQNode* nuDeparture = new eventQNode;
   nuDeparture->type = 2;
   nuDeparture->eNext = 0;
   nuDeparture->pLink = cpuHead->pLink;

   
   if( schedulerType == 1 ||                  
       schedulerType == 3 ){                  
          nuDeparture->time =
	     cpuHead->pLink->startTime +
             cpuHead->pLink->remainingTime;
   }
   else if( schedulerType == 2 ){             
      if( cpuHead->pLink->reStartTime == 0 ){
         nuDeparture->time =
            cpuHead->pLink->startTime +
            cpuHead->pLink->remainingTime;
      }
      else{
      nuDeparture->time =
         cpuHead->pLink->reStartTime +
         cpuHead->pLink->remainingTime;
      }
   }

   
   insertIntoEventQ(nuDeparture);
}


void handleDeparture(){
   
   cpuHead->pLink->finishTime = eHead->time;
	 cpuHead->pLink->remainingTime = 0.0;
   cpuHead->pLink = 0;
   cpuHead->clock = eHead->time;
   cpuHead->cpuIsBusy = false;

   
   popEventQHead();
}


void schedulePreemption(){
   eventQNode* nuPreemption = new eventQNode;
   nuPreemption->time = eHead->time;
   nuPreemption->type = 4;
   nuPreemption->eNext = 0;
   nuPreemption->pLink = eHead->pLink;

   
   
   popEventQHead();

   
   insertIntoEventQ( nuPreemption );
}


void handlePreemption(){
   
   procListNode* preemptedProcPtr = cpuHead->pLink;

   
   cpuHead->pLink->remainingTime =
      cpuEstFinishTime() - eHead->time;

   
   cpuHead->pLink = eHead->pLink;
   cpuHead->clock = eHead->time;
   if( cpuHead->pLink->reStartTime == 0.0  ){
      cpuHead->pLink->startTime = eHead->time;
   }
   else{
      cpuHead->pLink->reStartTime = eHead->time;
   }

   
   eventQNode* preemptedProcArrival = new eventQNode;
   preemptedProcArrival->time = eHead->time;
   preemptedProcArrival->type = 1;
   preemptedProcArrival->eNext = 0;
   preemptedProcArrival->pLink = preemptedProcPtr;

   
   popEventQHead();

   
   insertIntoEventQ( preemptedProcArrival );
}

void scheduleQuantumAllocation(){
   
   eventQNode* nuAllocation = new eventQNode;

   
   procListNode* nextProc;
   nextProc = rHead->pLink;

   
   if( rHead != 0 ){
      if( rHead->pLink->arrivalTime < cpuHead->clock ){
         nuAllocation->time = cpuHead->clock;
      }
      else{
         
         cpuHead->clock = rHead->pLink->arrivalTime;

         
         float nextQuantumTime = quantumClock;
         while( nextQuantumTime < cpuHead->clock ){
            nextQuantumTime += quantum;
         }
         quantumClock = nextQuantumTime;

         
         nuAllocation->time = getNextQuantumAllocationTime();
      }
   }
   else{
      cout << "Error in scheduleQuantumAllocation()" << endl;
   }

   
   nuAllocation->type = 3;
   nuAllocation->eNext = 0;
   nuAllocation->pLink = nextProc;

   
   insertIntoEventQ( nuAllocation );
}

void handleQuantumAllocation(){
   
   cpuHead->pLink = eHead->pLink;

   
   cpuHead->cpuIsBusy = true;

   
   if( cpuHead->pLink->startTime == 0 ){
      cpuHead->pLink->startTime = eHead->time;
   }
   else{
      cpuHead->pLink->reStartTime = eHead->time;
   }

   
   popReadyQHead();
   popEventQHead();
}

void scheduleQuantumDeparture(){
   
   eventQNode* nuDeparture = new eventQNode;
   nuDeparture->type = 2;
   nuDeparture->eNext = 0;
   nuDeparture->pLink = cpuHead->pLink;

   
   if( cpuHead->pLink->reStartTime == 0 ){
      nuDeparture->time =
         cpuHead->pLink->startTime +
         cpuHead->pLink->remainingTime;
   }
   else{
      nuDeparture->time =
         cpuHead->pLink->reStartTime +
         cpuHead->pLink->remainingTime;
   }

   
   insertIntoEventQ(nuDeparture);
}

void handleQuantumDeparture(){
   
   cpuHead->pLink->finishTime = eHead->time;
      cpuHead->pLink->remainingTime = 0.0;
   cpuHead->pLink = 0;
   cpuHead->clock = eHead->time;
   cpuHead->cpuIsBusy = false;

   
   popEventQHead();
}

void scheduleQuantumPreemption(){
   
   eventQNode* nuPreemption = new eventQNode;
   nuPreemption->type = 4;
   nuPreemption->eNext = 0;

   
   cpuHead->clock = rHead->pLink->arrivalTime;

   
   float nextQuantumTime = quantumClock;
   while( nextQuantumTime < cpuHead->clock ){
      nextQuantumTime += quantum;
   }
   quantumClock = nextQuantumTime;

   
   nuPreemption->time = getNextQuantumClockTime();

   
   nuPreemption->pLink = rHead->pLink;

   
   insertIntoEventQ( nuPreemption );
}

void handleQuantumPreemption(){
   
   procListNode* preemptedProcPtr = cpuHead->pLink;

   
   cpuHead->pLink->remainingTime =
      cpuEstFinishTime() - eHead->time;

   
   cpuHead->pLink = eHead->pLink;
   cpuHead->clock = eHead->time;
   if( cpuHead->pLink->startTime == 0.0  ){
      cpuHead->pLink->startTime = eHead->time;
   }
   else{
      cpuHead->pLink->reStartTime = eHead->time;
   }

   
   float nextQuantumTime = quantumClock;
   while( nextQuantumTime < eHead->time  ){
      nextQuantumTime += quantum;
   }
   quantumClock = nextQuantumTime;

   
   eventQNode* preemptedProcArrival = new eventQNode;
   preemptedProcArrival->time = eHead->time;
   preemptedProcArrival->type = 1;
   preemptedProcArrival->eNext = 0;
   preemptedProcArrival->pLink = preemptedProcPtr;

   
   popEventQHead();

   
   popReadyQHead();

   
   insertIntoEventQ( preemptedProcArrival );
}

float getNextQuantumClockTime(){
   return quantumClock + quantum;
}

float getNextQuantumAllocationTime(){
   float nextQuantumTime = quantumClock;
   while( nextQuantumTime < rHead->pLink->arrivalTime  ){
      nextQuantumTime += quantum;
   }
   return nextQuantumTime;
}





float urand(){
   srand (time(NULL));
   return( (float) rand() / RAND_MAX );
}


float genExp(float val){
   float u, x;
   x = 0;
   while( x == 0 ){
      u = urand();
      x = (-1/val)*log(u);
   }
   return x;
}

void insertIntoEventQ( eventQNode* nuEvent ){
   
   if( eHead == 0 ) eHead = nuEvent;
   else if( eHead->time > nuEvent->time ){
      nuEvent->eNext = eHead;
      eHead = nuEvent;
   }
   else{
      eventQNode* eIt = eHead;
      while( eIt != 0 ){
         if( (eIt->time < nuEvent->time) && (eIt->eNext == 0) ){
            eIt->eNext = nuEvent;
	    break;
         }
         else if( (eIt->time < nuEvent->time) &&
                  (eIt->eNext->time > nuEvent->time)){
            nuEvent->eNext = eIt->eNext;
            eIt->eNext = nuEvent;
            break;
         }
         else{
            eIt = eIt->eNext;
         }
      }
   }
}

void popEventQHead(){
   eventQNode* tempPtr = eHead;
   eHead = eHead->eNext;
   delete tempPtr;
}

void popReadyQHead(){
   readyQNode* tempPtr = rHead;
   rHead = rHead->rNext;
   delete tempPtr;
}

procListNode* getSRTProcess(){
   
   readyQNode* rIt = rHead;
   procListNode* srtProc = rIt->pLink;
   float srt = rIt->pLink->remainingTime;
   while( rIt != 0){
      if( rIt->pLink->remainingTime < srt ){
          srt = rIt->pLink->remainingTime;
	        srtProc = rIt->pLink;
      }
      rIt = rIt->rNext;
   }
   return srtProc;
}

procListNode* getHRRProcess(){
   readyQNode* rIt = rHead;
   procListNode* hrrProc = rIt->pLink;
   float hrr = getResponseRatioValue( hrrProc );

   while( rIt != 0){
      if( getResponseRatioValue( rIt->pLink ) > hrr ){
         hrr = getResponseRatioValue( rIt->pLink );
	 hrrProc = rIt->pLink;
      }
      rIt = rIt->rNext;
   }
   return hrrProc;
}

float getResponseRatioValue( procListNode* thisProc ){
   float HRR = ( ( cpuHead->clock -
                   thisProc->arrivalTime ) +
		   thisProc->serviceTime ) /
		   thisProc->serviceTime;
   return HRR;
}



float getAvgTurnaroundTime(){
   float totTurnaroundTime = 0.0;
   procListNode* pIt = pHead;
   while( pIt->finishTime != 0 ){
      
      totTurnaroundTime +=
         ( pIt->finishTime - pIt->arrivalTime );
      pIt = pIt->pNext;
   }
   return (totTurnaroundTime/stopCond);
}

float getTotalThroughput(){
   procListNode* pIt = pHead;
   float finTime = 0.0;
   while( pIt->finishTime != 0 ){
      
      if( pIt->pNext->finishTime == 0 ) {
         finTime = pIt->finishTime;
      }
      pIt = pIt->pNext;
   }
   return ( (float)stopCond / finTime );
}

float getCpuUtil(){
   procListNode* pIt = pHead;
   float busyTime = 0.0;
   float finTime = 0.0;
   while( pIt->finishTime != 0 ){
      busyTime += pIt->serviceTime;
      if( pIt->pNext->finishTime == 0 )
         finTime = pIt->finishTime;
      pIt = pIt->pNext;
   }
   return ( busyTime / finTime );
}

float getAvgNumProcInQ(){
   
   
   float timeNmin1 = 0.0;
   procListNode* pIt = pHead;
   while( pIt->finishTime != 0 ){
      if( pIt->pNext->finishTime == 0 )
         timeNmin1 = pIt->finishTime;
      pIt = pIt->pNext;
   }
   int timeN = static_cast<int>(timeNmin1) + 1;

   
   
   pIt = pHead;
   int time = 0;;
   int numProcsInQ = 0;
   for( time = 0; time < timeN; time++ ){
      while( pIt->finishTime != 0 ){
         if( ( pIt->arrivalTime < time && pIt->startTime > time ) ||
             ( pIt->arrivalTime > time && pIt->arrivalTime < (time + 1) ) ){
            numProcsInQ ++;
         }
         pIt = pIt->pNext;
     }
     pIt = pHead;
   }

   return ( (float)numProcsInQ / timeN );
}

void generate_report(){
	string scheduler;

	if( schedulerType == 1 )      scheduler = "FCFS()";
   else if( schedulerType == 2 ) scheduler = "SRTF()";
   else if( schedulerType == 3 ) scheduler = "HRRN()";
   else if( schedulerType == 4 ) scheduler = "RORO()";

   ofstream report ( "report.txt", ios::out | ios::app );

   if( lambda == 1 ){
      report << endl
          << "Scheduler \tLambda \t\tAvgTs\t AvgTurnaround \tTotalThruput\tCPU Util\tAvg#ProcsInQ \tQuantum" << endl
          << "---------------------------------------------------------------------------------------------------------------"
          << endl;
      report.close();
   }

   report << scheduler << "\t\t"
          << setprecision(7)
          << lambda << "     \t\t"
          << avgTs  << "\t"
          << getAvgTurnaroundTime() << "\t"
          << getTotalThroughput() << "\t"
          << getCpuUtil() << "\t"
          << getAvgNumProcInQ() << "\t"
			    << quantum
          << endl;
   report.close();
   
	cout << endl << "Program completed. "
        << "Results written to <report.txt> in the .exe folder" << endl;
}
