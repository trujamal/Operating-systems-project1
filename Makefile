# generic c++ makefile

TARGET	=	sim#				  executable
SRCS		=	sim.cpp#			  source files
OBJS	 	= 	$(SRCS:.cpp=.0)# object files

.PHONY:
	all:	$(TARGET)

$(TARGET): 	$(SRCS)
	g++ -o $(TARGET) $(SRCS)

fcfs:
	./sim 1 1 0.06

clean:
	@rm $(TARGET) 


