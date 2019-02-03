# DEVS
Discrete Event Scheduling Simulation

## FORMAT OF FILES:
 
Every Individual test should include two files "setup.txt" and
"arrivals.txt" where the inputs for your simulation are defined. 

### I - setup.txt:

The file setup.txt consists of three parts:
 - Part 1: One line (i.e., the first line in the file) which is a positive
		integer that sets the number of tasks "n_tasks" that the RTOS should schedule.

 - Part 2: "n_tasks" lines that define the tasks that the system should schedule.
		Every line has the format:

		<task_id>  <frequency>

		Where:
		<task_id> is a positive non-zero integer  
		<frequency> is the periodicity of the task with <task_id>  

 - Part 3: One line that contains a positive integer defining the context
		switching overhead. This overhead can equal zero. This overhead should be
		simulated when the execution of a given task is interrupted by a higher
		priority task

For example, "setup" of a system with 2 tasks and scheduler overhead of 1 unit will look like:    

2  
1 100  
2 50   
1  


### II - arrivals.txt

The input file arrivals.txt consists of 2 parts 

 - Part 1: One line (i.e., the first line in the file) which is a positive
		integer that sets the number of events "n_events" your simulator will trace.

 - Part 2: "n_events" lines that define the events the simulator will trace.
		Every line has the format: 

		<time> <task_id> <execution_time> <deadline>

	    Where:    
		<time> is a positive integer representing the time unit when the event occurs   
		<task_id> is a positive integer that is less than or equal <n_tasks> defining the task_id for the event    
		<execution_time> is non-zero positive integer representing the time required to execute the task that associates this event  
		<deadline> is non-zero positive integer representing the time by which this event should complete execution  

For example, using the setupt.txt example shown above, arrivals.txt can look like:  
3  
0 1 20 100  
1 2 10 50  
60 2 10 100  

### III- correct-output.txt   

correct-output.txt contains the simulation trace for the system defined in setup.txt and arrivals.txt.  
As the simulator is implemented as a discrete events system, we are only interested in the moment when the task being executed changes.  

Therefore, correct-output.txt will consist of multiple lines where every line indicates a change in the task being executed by the system.   

Every line in correct-output.txt has the format:

	<time> <task-id>.<task-instance>

	Note: There should be a SINGLE space " " between these three fields.

	Where:
	<time> is the time when the simulator switches tasks. 

	<task-id> is the id of task that will start execution.

	<task-instance> is a non zero positive integer representing each subsequent instance for the task "task-id". The value of "task-instance" should start by 1, and be incremented by 1 for every task.  

Two special values of "task-id" are reserved for the context switching overhead and the idle execution. These values are: "0" for the context switching overhead and "-1" for idle execution.

For example, given the above values for setup.txt and arrivals.txt, using a RMS or EDF schedules, the correct-output.txt should be:  
0 1.1  
1 0.1  
2 2.1  
12 1.1  
31 -1.1  
60 2.2  
70 -1.2  
