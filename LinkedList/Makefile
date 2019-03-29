# the compiler needs to be g++ for this C++ program
CC = g++
CFLAGS  = -g

default: project1

# identify source files needed to create the object files
main.o:  main.cpp header.h
	$(CC) $(CFLAGS) -c main.cpp

Schedulers.o:  Schedulers.cpp header.h
	$(CC) $(CFLAGS) -c Schedulers.cpp

# identify object files needed to create the executable
project1:  main.o Schedulers.o
	$(CC) $(CFLAGS) -o project1 main.o Schedulers.o

# To start over from scratch, type 'make clean', which will
# remove old files of type .exe, .o, ~
clean:
	$(RM) project1 *.o *~
