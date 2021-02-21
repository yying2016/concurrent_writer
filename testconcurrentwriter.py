import sqlite3
from time import sleep
import uuid
import random
from concurrentwriter import ConcurrentWriter


class TestConcurrentWriter(ConcurrentWriter):
    def __init__(self, num_processers, retry_times=10, retry_interval=1):
        super().__init__(num_processers, retry_times, retry_interval)

    @staticmethod
    def execute(stuid, name, age):
        conn = sqlite3.connect('example.db', isolation_level=None)
        c = conn.cursor()
        sql = f"INSERT INTO student (stuid, name, age) VALUES ({stuid}, '{name}', {age})"
        c.execute(sql)
        conn.commit()
        conn.close()

    @staticmethod
    def produce_tasks(tasks):
        student_names = ["Alice", "Jimmy", "Nick", "Anna"]
        for i in range(10):
            sleep(0.1)
            task = {
                "stuid": uuid.uuid4().int,
                "name": random.choice(student_names),
                "age": random.randint(10, 20)
            }

            tasks.put(task)
            print("put")

        print(f"{i + 1} task(s) created!")


if __name__ == "__main__":
    tester = TestConcurrentWriter(5)
    tester.start()