import numpy as np
from task import Processor, Task
import matplotlib.pyplot as plt

class LIFO():
     
    def __init__(self, interval = 10,  number_tasks = 5000):
        
        self.number_tasks = number_tasks  # кількість задач що генерується
        self.count = 0               # лічильник задач
        self.queue = []
        self.empty_tasks = []              # черга 
        self.solved = []             # вирішені задачі
        self.interval = interval

    def generate_tasks(self):
        randomNumbers = np.random.normal(loc=self.interval, scale=2, size=self.number_tasks)
        randomInt = np.round(randomNumbers).astype(int)
        self.t_current = 0
        for time in randomInt:
            if time <= 0:
                self.t_current += self.interval
            else:
                self.t_current += time
            task = Task(time_arrive=self.t_current, t_solve=10)
            self.empty_tasks.append(task)

    def check_modeling(self):
        for task in self.solved:
            print('Time arrive: ', task.t_in)
            print('Start process: ', task.t_start_process)
            print('Processing time', task.t_solve)
            print('Time of exit from system', task.t_out)
            print('Time in queue', task.t_inQueue)
            print('-'*20)

    def start(self):
        self.generate_tasks() 
        processor  = Processor() 
        self.t_current = 0

        while len(self.solved) < self.number_tasks:
            if not processor.is_free():
                if processor.task.t_solve == processor.task.time_processed:
                    task = processor.task
                    task.t_out = self.t_current
                    self.solved.append(task)
                    processor.task = None

            if processor.is_free():
                if len(self.queue) > 0:
                    processor.task = self.queue.pop(len(self.queue) - 1)
                    if processor.task.time_processed == 0:
                        processor.task.t_start_process = self.t_current
                else:
                    processor.task = None

            if len(self.empty_tasks) > 0 and self.empty_tasks[0].t_in == self.t_current:
                task = self.empty_tasks.pop(0)
                if processor.is_free():
                    processor.task = task
                    processor.task.t_start_process = self.t_current
                else:
                    self.queue.append(task)

            self.t_current += 1
            if not processor.is_free():
                processor.task.time_processed += 1

        for task in self.solved:
            task.t_inQueue = task.t_out - task.t_solve - task.t_in


    def get_average_time_in_queue(self):
        if not self.solved:
            print('In the first instance generate tasks and execute modeling')
            return None
        else:
            return sum([task.t_inQueue for task in self.solved]) / self.number_tasks

    def get_inaction_time_percent(self):
        if not self.solved:
            print('In the first instance generate tasks and execute modeling')
            return None
        else:
            return (self.solved[-1].t_out - self.number_tasks*self.solved[0].t_solve) / \
                   self.solved[-1].t_out

def check_LIFO():
    time = list(range(4, 25))
    average_time_in_queue = []
    average_inactive_percent = []

    for i in time:
        smo = LIFO(interval=i, number_tasks=1000)
        smo.start()
        average_time_in_queue.append(smo.get_average_time_in_queue())
        average_inactive_percent.append(smo.get_inaction_time_percent())


    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)

    ax1.plot(time, average_time_in_queue)
    ax1.set_title('LIFO\n Середній час очікування')
    ax2.plot(time, average_inactive_percent)
    ax2.set_title('Відсоток простою')
    plt.show()


    for time in [2, 9, 10, 11]:
        smo = LIFO(interval=time, number_tasks=1000)
        smo.start()
        array = [task.t_inQueue for task in smo.solved]
        plt.hist(array, bins=25)
        plt.title("Залежність кількісті заявок від часу очікування, time = {}".format(time))
        plt.xlabel("Час очікування")
        plt.ylabel("Кількість заявок")
        plt.show()
check_LIFO()