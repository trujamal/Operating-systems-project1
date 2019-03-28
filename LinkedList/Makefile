CC = g++
CFLAGS  = -g

default: project_one_simmulator


main.o:  main.cpp header.h
	$(CC) $(CFLAGS) -c main.cpp

implementation.o:  Schedulers.cpp header.h 
	$(CC) $(CFLAGS) -c Schedulers.cpp


project_one_simmulator:  main.o Schedulers.o 
	$(CC) $(CFLAGS) -o project_one_simmulator main.o Schedulers.o



clean: 
	$(RM) project_one_simmulator *.o *~
