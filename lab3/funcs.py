from multiprocessing import current_process
import time


def worker(output):
    name = current_process().name
    output.put(f"{name} Starting")
    time.sleep(2)
    output.put(f"{name} Exiting")


def service(output):
    name = current_process().name
    output.put(f"{name} Starting")
    time.sleep(3)
    output.put(f"{name} Exiting")
