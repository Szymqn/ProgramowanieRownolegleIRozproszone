import threading
import time
import random


class Railway:
    Railway = 1
    Departure = 2
    During = 3
    Arrival = 4
    Disaster = 5

    def __init__(self, num_of_trucks, num_of_trains):
        self.num_of_trucks = num_of_trucks
        self.num_of_trains = num_of_trains
        self.num_of_occupied = 0
        self.lock = threading.Lock()

    def start(self, number):
        with self.lock:
            self.num_of_occupied -= 1
            print(f"Permission for the departure of the train no. {number}")
            return self.Departure

    def arrival(self):
        time.sleep(1)
        with self.lock:
            if self.num_of_occupied < self.num_of_trucks:
                self.num_of_occupied += 1
                print(f"Permission for the arrival of the truck no. {self.num_of_occupied}")
                return self.Railway
            else:
                return self.Arrival

    def reduce(self):
        with self.lock:
            self.num_of_trains -= 1
            print("Crash")
            if self.num_of_trains == self.num_of_trucks:
                print("The number of trains is the same as the number of tracks")


class Train(threading.Thread):
    Railway = 1
    Departure = 2
    During = 3
    Arrival = 4
    Disaster = 5
    Service = 1000
    Repair = 500

    def __init__(self, number, mileage_limit, railway):
        super().__init__()
        self.number = number
        self.mileage_limit = mileage_limit
        self.state = self.During
        self.railway = railway

    def run(self):
        while True:
            if self.state == self.Railway:
                if random.randint(0, 1) == 1:
                    self.state = self.Departure
                    self.mileage_limit = self.Service
                    print(f"Request for permission to depart")
                    self.state = self.railway.start(self.number)
                else:
                    print("Wait for permission...")
            elif self.state == self.Departure:
                print(f"Departure of train no. {self.number}")
                self.state = self.During
            elif self.state == self.During:
                self.mileage_limit -= random.randint(0, 500)
                if self.mileage_limit <= self.Repair:
                    self.state = self.Arrival
                else:
                    time.sleep(random.randint(0, 1))
            elif self.state == self.Arrival:
                print(f"Request for permission for arrival no. {self.number}, mileage limit {self.mileage_limit}")
                self.state = self.railway.arrival()
                if self.state == self.Arrival:
                    self.mileage_limit -= random.randint(0, 500)
                    print(f"Reserve {self.mileage_limit}")
                    if self.mileage_limit <= 0:
                        self.state = self.Disaster
            elif self.state == self.Disaster:
                print(f"Train no. {self.number} disaster")
                self.railway.reduce()


class RailwaySimulator:
    num_of_trains = 100
    num_of_tracks = 5

    def __init__(self):
        self.railway = Railway(self.num_of_tracks, self.num_of_trains)

    def run_simulation(self):
        for i in range(self.num_of_trains):
            Train(i, 2000, self.railway).start()


if __name__ == "__main__":
    simulator = RailwaySimulator()
    simulator.run_simulation()
