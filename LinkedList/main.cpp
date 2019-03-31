/* Project 1
 In this project, we are going to build a discrete-time event
 simulator for a number of CPU schedulers on a single CPU system.
 The goal of this project is to compare and assess the impact of
 different schedulers on different performance metrics, and across multiple workloads.
 @authors: Jamal Rasool, Kristof York
 @date: March 21st, 2019
*/
#include "header.h"
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int argc, char *argv[]) {
   parseArgs(argv);          // parse arguments from console
   init();                   // initialize the simulation
   run_sim();                // run the simulation
   generate_report();        // output sim stats to file

   return EXIT_SUCCESS;
}
