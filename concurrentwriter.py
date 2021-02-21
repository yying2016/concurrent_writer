from multiprocessing import Queue, Process
from time import sleep


class ConcurrentWriter:
    def __init__(self, num_processors, retry_times=10, retry_interval=1):
        assert num_processors > 1, "Number of processors must be larger than 1."
        self._num_processors = num_processors
        self._retry_times = retry_times
        self._retry_interval = retry_interval
        self._tasks = Queue()
        self._init_workers()

    def _init_workers(self):
        self._producers = []
        for i in range(self._num_processors - 1):
            self._producers.append(Process(target=self.produce_tasks, args=(self._tasks, )))

        self._writer = Process(
            target=self.execute_tasks,
            args=(self._tasks, self._retry_times, self._retry_interval, self.execute)
        )

    @staticmethod
    def execute(**kwargs):
        raise NotImplementedError("Not implemented!")

    @staticmethod
    def execute_tasks(tasks, retry_times, retry_interval, execute_func):
        total_tasks = 0
        retried_times = 0

        while True:
            if not tasks.empty():
                retried_times = 0
                task_args = tasks.get()
                execute_func(**task_args)
                total_tasks += 1
                print('A writing task is done!')
            else:
                if retried_times < retry_times:
                    retried_times += 1
                    sleep(retry_interval)
                else:
                    print('No new tasks are created. Finished executing all the tasks.')
                    break

    @staticmethod
    def produce_tasks(tasks):
        raise NotImplementedError("Not implemented")

    def start(self):
        for producer in self._producers:
            producer.start()
        self._writer.start()

        for producer in self._producers:
            producer.join()
        self._writer.join()