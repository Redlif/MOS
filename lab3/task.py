class Task():

    def __init__(self, time_arrive, t_solve):
        self.t_in = time_arrive                               # час входу до системи
        self.t_start_process = 0   
        self.t_solve = t_solve
        self.t_inQueue = 0                          # час в черзі (записується пізніше)
        self.t_out = 0   
        self.time_processed = 0                           # час виходу з системи

    def calc_time_in_queue(self):
        if self.t_out:
            self.t_inQueue = self.t_out - self.t_in - self.t_solve

class Processor:
    def __init__(self, task=None):
        self.task = task

    def is_free(self):
        return not self.task