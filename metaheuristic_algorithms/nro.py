import numpy as np
from math import gamma
import scipy.stats as ss
from copy import deepcopy

from includes.utils import *
from blockchain_network.simulation import Simulator


class NroEngine:
    ID_POS = 0
    ID_FIT = 1

    def __init__(self, population_size=None, epochs=None, num_simulation_each_solution=None, n_value=None):
        self.population_size = population_size
        self.epochs = epochs
        self.num_simulation_each_solution = num_simulation_each_solution
        self.n_value = n_value
        self.element_length = 10
        self.domain_range = [0, 1]
    
    def _amend_solution_and_return__(self, solution=None):
        for i in range(self.element_length):
            if solution[i] < self.domain_range[0] or solution[i] > self.domain_range[1]:
                solution[i] = np.random.uniform(self.domain_range[0], self.domain_range[1])
        return solution

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
        if self.n_value == 75:
            scenario = [[100, 200, 21, 20, 75]]
        elif self.n_value == 100:
            scenario = [[100, 200, 21, 20, 100]]
        elif self.n_value == 125:
            scenario = [[100, 200, 21, 20, 125]]
        elif self.n_value == 'all':
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
    
    def _get_global_worst__(self, pop=None, id_fitness=None, id_worst=None):
        sorted_pop = sorted(pop, key=lambda temp: temp[id_fitness])
        return deepcopy(sorted_pop[id_worst])
    
    def _check_array_equal__(self, array1, array2):
        check = True
        for i in range(len(array1)):
            if array1[i] != array2[i]:
                check = False
                break
        return check

    def evolve(self):
        pop = [self.create_solution() for _ in range(self.population_size)]
        g_best = max(pop, key=lambda x: x[1])
        self.loss_train = []
        for epoch in range(self.epochs):
            xichma_v = 1
            xichma_u = ((gamma(1 + 1.5) * np.sin(np.pi * 1.5 / 2)) / (gamma((1 + 1.5) / 2) * 1.5 * 2 ** ((1.5 - 1) / 2))) ** (1.0 / 1.5)
            levy_b = (np.random.normal(0, xichma_u ** 2)) / (np.sqrt(np.random.normal(0, xichma_v ** 2)) ** (1.0 / 1.5))

            # NFi phase
            Pb = np.random.uniform()
            Pfi = np.random.uniform()
            freq = 0.05
            alpha = 0.01
            for i in range(self.population_size):

                ## Calculate neutron vector Nei by Eq. (2)
                ## Random 1 more index to select neutron
                temp1 = list( set(range(0, self.population_size)) - set([i]))
                i1 = np.random.choice(temp1, replace=False)
                Nei = (pop[i][self.ID_FIT] + pop[i1][self.ID_FIT]) / 2
                Xi = None
                ## Update population of fission products according to Eq.(3), (6) or (9);
                if np.random.uniform() <= Pfi:
                    ### Update based on Eq. 3
                    if np.random.uniform() <= Pb:
                        xichma1 = (np.log(epoch + 1) * 1.0 / (epoch+1)) * np.abs( np.subtract(pop[i][self.ID_POS], g_best[self.ID_POS]))
                        gauss = np.array([np.random.normal(g_best[self.ID_POS][j], xichma1[j]) for j in range(self.element_length)])
                        Xi = gauss + np.random.uniform() * g_best[self.ID_FIT] - round(np.random.rand() + 1)*Nei
                    ### Update based on Eq. 6
                    else:
                        i2 = np.random.choice(temp1, replace=False)
                        xichma2 = (np.log(epoch + 1) * 1.0 / (epoch+1)) * np.abs( np.subtract(pop[i2][self.ID_POS], g_best[self.ID_POS]))
                        gauss = np.array([np.random.normal(pop[i][self.ID_POS][j], xichma2[j]) for j in range(self.element_length)])
                        Xi = gauss + np.random.uniform() * g_best[self.ID_FIT] - round(np.random.rand() + 2) * Nei
                ## Update based on Eq. 9
                else:
                    i3 = np.random.choice(temp1, replace=False)
                    xichma2 = (np.log(epoch + 1) * 1.0 / (epoch+1)) * np.abs( np.subtract(pop[i3][self.ID_POS], g_best[self.ID_POS]))
                    Xi = np.array([np.random.normal(pop[i][self.ID_POS][j], xichma2[j]) for j in range(self.element_length)])

                ## Check the boundary and evaluate the fitness function
                Xi = self._amend_solution_and_return__(Xi)
                fit = self.compute_fitness(Xi)
                if fit < pop[i][self.ID_FIT]:
                    pop[i] = [Xi, fit]
                if fit < g_best[self.ID_FIT]:
                    g_best = [Xi, fit]

            # NFu phase

            ## Ionization stage
            ## Calculate the Pa through Eq. (10);
            ranked_pop = ss.rankdata([pop[i][self.ID_FIT] for i in range(self.population_size)])
            for i in range(self.population_size):
                X_ion = deepcopy(pop[i][self.ID_POS])
                if (ranked_pop[i] * 1.0 / self.population_size) < np.random.uniform():
                    temp1 = list(set(range(0, self.population_size)) - set([i]))
                    i1, i2 = np.random.choice(temp1, 2, replace=False)

                    for j in range(self.element_length):
                        #### Levy flight strategy is described as Eq. 18
                        if pop[i2][self.ID_POS][j] == pop[i][self.ID_POS][j]:
                            X_ion[j] = pop[i][self.ID_POS][j] + alpha * levy_b * ( pop[i][self.ID_POS][j] - g_best[self.ID_POS][j])
                        #### If not, based on Eq. 11, 12
                        else:
                            if np.random.uniform() <= 0.5:
                                X_ion[j] = pop[i1][self.ID_POS][j] + np.random.uniform() * (pop[i2][self.ID_POS][j] - pop[i][self.ID_POS][j])
                            else:
                                X_ion[j] = pop[i1][self.ID_POS][j] - np.random.uniform() * (pop[i2][self.ID_POS][j] - pop[i][self.ID_POS][j])

                else:   #### Levy flight strategy is described as Eq. 21
                    X_worst = self._get_global_worst__(pop, self.ID_FIT, -1)
                    for j in range(self.element_length):
                        ##### Based on Eq. 21
                        if X_worst[self.ID_POS][j] == g_best[self.ID_POS][j]:
                            X_ion[j] = pop[i][self.ID_POS][j] + alpha * levy_b * (self.domain_range[1] - self.domain_range[0])
                        ##### Based on Eq. 13
                        else:
                            X_ion[j] = pop[i][self.ID_POS][j] + round(np.random.uniform()) * np.random.uniform()*( X_worst[self.ID_POS][j] - g_best[self.ID_POS][j] )

                ## Check the boundary and evaluate the fitness function for X_ion
                X_ion = self._amend_solution_and_return__(X_ion)
                fit = self.compute_fitness(X_ion)
                if fit < pop[i][self.ID_FIT]:
                    pop[i] = [X_ion, fit]
                if fit < g_best[self.ID_FIT]:
                    g_best = [X_ion, fit]
            ## Fusion Stage

            ### all ions obtained from ionization are ranked based on (14) - Calculate the Pc through Eq. (14)
            ranked_pop = ss.rankdata([pop[i][self.ID_FIT] for i in range(self.population_size)])
            for i in range(self.population_size):

                X_fu = deepcopy(pop[i][self.ID_POS])
                temp1 = list(set(range(0, self.population_size)) - set([i]))
                i1, i2 = np.random.choice(temp1, 2, replace=False)

                #### Generate fusion nucleus
                if (ranked_pop[i] * 1.0 / self.population_size) < np.random.uniform():
                    t1 = np.random.uniform() * (np.array(pop[i1][self.ID_POS]) - np.array(g_best[self.ID_POS]))
                    t2 = np.random.uniform() * (np.array(pop[i2][self.ID_POS]) - np.array(g_best[self.ID_POS]))
                    temp2 = np.array(pop[i1][self.ID_POS]) - np.array(pop[i2][self.ID_POS])
                    X_fu = pop[i][self.ID_POS] + t1 + t2 - np.exp(-np.linalg.norm(temp2)) * temp2
                #### Else
                else:
                    ##### Based on Eq. 22
                    if self._check_array_equal__(pop[i1][self.ID_POS], pop[i2][self.ID_POS]):
                        X_fu = pop[i][self.ID_POS] + alpha * levy_b * (pop[i][self.ID_POS] - g_best[self.ID_POS])
                    ##### Based on Eq. 16, 17
                    else:
                        if np.random.uniform() > 0.5:
                            X_fu = pop[i][self.ID_POS] - 0.5*(np.sin(2*np.pi*freq*epoch + np.pi)*(self.epochs - epoch)/self.epochs + 1)*(np.array(pop[i1][self.ID_POS]) - np.array(pop[i2][self.ID_POS]))
                        else:
                            X_fu = pop[i][self.ID_POS] - 0.5 * (np.sin(2 * np.pi * freq * epoch + np.pi) * epoch / self.epochs + 1) * (np.array(pop[i1][self.ID_POS]) - np.array(pop[i2][self.ID_POS]))

                X_fu = self._amend_solution_and_return__(X_fu)
                fit = self.compute_fitness(X_fu)
                if fit < pop[i][self.ID_FIT]:
                    pop[i] = [X_fu, fit]
                if fit < g_best[self.ID_FIT]:
                    g_best = [X_fu, fit]

            self.loss_train.append(g_best[self.ID_FIT])
            print("Generation : {0}, best result so far: {1}".format(epoch + 1, g_best[self.ID_FIT]))
        return g_best[self.ID_POS], self.loss_train
