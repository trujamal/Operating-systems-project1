# the compiler needs to be g++ for this C++ program
CC = g++
CFLAGS  = -g -Wall

default: proj1

# identify source files needed to create the object files
main.o:  main.cpp header.h
	$(CC) $(CFLAGS) -c main.cpp

implementation.o:  implementation.cpp header.h 
	$(CC) $(CFLAGS) -c implementation.cpp

# identify object files needed to create the executable
proj1:  main.o implementation.o 
	$(CC) $(CFLAGS) -o proj1 main.o implementation.o

# To start over from scratch, type 'make clean', which will  
# remove old files of type .exe, .o, ~
clean: 
	$(RM) proj1 *.o *~
