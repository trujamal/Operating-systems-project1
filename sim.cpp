#include "process.cpp"  // user defined process class
#include <vector>       // used for queueing
#include <algorithm>    // used for sort();
#include <sstream>
#include <queue>
#include <iomanip>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <fstream>
using namespace std;

// events
#define ARRIVAL 1
#define DEPARTURE 2
#define QUANTUM 3
     
// function definition
void init();
int run_sim(int scheduler);
void generate_report();
void schedule_event();
int processArrival(struct event* eve);
int processDeparture(struct event* eve);
float genexp(float lambda);
void simFCFS();   // first come first serve
void simSRTF();   // shortest remaing time first 
void simHRRN();   // highest response ratio next
void simRR();     // round robin

//Global variables
bool cpuBusy;
float turnaround;
float utilization;
float throughput;
float avg_proc_in_Q;
float simClock; // simulation clock
float avgServiceTime;
float lambda;
float sumServiceTime;
float sumWait;
float sumArrivalRate;
int scheduler;
int quantum;
int processCount = 0;
int endSimulation = 10000; // how many processes to finish before end sim
vector <process> eventQ;


void init()
{
    // initialize all variables, states, and end conditions
    // schedule first events
    simClock = 0;
    sumServiceTime = 0;
    quantum = 0;
    sumWait = 0;
    sumArrivalRate = 0;
    cpuBusy = false;

    for(int i = 0; i < 3; i++)
    {
        float randServiceTime = genexp(1/avgServiceTime);
        process temp(randServiceTime, 0, ++processCount, ARRIVAL);
        eventQ.push_back(temp);
    }
}

void generate_report()
{
    float avgLambda = processCount/sumArrivalRate;
    // output statistics
    turnaround = (sumServiceTime+sumWait)/endSimulation;
    throughput = endSimulation/simClock;
    utilization = (processCount/sumArrivalRate) / (endSimulation/simClock);
    avg_proc_in_Q = (turnaround*avgLambda - avgLambda*(sumServiceTime/endSimulation))/avgLambda;
    cout << "Total Clock: " << simClock << endl;
    cout << "Turnaround Time: " << turnaround << " Total Throughput: " << throughput << endl;
    cout << "CPU Utilization: " << utilization << " or " << utilization * 100 << "% Avg. process in Queue: " << avg_proc_in_Q << endl;

    cout<<"avgLambda: "<<avgLambda<<endl;
    cout<<"sumServiceTime: "<<sumServiceTime<<endl;
    cout<<"sumWait: "<<sumWait<<endl;
    float turnTime = (sumServiceTime+sumWait)/endSimulation;
    cout<<"turnTime: "<<turnTime<<endl;
    ofstream ofs;
    ofs.open ("sim.data", std::ofstream::out | std::ofstream::app);

    ofs << lambda << "," << turnaround << "," << throughput << "," << utilization << "," << avg_proc_in_Q << std::endl;
   
    ofs.close();
}
 
//schedules an event in the future
void schedule_event()
{   // insert event in the event queue in its order of time

    // generate random service time and arrival time
    float randServiceTime = genexp(1/avgServiceTime);
    float randArrivalTime = genexp(lambda);

    sumArrivalRate += randArrivalTime;

    //set new event with serviceTime, arrivalTime, pid, processType
    process temp(randServiceTime, 
            simClock + randArrivalTime, 
            ++processCount, 
            ARRIVAL);
    eventQ.push_back(temp);
}

// returns a random number between 0 and 1
float urand()
{
    return( (float) rand()/RAND_MAX );
}

// returns a random number that follows an exp distribution
float genexp(float lambda)
{
    float u,x;
    x = 0;
    while (x == 0)
    {
        u = urand();
        x = (-1/lambda)*log(u);
    }
    return(x);
}

int run_sim(int scheduler)
{
    int pCount = 0; // number of completed process's

    switch (scheduler)
    {
        case 1:
            simFCFS();  // first come first serve
            break;
        case 2:
            simSRTF();  // shortest remaining time first
            break;
        case 3:
            simHRRN();  // highest response ratio next ((wait+burst)/burst)
            break;
        case 4:
            simRR();    // round robin
            break;
        default:
            cout<<"improper scheduler input (1-4 requested)"<<endl
                <<"1) First Come First Serve"<<endl
                <<"2) Shortest Remaining Time First"<<endl
                <<"3) Highest Response Ratio Next"<<endl
                <<"4) Round Robin"<<endl;
            break;
    }
    return 0;
}

void simFCFS()    // first come first serve
{
    vector<process> readyQ;
    int pCount = 0;
    unsigned int eqSize = eventQ.size();
    while (pCount < endSimulation)
    {
        sort(eventQ.begin(), eventQ.end(), sorter3);

        switch (eventQ.front().get_type())
        {
            case ARRIVAL:
                simClock = eventQ.front().get_arrival();
                schedule_event();
                
                if (cpuBusy == false) // process event, push departure
                {
                    cpuBusy = true;
                    eventQ.front().set_type(DEPARTURE);
                    eventQ.front().set_arrival(simClock + eventQ.front().get_serviceTime());
                }
                else
                {
                    readyQ.push_back(eventQ.front());
                    eventQ.erase(eventQ.begin());
                }

                break;
            case DEPARTURE:
                simClock = eventQ.front().get_arrival();
                
                if(!readyQ.empty())
                {
                    readyQ.front().been_seen(simClock - readyQ.front().get_arrival());
                    sumWait += readyQ.front().get_totalWait();
                }

                sumServiceTime += eventQ.front().get_serviceTime();
                eventQ.erase(eventQ.begin());
 
                if(readyQ.empty())
                    cpuBusy = false;
                else
                {
                    readyQ.front().set_type(DEPARTURE);
                    readyQ.front().set_arrival(simClock + readyQ.front().get_serviceTime());

                    eventQ.push_back(readyQ.front());
                    readyQ.erase(readyQ.begin());
                }

                pCount++;

                break;
            default:
            	cout << "Please check your input." << endl;
                break;
        }
    }
}

void simSRTF()    // shortest remaing time first 
{
	vector<process> readyQ;
    int pCount = 0;
    unsigned int eqSize = eventQ.size();
    while (pCount < endSimulation)
    {
    	sort(eventQ.begin(), eventQ.end(), sorter3);

    	switch (eventQ.front().get_type())
        {
        	case ARRIVAL:

            break;
        	case DEPARTURE:
             
            break;
        	default:
        		cout << "Please check your input." << endl;
            break;
        }

    }
}

void simHRRN()    // highest response ratio next
{
    vector<process> readyQ;
    int pCount = 0;
    unsigned int eqSize = eventQ.size();
    while (pCount < endSimulation)
    {
        sort(eventQ.begin(), eventQ.end(), sorter3);

        switch (eventQ.front().get_type())
        {
            case ARRIVAL:
                simClock = eventQ.front().get_arrival();
                schedule_event();
                
                if (cpuBusy == false) // process event, push departure
                {
                    cpuBusy = true;
                    eventQ.front().set_type(DEPARTURE);
                    eventQ.front().set_arrival(simClock + eventQ.front().get_serviceTime());
                }
                else
                {
                    readyQ.push_back(eventQ.front());
                    eventQ.erase(eventQ.begin());
                }

                break;
            case DEPARTURE:
                simClock = eventQ.front().get_arrival();
                float priorityHRRN;
                
                for(unsigned int i = 0; i < readyQ.size(); i++)
                {
                    readyQ[i].set_wait(simClock - readyQ[i].get_arrival());
                    priorityHRRN = (readyQ[i].get_totalWait() + readyQ[i].get_serviceTime()) / readyQ[i].get_serviceTime();
                    readyQ[i].set_priority(priorityHRRN);
                }
               
                sort(readyQ.begin(), readyQ.end(), sorter2);
               
               if (!readyQ.empty())
               {
                readyQ.front().been_seen(simClock - readyQ.front().get_arrival());
                sumWait += readyQ.front().get_totalWait();
                sumServiceTime += readyQ.front().get_serviceTime();
                eventQ.erase(eventQ.begin());
               }

                if(readyQ.empty())
                    cpuBusy = false;
                else
                {
                    readyQ.front().set_type(DEPARTURE);
                    readyQ.front().set_arrival(simClock + readyQ.front().get_serviceTime());
                    eventQ.push_back(readyQ.front());
                    readyQ.erase(readyQ.begin());
                }
                pCount++;

                break;

            default:
                cout << "Please check your input." << endl;
                break;
        }
    }
}

void simRR() // round robin
{
	vector<process> readyQ;
    int pCount = 0;
    unsigned int eqSize = eventQ.size();
    while (pCount < endSimulation)
    {
    	sort(eventQ.begin(), eventQ.end(), sorter3);

    	switch (eventQ.front().get_type())
        {
        	case ARRIVAL:

            break;
        	case DEPARTURE:
             
            break;
        	default:
        		cout << "Please check your input." << endl;
            break;
        }

    }

}

int main(int argc, char *argv[] )
{
    // parse arguments
    scheduler = atoi(argv[1]);
    lambda = atoi(argv[2]);
    avgServiceTime = (float)atof(argv[3]);
    quantum = (float)atof(argv[4]);

    init();
    run_sim(scheduler); 
    generate_report();
    return 0;
}
