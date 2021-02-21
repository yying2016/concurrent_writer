# concurrent_writer
A library to process data with multiple processes and save the processed data into the same destination without locking the resources.
Python package 'multiprocessing' makes use of multiple cores of cpu for cpu-bound jobs. 
There are 2 ways to save the results of jobs into the same destination if it doesn't have an existing mechanism to handle concurrent writing (e.g. files, sqlite, ...).
The first approach is synchronous programming, which uses lock to ensure that only one process write to that destination at one time.
The second approach is to save the results to a data structure (e.g. queue) shared by the processes and create another only process to read the results from the shared data structure and write them to the destination.

## usages
ConcurrentWriter is an abstract class which uses a queue as the shared data structure between processes and implements the second approach to realize concurrent writing.
To use it, you can create a subclass inherited from ConcurrentWriter, and overide the method execute() and generate_tasks()
### execute()
This is a method to define how to write a single result into a destination.
### generate_tasks()
This is a method to define how to generate the writing tasks and put them into a queue.

### example
TestConcurrentWriter is a class inherited from ConcurrentWriter. It saves the results produced by multiple procesesses into a single table 'student' in a sqlite database. 
To run it, use command python TestConcurretnWriter.py.
