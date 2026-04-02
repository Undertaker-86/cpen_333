# Group #:
# Student names:

import threading
import queue
import time, random

PRODUCER_COUNT = 4
CONSUMER_COUNT = 5
ITEMS_PER_PRODUCER = 6
PRODUCER_DELAY_RANGE = (0.05, 0.18)
CONSUMER_DELAY_RANGE = (0.08, 0.22)
STOP_TOKEN = "__STOP__"


def consumerWorker(queue):
    """target worker for a consumer thread"""
    workerName = threading.current_thread().name
    print(f"{workerName} started.")
    while True:
        item = queue.get()
        if item == STOP_TOKEN:
            print(f"{workerName} received the stop signal.")
            queue.task_done()
            break

        time.sleep(random.uniform(*CONSUMER_DELAY_RANGE))
        print(f"{workerName} consumed {item}.")
        queue.task_done()

    print(f"{workerName} stopped.")


def producerWorker(queue):
    """target worker for a producer thread"""
    workerName = threading.current_thread().name
    print(f"{workerName} started.")
    for itemNumber in range(1, ITEMS_PER_PRODUCER + 1):
        time.sleep(random.uniform(*PRODUCER_DELAY_RANGE))
        item = f"{workerName}-item-{itemNumber:02d}"
        queue.put(item)
        print(f"{workerName} produced {item}.")
    print(f"{workerName} finished producing.")


if __name__ == "__main__":
    buffer = queue.Queue()

    consumers = [
        threading.Thread(
            target=consumerWorker,
            args=(buffer,),
            name=f"Consumer-{index}"
        )
        for index in range(1, CONSUMER_COUNT + 1)
    ]
    producers = [
        threading.Thread(
            target=producerWorker,
            args=(buffer,),
            name=f"Producer-{index}"
        )
        for index in range(1, PRODUCER_COUNT + 1)
    ]

    for consumer in consumers:
        consumer.start()
    for producer in producers:
        producer.start()

    for producer in producers:
        producer.join()

    print("All producers finished. Sending one stop token to each consumer.")
    for _ in range(CONSUMER_COUNT):
        buffer.put(STOP_TOKEN)

    buffer.join()

    for consumer in consumers:
        consumer.join()

    print(
        f"Run complete: {PRODUCER_COUNT * ITEMS_PER_PRODUCER} items were produced "
        f"and consumed through one FIFO queue."
    )
