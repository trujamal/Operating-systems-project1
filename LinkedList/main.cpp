#include "header.h"
#include <cstdlib>
#include <iostream>
using namespace std;

int main(int argc, char *argv[]) {
   parseArgs(argv);          // parse args from console
   init();                   // initialize the simulation
   run_sim();                // run the simulation
   generate_report();        // output sim stats to file

   return EXIT_SUCCESS;
}
