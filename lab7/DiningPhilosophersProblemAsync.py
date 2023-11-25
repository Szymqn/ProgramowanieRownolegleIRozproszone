import asyncio
import random


class Philosopher:
    def __init__(self, index, left_fork, right_fork):
        self.index = index
        self.left_fork = left_fork
        self.right_fork = right_fork

    async def run(self):
        for _ in range(5):
            await self.think()
            await self.eat()

    async def think(self):
        print(f"Philosopher {self.index} is thinking.")
        await asyncio.sleep(random.uniform(1, 3))

    async def eat(self):
        print(f"Philosopher {self.index} is hungry and trying to pick up forks.")
        async with self.left_fork, self.right_fork:
            print(f"Philosopher {self.index} is eating.")
            await asyncio.sleep(random.uniform(1, 3))
        print(f"Philosopher {self.index} finished eating.")


async def main():
    num_philosophers = 5
    forks = [asyncio.Lock() for _ in range(num_philosophers)]
    philosophers = []

    for i in range(num_philosophers):
        left_fork = forks[i]
        right_fork = forks[(i + 1) % num_philosophers]
        philosopher = Philosopher(i, left_fork, right_fork)
        philosophers.append(philosopher)

    tasks = [philosopher.run() for philosopher in philosophers]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "event loop is already running" in str(e):
            loop = asyncio.get_event_loop()
            loop.run_until_complete(main())
        else:
            raise e
