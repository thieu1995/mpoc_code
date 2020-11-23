import os
import time
import random
import queue
import multiprocessing
from multiprocessing import Pool
from queue import Queue
from sklearn.model_selection import ParameterGrid


def benchmark(item):
    # print(item)
    os.system(item['command'])


if __name__ == "__main__":
    # command=['pwd', 'pwd', 'pwd']
    # print(command)
    path_wrk = '/home/bkc_3/Desktop/wrk/wrk'
    destination_ip = '127.0.0.1'
    
    start_time = time.time()
    print(start_time)
    command_round = []
    for i in range(10):
        _command_round = []
        for j in range(70):
            destimation_port = 8000 + j
            time_benchwrk = random.choice(range(20))
            _command = ' -t12 -c400 -d{}s -s /home/bkc_3/Desktop/wrk/scripts/post_lua/post_{}.lua  http://{}:{}'\
                .format(time_benchwrk, j, destination_ip, destimation_port)
            _command_round.append(_command)
        command_round.append(_command_round)

    for i in range(10):
        param_grid = {
            'command': command_round[i]
        }
        print(param_grid)
        queue = Queue()
        for item in list(ParameterGrid(param_grid)):
            queue.put_nowait(item)
        pool = Pool(10)
        pool.map(benchmark, list(queue.queue))
        pool.close()
        pool.join()
        pool.terminate()
        print("Done")