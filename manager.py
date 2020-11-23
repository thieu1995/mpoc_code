import sys
import os
import multiprocessing
from multiprocessing import Pool
from queue import Queue
from sklearn.model_selection import ParameterGrid, train_test_split
import pandas as pd

from config import *
from metaheuristic_algorithms.genertic_algorithm import GenerticAlgorithmEngine
from metaheuristic_algorithms.particle_swarm_optimization import PSOEngine, Particle
from metaheuristic_algorithms.whale_optimization_algorithm import WoaEngine
from metaheuristic_algorithms.hsgo import HsgoEngine
from metaheuristic_algorithms.nro import NroEngine
from metaheuristic_algorithms.de import DeEngine
from metaheuristic_algorithms.qso import QsoEngine
from blockchain_network.simulation import Simulator
from graphs.visualization import *
from includes.utils import *
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42
plt.rcParams["font.family"] = "Arial"


def simulate_consensus_algorithms():
    if Config.CONSENSUS_METHOD == 'pos':
        print('|-> Simulate proof of stake consensus')
    elif Config.CONSENSUS_METHOD == 'dpos':
        print('|-> Simulate delegated proof of stake consensus')
        weights = [0.01721829, 0.27249606, 0.01478004, 0.05778563, 0.10831706, 0.06232477, 0.03541199, 0.16121772, -1]
        num_round = 500
        num_peer_on_network = 200
        num_leader_each_round = 21
        num_candidate_leader = 30
        num_peer_in_round_1 = 100
        simulator = Simulator(
            weights, num_round, num_peer_on_network, num_leader_each_round, num_candidate_leader, num_peer_in_round_1)
        
        simulator.simulate_dpos(num_candidate_leader)
    elif Config.CONSENSUS_METHOD == 'mdpos':
        print('|-> Simulate metaheuristic proof of stake consensus')
        weights_nro = [0.06617751, 0.59980905, 0.18280644, 0.23816735, 0.83763677, 0.45882368, 0.07787386, 0.92278235,
                       0.03458709, 0.02682467]

        num_round = 500
        num_peer_on_network = 500
        num_leader_each_round = 21
        num_candidate_leader = 30
        num_peer_in_round_1 = 75
        with open(f'final_results_{num_peer_on_network}_{num_peer_in_round_1}.txt', 'a+') as f:
            for i in range(10):
                simulator = Simulator(weights_nro, num_round, num_peer_on_network, num_leader_each_round, 
                                      num_candidate_leader, num_peer_in_round_1)
                fitness, peers_number_leader_time, leader_time  = simulator.simulate_mdpos()
                f.write('{}\n{}\n\n'.format(peers_number_leader_time, len(leader_time)))
    else:
        print('|-> We do not support this consensus method')


def _tunning_with_ga(item):
    print('>>> start experiment with pool <<<')

    population_size = item["population_size"]
    epochs = item["epochs"]
    num_simulation_each_solution = item["num_simulation_each_solution"]
    n_value = item['n_value']
    results_save_path = Config.CORE_DATA_DIR + '/{}/{}/{}_{}/'\
        .format('final_results', 'zero_to_one', 'genertic_algorithm', n_value)
    genertic_algorithm_ng = GenerticAlgorithmEngine(population_size, epochs, num_simulation_each_solution, n_value)
    best_solution, fitness_arr = genertic_algorithm_ng.evolve()
    file_name = 'training_fitness_{}_{}_{}'\
        .format(genertic_algorithm_ng.population_size, genertic_algorithm_ng.num_simulation_each_solution, 
                genertic_algorithm_ng.epochs)

    # save prediction
    fitness_arr_file = results_save_path + file_name + '.csv'
    fitness_arr_df = pd.DataFrame(np.array(fitness_arr))
    fitness_arr_df.to_csv(fitness_arr_file, index=False, header=None)
    with open(results_save_path + 'solution.txt', 'a+') as f:
        f.write('{}, {}, {} \n'.format(file_name, best_solution, fitness_arr[-1]))
    f.close()


def _tunning_with_pso(item):
    population_size = item["population_size"]
    epochs = item["epochs"]
    num_simulation_each_solution = item["num_simulation_each_solution"]
    n_value = item['n_value']
    results_save_path = Config.CORE_DATA_DIR + '/{}/{}/{}_{}/'\
        .format('final_results', 'zero_to_one', 'pso', n_value)
    pso_ng = PSOEngine(population_size, epochs, num_simulation_each_solution)
    pso_ng.particles = [Particle(n_value) for _ in range(pso_ng.population_size)]
    gbest_particle_position, fitness_arr = pso_ng.evolve()
    file_name = 'training_fitness_{}_{}_{}'\
        .format(pso_ng.population_size, pso_ng.num_simulation_each_solution, pso_ng.epochs)

    # save prediction
    fitness_arr_file = results_save_path + file_name + '.csv'
    fitness_arr_df = pd.DataFrame(np.array(fitness_arr))
    fitness_arr_df.to_csv(fitness_arr_file, index=False, header=None)
    with open(results_save_path + 'solution.txt', 'a+') as f:
        f.write('{}, {}, {} \n'.format(file_name, gbest_particle_position, fitness_arr[-1]))
    f.close()


def _tunning_with_woa(item):
    population_size = item["population_size"]
    epochs = item["epochs"]
    num_simulation_each_solution = item["num_simulation_each_solution"]
    n_value = item['n_value']
    results_save_path = Config.CORE_DATA_DIR + '/{}/{}/{}_{}/'\
        .format('final_results', 'zero_to_one', 'woa', n_value)
    woa_ng = WoaEngine(population_size, epochs, num_simulation_each_solution)
    woa_ng.particles = [Particle(n_value) for _ in range(woa_ng.population_size)]
    gbest_particle_position, fitness_arr = woa_ng.evolve()

    file_name = 'training_fitness_{}_{}_{}'\
        .format(woa_ng.population_size, woa_ng.num_simulation_each_solution, woa_ng.epochs)

    # save prediction
    fitness_arr_file = results_save_path + file_name + '.csv'
    fitness_arr_df = pd.DataFrame(np.array(fitness_arr))
    fitness_arr_df.to_csv(fitness_arr_file, index=False, header=None)
    with open(results_save_path + 'solution.txt', 'a+') as f:
        f.write('{}, {}, {} \n'.format(file_name, gbest_particle_position, fitness_arr[-1]))
    f.close()


def _tunning_with_hgso(item):
    population_size = item['population_size']
    epochs = item['epochs']
    num_simulation_each_solution = item['num_simulation_each_solution']
    n_clusters = item['n_clusters']
    n_value = item['n_value']
    results_save_path = Config.CORE_DATA_DIR + '/{}/{}/{}_{}/'\
        .format('final_results', 'zero_to_one', 'hsgo', n_value)
    hgso_ng = HsgoEngine(population_size, n_clusters, epochs, num_simulation_each_solution, n_value)
    gbest_particle_position, fitness_arr = hgso_ng.evolve()
    
    file_name = 'training_fitness_{}_{}_{}_{}'\
        .format(hgso_ng.population_size, hgso_ng.n_clusters, hgso_ng.num_simulation_each_solution, hgso_ng.epochs)

    # save prediction
    fitness_arr_file = results_save_path + file_name + '.csv'
    fitness_arr_df = pd.DataFrame(np.array(fitness_arr))
    fitness_arr_df.to_csv(fitness_arr_file, index=False, header=None)
    with open(results_save_path + 'solution.txt', 'a+') as f:
        f.write('{}, {}, {} \n'.format(file_name, gbest_particle_position, fitness_arr[-1]))
    f.close()

def _tunning_with_nro(item):
    population_size = item['population_size']
    epochs = item['epochs']
    num_simulation_each_solution = item['num_simulation_each_solution']
    n_value = item['n_value']
    results_save_path = Config.CORE_DATA_DIR + '/{}/{}/{}_{}/'\
        .format('final_results', 'zero_to_one', 'nro', n_value)

    if not os.path.exists(results_save_path):
        os.mkdir(results_save_path)

    nro_ng = NroEngine(population_size, epochs, num_simulation_each_solution, n_value)
    gbest_particle_position, fitness_arr = nro_ng.evolve()
    
    file_name = 'training_fitness_{}_{}_{}'\
        .format(nro_ng.population_size, nro_ng.num_simulation_each_solution, nro_ng.epochs)

    # save prediction
    fitness_arr_file = results_save_path + file_name + '.csv'
    fitness_arr_df = pd.DataFrame(np.array(fitness_arr))
    fitness_arr_df.to_csv(fitness_arr_file, index=False, header=None)
    with open(results_save_path + 'solution.txt', 'a+') as f:
        f.write('{}, {}, {} \n'.format(file_name, gbest_particle_position, fitness_arr[-1]))
    f.close()

def _tunning_with_de(item):
    population_size = item['population_size']
    epochs = item['epochs']
    num_simulation_each_solution = item['num_simulation_each_solution']
    n_value = item['n_value']
    results_save_path = Config.CORE_DATA_DIR + '/{}/{}/{}_{}/'\
        .format('final_results', 'zero_to_one', 'de', n_value)

    if not os.path.exists(results_save_path):
        os.mkdir(results_save_path)

    de_ng = DeEngine(population_size, epochs, num_simulation_each_solution, n_value)
    gbest_particle_position, fitness_arr = de_ng.evolve()
    
    file_name = 'training_fitness_{}_{}_{}'\
        .format(de_ng.population_size, de_ng.num_simulation_each_solution, de_ng.epoch)

    # save prediction
    fitness_arr_file = results_save_path + file_name + '.csv'
    fitness_arr_df = pd.DataFrame(np.array(fitness_arr))
    fitness_arr_df.to_csv(fitness_arr_file, index=False, header=None)
    with open(results_save_path + 'solution.txt', 'a+') as f:
        f.write('{}, {}, {} \n'.format(file_name, gbest_particle_position, fitness_arr[-1]))
    f.close()

def _tunning_with_qso(item):
    population_size = item['population_size']
    epochs = item['epochs']
    num_simulation_each_solution = item['num_simulation_each_solution']
    n_value = item['n_value']
    results_save_path = Config.CORE_DATA_DIR + '/{}/{}/{}_{}/'\
        .format('final_results', 'zero_to_one', 'qso', n_value)

    if not os.path.exists(results_save_path):
        os.mkdir(results_save_path)

    qso_ng = QsoEngine(population_size, epochs, num_simulation_each_solution, n_value)
    gbest_particle_position, fitness_arr = qso_ng.evolve()
    
    file_name = 'training_fitness_{}_{}_{}'\
        .format(qso_ng.population_size, qso_ng.num_simulation_each_solution, qso_ng.epoch)

    # save prediction
    fitness_arr_file = results_save_path + file_name + '.csv'
    fitness_arr_df = pd.DataFrame(np.array(fitness_arr))
    fitness_arr_df.to_csv(fitness_arr_file, index=False, header=None)
    with open(results_save_path + 'solution.txt', 'a+') as f:
        f.write('{}, {}, {} \n'.format(file_name, gbest_particle_position, fitness_arr[-1]))
    f.close()

def tunning_mdpos(metaheuristic_method):
    weights = random_parameter_combination(10)
    population_size = [30, 50]
    epochs = [200]
    num_simulation_each_solution = [1, 2]
    n_value = ['all']

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
    elif metaheuristic_method == 'pso':
        param_grid = {
            'population_size': population_size,
            'epochs': epochs,
            'num_simulation_each_solution': num_simulation_each_solution,
            'n_value': n_value
        }
        queue = Queue()
        for item in list(ParameterGrid(param_grid)):
            queue.put_nowait(item)
        pool = Pool(8)
        pool.map(_tunning_with_pso, list(queue.queue))
        pool.close()
        pool.join()
        pool.terminate()

    elif metaheuristic_method == 'woa':
        print('|-> Start tuning metaheuristic consensus by woa')
        param_grid = {
            'population_size': population_size,
            'epochs': epochs,
            'num_simulation_each_solution': num_simulation_each_solution,
            'n_value': n_value
        }
        queue = Queue()
        for item in list(ParameterGrid(param_grid)):
            queue.put_nowait(item)
        pool = Pool(8)
        pool.map(_tunning_with_woa, list(queue.queue))
        pool.close()
        pool.join()
        pool.terminate()
    elif metaheuristic_method == 'hsgo':
        print('|-> Start tuning metaheuristic consensus by hsgo')
        n_clusters = [5]
        param_grid = {
            'population_size': population_size,
            'epochs': epochs,
            'num_simulation_each_solution': num_simulation_each_solution,
            'n_clusters': n_clusters,
            'n_value': n_value
        }
        queue = Queue()
        for item in list(ParameterGrid(param_grid)):
            queue.put_nowait(item)
        pool = Pool(8)
        pool.map(_tunning_with_hgso, list(queue.queue))
        pool.close()
        pool.join()
        pool.terminate()
    elif metaheuristic_method == 'nro':
        print('|-> Start tuning metaheuristic consensus by nro')
        param_grid = {
            'population_size': population_size,
            'epochs': epochs,
            'num_simulation_each_solution': num_simulation_each_solution,
            'n_value': n_value
        }
        queue = Queue()
        for item in list(ParameterGrid(param_grid)):
            queue.put_nowait(item)
        pool = Pool(8)
        pool.map(_tunning_with_nro, list(queue.queue))
        pool.close()
        pool.join()
        pool.terminate()
    elif metaheuristic_method == 'qso':
        print('|-> Start tuning metaheuristic consensus by qso')
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
        pool.map(_tunning_with_qso, list(queue.queue))
        pool.close()
        pool.join()
        pool.terminate()
    elif metaheuristic_method == 'de':
        print('|-> Start tuning metaheuristic consensus by de')
        param_grid = {
            'population_size': population_size,
            'epochs': epochs,
            'num_simulation_each_solution': num_simulation_each_solution,
            'n_value': n_value
        }
        queue = Queue()
        for item in list(ParameterGrid(param_grid)):
            queue.put_nowait(item)
        pool = Pool(8)
        pool.map(_tunning_with_de, list(queue.queue))
        pool.close()
        pool.join()
        pool.terminate()
    else:
        print('|-> We do not support this method')


def benchmark(item):
    os.system(item['command'])


if __name__ == "__main__":
    try:
        if sys.argv[1] == 'simulate_consensus_alg':
            simulate_consensus_algorithms()
        elif sys.argv[1] == 'tunning_mdpos':
            tunning_mdpos(sys.argv[2])
        else:
            print('[ERROR] Please check your parameter')
    except IndexError:
        print('[ERROR] Miss system parameter for this script')
