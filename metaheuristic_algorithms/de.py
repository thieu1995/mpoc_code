import numpy as np
from copy import deepcopy

from includes.utils import *
from blockchain_network.simulation import Simulator

class DeEngine:
    ID_SOl = 0
    ID_FIT = 1
    def __init__(self, population_size, epochs, num_simulation_each_solution, n_value):
        self.epoch =  epochs
        self.population_size = population_size
        self.num_simulation_each_solution = num_simulation_each_solution
        self.n_value = n_value
        self.element_length = 10
        self.domain_range = [0, 1]
        self.weighting_factor = 0.8
        self.crossover_rate = 0.9

    def compute_fitness(self, solution):
        '''
        Simulate blockchain network by parameters
        '''
        # scenario = [num_round, num_peer_on_network, num_leader_each_round, num_candidate_leader, num_peer_in_round_1]
        # scenario = [[100, 200, 21, 20, 50]]
        # scenario = [[100, 200, 21, 20, 75], [100, 300, 21, 20, 75]]
        # scenario = [[100, 200, 21, 20, 100], [100, 300, 21, 20, 100]]
        # scenario = [[100, 200, 21, 20, 50], [100, 200, 21, 20, 75], [100, 200, 21, 20, 100]]
        # scenario = [[100, 200, 21, 20, 75]]
        # scenario = [[1, 10, 2, 2, 4]]
        # if self.n_value == 75:
        #     scenario = [[100, 200, 21, 20, 75]]
        # elif self.n_value == 100:
        #     scenario = [[100, 200, 21, 20, 100]]
        # elif self.n_value == 125:
        #     scenario = [[100, 200, 21, 20, 125]]
        # elif self.n_value == 'all':
        scenario = [[100, 200, 21, 20, 75], [100, 200, 21, 20, 100], [100, 200, 21, 20, 125]]
        # scenario = [[5, 50, 11, 10, 20]]

        fitness = 0
        for _scenario in scenario:
            for i in range(self.num_simulation_each_solution):
                simulator = Simulator(solution, _scenario[0], _scenario[1], _scenario[2], _scenario[3], _scenario[4])
                simulation_result = simulator.simulate_mdpos()
                fitness += simulation_result
        fitness /= (self.num_simulation_each_solution * len(scenario))
        return fitness

    def _mutation__(self, p0, p1, p2, p3):
        # Choose a cut point which differs 0 and chromosome-1 (first and last element)
        cut_point = np.random.randint(1, self.element_length - 1)
        sample = []
        for i in range(self.element_length):
            if i == cut_point or np.random.uniform() < self.crossover_rate:
                v = p1[i] + self.weighting_factor * ( p2[i] - p3[i])
                v = self.domain_range[0] if v < self.domain_range[0] else v
                v = self.domain_range[1] if v > self.domain_range[1] else v
                sample.append(v)
            else :
                sample.append(p0[i])
        return sample

    def _create_children__(self, pop):
        new_children = []
        for i in range(self.population_size):
            temp = np.random.choice(range(0, self.population_size), 3, replace=False)
            print(i)
            while i in temp:
                temp = np.random.choice(range(0, self.population_size), 3, replace=False)
            #create new child and append in children array
            child = self._mutation__(pop[i][self.ID_SOl], pop[temp[0]][self.ID_SOl], pop[temp[1]][self.ID_SOl], pop[temp[2]][self.ID_SOl])
            print(child)
            fit = self.compute_fitness(child)
            new_children.append([child, fit])
        return new_children

    ### Survivor Selection
    def _greedy_selection__(self, pop_old=None, pop_new=None):
        pop = [pop_new[i] if pop_new[i][self.ID_FIT] < pop_old[i][self.ID_FIT]
               else pop_old[i] for i in range(self.population_size)]
        return pop

    def create_solution(self):
        '''
        Initiate population
        About solution:
            - Page rank
            - Voting score 
            - Điểm vote mà các nút không tham gia epochs đó bầu chọn cho nút đó.
            - Coin age
            - Lượng token đã stake
            - Số epoch mà nút đó tham gia vào hệ thống blockchain
            - Số lần mà nút đó đã đóng block
            - Số lần mà nút đó được đưa vào round
            - Số lần mà nút đó không được đưa vào round nhưng bầu chọn đúng nút
        '''
        _solution = random_parameter_combination(self.element_length)
        _fitness = self.compute_fitness(_solution)
        # print(_solution, _fitness)
        return [_solution, _fitness]

    def _get_global_best__(self, pop=None, id_fitness=None, id_best=None):
        sorted_pop = sorted(pop, key=lambda temp: temp[id_fitness])
        return deepcopy(sorted_pop[id_best])

    def evolve(self):
        pop = [self.create_solution() for _ in range(self.population_size)]
        gbest = self._get_global_best__(pop=pop, id_fitness=self.ID_FIT, id_best=0)
        self.loss_train = []
        for i in range(self.epoch):
            # create children
            children = self._create_children__(pop)
            print('line 113')
            # create new pop by comparing fitness of corresponding each member in pop and children
            pop = self._greedy_selection__(pop, children)
            print('line 116')
            current_best = self._get_global_best__(pop=pop, id_fitness=self.ID_FIT, id_best=0)
            print('line 118')
            if current_best[self.ID_FIT] < gbest[self.ID_FIT]:
                gbest = deepcopy(current_best)
            
            print('Epoch : {}, Fitness: {}'.format(i + 1, gbest[self.ID_FIT]))
            self.loss_train.append(gbest[self.ID_FIT])
        return gbest[self.ID_SOl], self.loss_train





