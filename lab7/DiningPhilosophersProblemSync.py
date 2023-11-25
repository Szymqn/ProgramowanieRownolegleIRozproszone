import threading
import time
import random


class PhilosopherParallel(threading.Thread):
    def __init__(self, index, left_fork, right_fork):
        super().__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        for _ in range(5):
            self.think()
            self.eat()

    def think(self):
        print(f"Philosopher {self.index} is thinking.")
        time.sleep(random.uniform(1, 3))

    def eat(self):
        print(f"Philosopher {self.index} is hungry and trying to pick up forks.")
        with self.left_fork, self.right_fork:
            print(f"Philosopher {self.index} is eating.")
            time.sleep(random.uniform(1, 3))
        print(f"Philosopher {self.index} finished eating.")


num_philosophers = 5
forks = [threading.Lock() for _ in range(num_philosophers)]
philosophers = []

for i in range(num_philosophers):
    left_fork = forks[i]
    right_fork = forks[(i + 1) % num_philosophers]
    philosopher = PhilosopherParallel(i, left_fork, right_fork)
    philosophers.append(philosopher)

for philosopher in philosophers:
    philosopher.start()

for philosopher in philosophers:
    philosopher.join()
