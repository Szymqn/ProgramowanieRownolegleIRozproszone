from multiprocessing import current_process
import time


def worker(output):
    name = current_process().name
    print(f"{name} Starting")  # Add print statements here
    output.append(f"{name} Starting")
    time.sleep(2)
    print(f"{name} Exiting")  # Add print statements here
    output.append(f"{name} Exiting")


def service(output):
    name = current_process().name
    print(f"{name} Starting")  # Add print statements here
    output.append(f"{name} Starting")
    time.sleep(3)
    print(f"{name} Exiting")  # Add print statements here
    output.append(f"{name} Exiting")
