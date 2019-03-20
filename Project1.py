# Program Strucutre in python.
def schedule_event(type, time, other_val):
	# creates a new event and places it in the event queue based on its time.



# Three parts in the init

def Init_Process():
	clock=0;
	# Generate a list of processes (Arrival times, Service Time)
	End_condition = 0;
	# Ready Queue (No proceses within it)
	CPU_idle = True;
	# Init Event Queue w/ arrivals.


def get_event():

def process_arrival(event):
	if(CPU_idle == 1) #Checking to see if its true
		CPU_idle == 0;
		schedule_event(dep, event_time + service_time);
	else
		#Place P in Ready queue

def process_departure(event):
	if(readqueue == 0) # Check to see if ready queue is empty
		CPU_idle = 1;
	else
		remove_process(from_readqueue)
		schedule_event(dep, event_time + s);


while (!End_condition):
	event = get_event();
	clock = event -> time;

	switch(event->type) 
		case ARR:
			# Arrival case call function
			process_arrival(event);
		case DEP:
			# Arrival case call function
			process_depature(event);


