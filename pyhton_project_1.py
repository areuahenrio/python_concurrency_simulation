import threading
import time
import random

class Sensor:
    def __init__(self, read_id):
        self.read_id = read_id
        self.process_time = random.randint(1, 6)

class Aggregator:
    def __init__(self, agg_id, max_readings):
        self.agg_id = agg_id
        self.max_reading = max_readings
        self.count = 0
        self.lock = threading.Lock()
        self.active = 0

    def handle_read(self, reading):
        with self.lock:
            if self.active >= self.max_reading:
                return False
            self.active += 1

        print(f"Aggregator {self.agg_id} assigned Reading {reading.read_id}")
        time.sleep(reading.process_time)
        with self.lock:
            self.active -= 1
            self.count += 1
            print(f"Aggregator {self.agg_id} completed Reading {reading.read_id}")
        return True

def worker(aggregator, que, que_lock):
    while True:
        with que_lock:
            if len(que) == 0:
                return
            reading = que.pop(0)
        work_done = aggregator.handle_read(reading)
        if work_done:
            print(f"Reading {reading.read_id} assigned to Aggregator {aggregator.agg_id}")
        else:
            print(f"Maximum capacity reached for reading {reading.read_id}")
            with que_lock:
                que.append(reading)
            time.sleep(0.5)

def main():
    num_sensors = 50
    num_aggregators = 5
    max_readings = 3

    readings = [Sensor(i) for i in range(1, num_sensors + 1)]
    que = list(readings)
    que_lock = threading.Lock()

    aggregators = [Aggregator(i, max_readings) for i in range(1, num_aggregators + 1)]

    threads = []
    for agg in aggregators:
        t = threading.Thread(target=worker, args=(agg, que, que_lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("Readings:", end=" ")
    for reading in readings:
        print(reading.read_id, end=" ")
    print()

    print("Aggregators:", end=" ")
    for aggregator in aggregators:
        print(aggregator.agg_id, end=" ")
    print()

    print("All readings processed.")

if __name__ == "__main__":
    main()
