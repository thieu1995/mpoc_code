#!/usr/bin/env python
# ------------------------------------------------------------------------------------------------------%
# Created by "Thieu" at 09:39, 18/11/2020                                                               %
#                                                                                                       %
#       Email:      nguyenthieu2102@gmail.com                                                           %
#       Homepage:   https://www.researchgate.net/profile/Nguyen_Thieu2                                  %
#       Github:     https://github.com/thieu1995                                                        %
# ------------------------------------------------------------------------------------------------------%

from queue import Queue
from multiprocessing import Pool
from sklearn.model_selection import ParameterGrid
from time import sleep

metaheuristic_method = "ga"
population_size = [30, 50, 100]
epochs = [200]
num_simulation_each_solution = [1, 2]
n_value = ['all']


def _tunning_with_ga(item):
    print('>>> start experiment with pool <<<')

    population_size = item["population_size"]
    epochs = item["epochs"]
    num_simulation_each_solution = item["num_simulation_each_solution"]
    n_value = item['n_value']
    t = 0
    for i in range(0, 100):
        t += 1
        sleep(0.1)
        print("{}, {}, {}, {}, {}".format(t, population_size, epochs, num_simulation_each_solution, n_value))
    return True



if metaheuristic_method == 'ga':
    param_grid = {
        'population_size': population_size,
        'epochs': epochs,
        'num_simulation_each_solution': num_simulation_each_solution,
        'n_value': n_value
    }
    queue = Queue()
    for item in list(ParameterGrid(param_grid)):
        queue.put_nowait(item)
    pool = Pool(1)
    pool.map(_tunning_with_ga, list(queue.queue))
    pool.close()
    pool.join()
    pool.terminate()