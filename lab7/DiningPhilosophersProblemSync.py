import threading
import time
import random


class PhilosopherParallel(threading.Thread):
    def __init__(self, index, left_fork, right_fork):
        super().__init__()
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork
        self.holding_left_fork = False
        self.holding_right_fork = False

    def run(self):
        for _ in range(5):
            self.think()
            self.eat()

    def think(self):
        print(f"Philosopher {self.index} is thinking.")
        time.sleep(random.uniform(1, 3))

    def eat(self):
        print(f"Philosopher {self.index} is hungry and trying to pick up forks.")

        while True:
            fork1, fork2 = self.left_fork, self.right_fork

            with fork1:
                if not self.holding_left_fork:
                    self.holding_left_fork = True

                    with fork2:
                        if not self.holding_right_fork:
                            self.holding_right_fork = True
                            break
                        else:
                            self.holding_left_fork = False

            time.sleep(random.uniform(0, 1))

        print(f"Philosopher {self.index} is eating.")
        time.sleep(random.uniform(1, 3))

        self.holding_left_fork = False
        self.holding_right_fork = False
        print(f"Philosopher {self.index} finished eating.")


if __name__ == "__main__":
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
