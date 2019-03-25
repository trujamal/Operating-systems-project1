// class to hold relevant process information
#ifndef PROCESS_CPP
#define PROCESS_CPP

class process {
    private:
        float arrivalTime;
        float serviceTime;
        float prempTime;
        float serviceTimeLeft;
        bool seen;
        float initialWait;
        float totalWait;
        float priority;
        int pid;
        int processType;      // arrival, departure, quantum
    public:
        process(float burst, float time, int id, int type);
        void set_arrival(float time);
        void set_pid(int num);
        float get_arrival();
        float get_serviceTime();
        float get_priority();
        void set_priority(float newPriority);
        float get_serviceTimeLeft();
        void dec_burst();
        float get_initialWait();
        float get_totalWait();
        void set_prempTime(float time);
        void add_wait(float time);
        bool get_seen();
        void been_seen(float time);
        int get_pid();
        int get_type();
        void set_type(int type);
        void set_wait(float time);
};

process::process(float burst, float time, int id, int type)
{
    pid = id;
    serviceTime = burst;
    serviceTimeLeft = burst;
    arrivalTime = time;
    seen = false;
    priority = 1.0;
    initialWait = 0.0;
    totalWait = 0.0;
    processType = type;
}

void process::set_pid(int num)
{
    pid = num;
}

bool process::get_seen()
{
    return seen;
}

float process::get_priority()
{
    return priority;
}

void process::set_priority(float newPriority)
{
    priority = newPriority;
}

float process::get_serviceTime()
{
    return serviceTime;
}

int process::get_pid()
{
    return pid;
}

int process::get_type()
{
    return processType;
}

void process::set_type(int type)
{
    processType = type;
}

void process::set_arrival(float time)
{
    arrivalTime = time;
}

float process::get_arrival()
{
    return arrivalTime;
}

float process::get_serviceTimeLeft()
{
    return serviceTimeLeft;
}

void process::dec_burst()
{
    serviceTimeLeft = serviceTimeLeft - 1;
}

float process::get_initialWait()
{
    return initialWait;
}

float process::get_totalWait()
{
    return totalWait;
}

void process::set_prempTime(float time)
{
    prempTime = time;
}

void process::add_wait(float time)
{
    totalWait = totalWait + time;
}

void process::set_wait(float time)
{
    totalWait = time;
}
void process::been_seen(float time)
{
    seen = true;
    initialWait = time;
    totalWait = time;
}

bool sorter(process a, process b)
{
    return a.get_serviceTimeLeft() < b.get_serviceTimeLeft();
}

bool sorter2(process a, process b)
{
    return a.get_priority() > b.get_priority();
}

bool sorter3(process a, process b)
{
    return a.get_arrival() < b.get_arrival();
}

#endif // PROCESS_CPP
