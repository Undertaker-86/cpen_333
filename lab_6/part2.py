#student name: Gyan Edbert Zesiro
#student number: 38600060

import multiprocessing
import random #is used to cause some randomness 
import time   #is used to cause some delay to simulate thinking or eating times

# For part 2, we will use the method to execute only when both chopstick is available
# Summary of approach:
# Acqure left chopstick, then attempt to acquire right chopstick without blocking
# If the right chopstick isn't available, release the left and retries again
def philosopher(id: int, chopstick: list, mutex: multiprocessing.Lock): 
    """
       implements a thinking-eating philosopher
       id is used to identifier philosopher #id (id is between 0 to numberOfPhilosophers-1)
       chopstick is the list of semaphores associated with the chopsticks 
       mutex: a lock ensuring atomic operation for chopstick
    """
    def eatForAWhile():   #simulates philosopher eating time with a random delay
        print(f"DEBUG: philosopher{id} eating")
        time.sleep(round(random.uniform(.1, .3), 2)) #a random delay (100 to 300 ms)
    
    def thinkForAWhile(): #simulates philosopher thinking time with a random delay
        print(f"DEBUG: philosopher{id} thinking")
        time.sleep(round(random.uniform(.1, .3), 2)) #a random delay (100 to 300 ms)

    for _ in range(6): #to make testing easier, instead of a forever loop we use a finite loop
        leftChopstick = id
        rightChopstick = (id + 1) % 5      #5 is number of philosophers

        while True:
            mutex.acquire()
        #to simplify, try statement not used here
            chopstick[leftChopstick].acquire()
            print(f"DEBUG: philosopher{id} has chopstick{leftChopstick}")
            # The key line, acquire right chopstick without blocking
            if chopstick[rightChopstick].acqure(block=False):
                # Both chopstick acquired succesfully
                print(f"DEBUG: philosopher{id} has chopstick{rightChopstick}")
                mutex.release()
                break # Exit loop to eat
            else:
                # Right chopstick not available, release our lock to try again later
                print(f"DEBUG: philosopher{id} release chopstick{leftChopstick}")
                chopstick[leftChopstick].release()
                mutex.release()
                # Delay before retrying
                time.sleep(round(random.uniform(.01, .05), 3))

        eatForAWhile()  #use this line as is

        print(f"DEBUG: philosopher{id} is to release chopstick{rightChopstick}")
        chopstick[rightChopstick].release()
        print(f"DEBUG: philosopher{id} is to release chopstick{leftChopstick}")
        chopstick[leftChopstick].release()

        thinkForAWhile()  #use this line as is

if __name__ == "__main__":
    semaphoreList = list()          #this list will hold one semaphore per chopstick
    numberOfPhilosophers = 5

    for i in range(numberOfPhilosophers):             
        semaphoreList.append(multiprocessing.Semaphore(1))    #one semaphore per chopstick
    
    # Mutex initilization
    mutex = multiprocessing.Lock()
    philosopherProcessList = list()
    for i in range(numberOfPhilosophers): #instantiate all processes representing philosophers
        philosopherProcessList.append(multiprocessing.Process(target=philosopher, args=(i, semaphoreList, mutex)))
    for j in range(numberOfPhilosophers): #start all child processes
        philosopherProcessList[j].start()
    for k in range(numberOfPhilosophers): #join all child processes
        philosopherProcessList[k].join()
