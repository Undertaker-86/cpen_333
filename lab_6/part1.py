# student name: Gyan Edbert Zesiro
# student number: 38600060

import multiprocessing
import random  # is used to cause some randomness
import time  # is used to cause some delay to simulate thinking or eating times


# We will be implementing the 4 philosophers solution, so atleast one chopstick will always be free
# This means that we won't have a circular wait condition, which means no deadlock
def philosopher(id: int, chopstick: list, tableSemaphore: multiprocessing.Semaphore):
    """
    implements a thinking-eating philosopher
    id is used to identifier philosopher #id (id is between 0 to numberOfPhilosophers-1)
    chopstick is the list of semaphores associated with the chopsticks
    tableSemaphore: semaphore limiting how many philosophers can sit at the table
    """

    def eatForAWhile():  # simulates philosopher eating time with a random delay
        print(f"DEBUG: philosopher{id} eating")
        time.sleep(round(random.uniform(0.1, 0.3), 2))  # a random delay (100 to 300 ms)

    def thinkForAWhile():  # simulates philosopher thinking time with a random delay
        print(f"DEBUG: philosopher{id} thinking")
        time.sleep(round(random.uniform(0.1, 0.3), 2))  # a random delay (100 to 300 ms)

    for _ in range(6):  # to make testing easier, instead of a forever loop we use a finite loop
        leftChopstick = id
        rightChopstick = (id + 1) % 5  # 5 is number of philosophers

        # At most 4 philosophers can be seated
        tableSemaphore.acquire()

        chopstick[leftChopstick].acquire()
        print(f"DEBUG: philosopher{id} has chopstick{leftChopstick}")
        chopstick[rightChopstick].acquire()
        print(f"DEBUG: philosopher{id} has chopstick{rightChopstick}")

        eatForAWhile()  # use this line as is

        print(f"DEBUG: philosopher{id} is to release chopstick{rightChopstick}")
        chopstick[rightChopstick].release()
        print(f"DEBUG: philosopher{id} is to release chopstick{leftChopstick}")
        chopstick[leftChopstick].release()

        # Release the table seat after putting down both chopsticks
        tableSemaphore.release()

        thinkForAWhile()  # use this line as is


if __name__ == "__main__":
    semaphoreList = list()  # this list will hold one semaphore per chopstick
    numberOfPhilosophers = 5

    for i in range(numberOfPhilosophers):
        semaphoreList.append(
            multiprocessing.Semaphore(1)
        )  # one semaphore per chopstick

    # Initialize semaphore to 4
    tableSemaphore = multiprocessing.Semaphore(numberOfPhilosophers - 1)

    philosopherProcessList = list()
    for i in range(numberOfPhilosophers):  # instantiate all processes representing philosophers
        philosopherProcessList.append(
            multiprocessing.Process(target=philosopher, args=(i, semaphoreList, tableSemaphore))
        )
    for j in range(numberOfPhilosophers):  # start all child processes
        philosopherProcessList[j].start()
    for k in range(numberOfPhilosophers):  # join all child processes
        philosopherProcessList[k].join()
