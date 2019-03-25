/****************************************************
*   course:       CS4328 
*   project:      Project 1 - Scheduler Simulator 
*   programmer:   Stacy Bridges
*   date:         11/04/2015  
*   description:  This program provides discrete time
*                 event simulations for 4 schedulers:
*                  1. First Come First Serve
*                  2. Shortest Remaining Time First
*                  3. Highest Response Ratio Next
*                  4. Round Robin
****************************************************/

/////////////////////////////////////////////////////
// include library content and program fils
#include "header.h"
#include <cstdlib>            // EXIT_SUCCESS
#include <iostream>
using namespace std;

/////////////////////////////////////////////////////
// begin main program
int main(int argc, char *argv[]){
   parseArgs(argv);          // parse args from console
   init();                   // initialize the simulation
   run_sim();                // run the simulation
   generate_report();        // output sim stats to file

   return EXIT_SUCCESS;      // exit program
}

