#!/usr/bin/env python3

## @package DEVS-FIFO
#
#  Discrete event simulator using the FIFO scheduler
#  =================================================
#
#  @brief Implementation of a discrete event simulator for the FIFO scheduling strategy
#         Input to the simulator is the system description, which consists of:
#             -# Number of tasks to schedule
#             -# Task periods 
#             -# Arrival times
#             -# Execution times
#             -# Deadlines
#
#         Depending on the scheduling strategy, the simulator generates a trace 
#         for the tasks being executed
#
#         Refer to readme.txt for a description of the input file formats
#
#  @date   4/12/2017
#  @author srijeshs

## Simpy for simulating a time base
import simpy as sp

## Reading the arrivals.txt from file into artime
with open('./arrivals.txt') as f:
    content = f.read().splitlines()
    artime=[]
    for i in range(0,len(content)):
        artime.append(content[i].split(' '))


## Reading the setup.txt from file into servtime
with open('./setup.txt') as f:
    content = f.read().splitlines()
    servtime=[]
    for i in range(0,len(content)):
        servtime.append(content[i].split(' '))

## Removing carriage returns, and white spaces to guard against variablility in inputs
for i in range(0,len(artime)):
    for j in range(0,len(artime[i])):
       if artime[i][j] in ['', ' ' , '\n']:
          del artime[i][j]

i=0

## Sorting event queue according to arrival time and task id
for i in range(2,len(artime)):
    if int(artime[i-1][0])>int(artime[i][0]):
        artime[i-1],artime[i]=artime[i],artime[i-1]

    elif int(artime[i-1][0])==int(artime[i][0]):
        if int(artime[i-1][1])>int(artime[i][1]):
            artime[i-1],artime[i]=artime[i],artime[i-1]


## Removing carriage returns, and white spaces
for i in range(0,len(servtime)):
    for j in range(0,len(servtime[i])):
       if servtime[i][j] in ['', ' ' , '\n']:
          del servtime[i][j]

## Initialization of list variables
timelist=[]                         ### Time stamps of event occurences
tasklist=[]                         ### List of task IDs scheduled at the time stamps
taskcount=[0]*(len(servtime))       ### Task count accumulator for instances of each task's scheduling  list
instancecount=[]                    ### Task counter snapshots for each scheduled instance of each task at each time stamp

## Array index placeholders for readability
ARRTIME_IDX  = 0
TASKID_IDX   = 1
EXECTIME_IDX = 2
PERIOD_IDX   = 3

## Placeholders for the taskID of IDLE state and the index in the task counter for an IDLE "task"
IDLE_TASKID  = -1
IDLE_TASKCNT_LISTIDX = 3

## Event queue simulation function
def event_sim(env):
    iArrival=1

    timelist.append(env.now)                                                        ### Append the initial timestamp
    tasklist.append(int(artime[iArrival][TASKID_IDX]))                              ### Append the first arriving task's ID
    taskcount[int(artime[iArrival][TASKID_IDX])]+=1                                 ### Increment the task count for the first task
    instancecount.append(taskcount[int(artime[iArrival][TASKID_IDX])])              ### Record the count at this timestamp instance

    ## BEGIN FOR LOOP OVER EACH ARRIVAL FROM THE ARRIVALS.TXT INPUT FILE
    for iArrival in range(2,len(artime)-1): 
        
        ### timeGap stores the time between the current task's execution time and the next task's arrival 
        timeGap= (env.now+int(artime[iArrival][2]))-int(artime[iArrival+1][ARRTIME_IDX]) 

        ### If the current task ends later than the next one arrives
        if timeGap>0:
            yield env.timeout(abs(int(artime[iArrival+1][ARRTIME_IDX])-env.now))    ### Increment time to the arrival of next task
            yield env.timeout(abs(timeGap))                                         ### FIFO: Continue to increment time to the end of current task
            timelist.append(env.now)                                                ### Assuming current task has ended, record the timestamp
            tasklist.append(int(artime[iArrival+1][TASKID_IDX]))                    ### Record task ID of the waiting next task
            taskcount[int(artime[iArrival+1][TASKID_IDX])]+=1                       ### Increment the task count for that task by 1
            instancecount.append(taskcount[int(artime[iArrival+1][TASKID_IDX])])    ### Save the task's instance count at this timestamp

        ### Else if the current task ends before than the next one arrives
        elif timeGap<0:
            yield env.timeout(int(artime[iArrival][EXECTIME_IDX]))                  ### Increment time by the execution time of the current task
            timelist.append(env.now)                                                ### Assuming current task has ended, record the timestamp 
            tasklist.append(IDLE_TASKID)                                            ### FIFO: Since no task has arrived yet, record a -1 in the result
            taskcount[IDLE_TASKCNT_LISTIDX]+=1                                      ### Increment the IDLE state (3)'s task count by 1
            instancecount.append(taskcount[IDLE_TASKCNT_LISTIDX])                   ### Save the IDLE task's instance count at this timestamp

            yield env.timeout(abs(timeGap))                                         ### Jump to the arrival of the next task post IDLE
            timelist.append(env.now)                                                ### Record the timestamp
            tasklist.append(int(artime[iArrival+1][TASKID_IDX]))                    ### Schedule the next task and record its task ID
            taskcount[int(artime[iArrival+1][TASKID_IDX])]+=1                       ### Increment the task count for that task by 1    
            instancecount.append(taskcount[int(artime[iArrival+1][TASKID_IDX])])    ### Save the task's instance count at this timestamp

    ## END OF FOR LOOP OVER EACH ARRIVAL FROM INPUT

    yield env.timeout(int(artime[len(artime)-1][EXECTIME_IDX]))                     ### Finally, increment time by the last task's execution time
    timelist.append(env.now)                                                        ### Record the final timestamp
    tasklist.append(IDLE_TASKID)                                                    ### Record an IDLE task due to the completion of all scheduled tasks
    taskcount[IDLE_TASKCNT_LISTIDX]+=1                                              ### Increment the IDLE state (3)'s task count by 1
    instancecount.append(taskcount[IDLE_TASKCNT_LISTIDX])                           ### Save the IDLE task's instance count at this timestamp

    ## Formatting of results in the specified format
    for i in range(0,len(instancecount)):
        instancecount[i]= '.'+str(instancecount[i])
        tasklist[i]=str(tasklist[i])+instancecount[i]
    
    ## iArrivalip up the outputs and print results to stdout
    zipped=zip(timelist,tasklist)
    printresult=list(zipped)
    for m in range(0,len(printresult)):
        print(printresult[m][0],printresult[m][1])
        
## END OF EVENT_SIM FUNCTION

## DEFINITION OF ENVIRONMENT SIMULATION VARIABLES FROM SIMPY. CALLS event_sim(env)
env = sp.Environment()                ### INIT A ENVIRONMENT CONTEXT VARIABLE
env.process(event_sim(env))           ### BEGIN THE PROCESS BY CALLING event_sim
env.run(until=(10000000))             ### UPPER BOUND FOR SIMULATION RUN


'''
Required Output format
<time> <task-id>.<task-instance>
0 1.1
20 2.1
30 -1.1
60 2.2
70 -1.2
110 2.3
121 -1.3
150 2.4
160 -1.4
180 1.2
200 2.5
210 -1.5
'''
