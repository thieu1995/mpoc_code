import time
import random
import matplotlib.pyplot as plt

from blockchain_network.simulation import Simulator
from includes.utils import *


class GenerticAlgorithmEngine:
    cross_over_rate = 0.9
    mutation_rate = 0.05
    sigma = 0.01

    def __init__(self, population_size=10, epochs=2, num_simulation_each_solution=1, n_value=None):
        self.population_size = population_size
        self.epochs = epochs
        self.num_simulation_each_solution = num_simulation_each_solution
        self.element_length = 10
        self.n_value = n_value
    
    def compute_fitness(self, solution):
        '''
        Simulate blockchain network by parameters
        '''
        # scenario = [num_round, num_peer_on_network, num_leader_each_round, num_candidate_leader, num_peer_in_round_1]

        if self.n_value == 75:
            scenario = [[100, 200, 21, 20, 75]]
        elif self.n_value == 100:
            scenario = [[100, 200, 21, 20, 100]]
        elif self.n_value == 125:
            scenario = [[100, 200, 21, 20, 125]]
        elif self.n_value == 'all':
            scenario = [[100, 200, 21, 20, 100]]

        fitness = 0
        for _scenario in scenario:
            for i in range(self.num_simulation_each_solution):
                simulation_result = 0
                while simulation_result == 0:
                    try:
                        simulator = Simulator(solution, _scenario[0], _scenario[1], _scenario[2], _scenario[3], _scenario[4], 0.1)
                        simulation_result = simulator.simulate_mdpos()   
                    except Exception as ex:
                        pass
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
        return [_solution, _fitness]

    def cal_rank(self, pop):
        '''
        Calculate ranking for element in current population
        '''
        fit = []
        for i in range(len(pop)):
            fit.append(pop[i][1])
        arg_rank = np.array(fit).argsort()
        rank = [i / sum(range(1, len(pop) + 1)) for i in range(1, len(pop) + 1)]
        return rank

    def wheel_select(self, pop, prob):
        '''
        Select dad and mom from current population by rank
        '''
        r = np.random.random()
        sum = prob[0]
        for i in range(1, len(pop) + 1):
            if sum > r:
                return i - 1
            else:
                sum += prob[i]
        return sum

    def cross_over(self, dad_element, mom_element):
        '''
        crossover dad and mom choose from current population
        '''
        r = np.random.random()
        child1_element = []
        if r < self.cross_over_rate:
            for i in range(len(dad_element[0])):
                n = random.choice([0, 1])
                if n == 0:
                    child1_element.append(dad_element[0][i])
                else:
                    child1_element.append(mom_element[0][i])

            fit1 = self.compute_fitness(child1_element)
            if fit1 < dad_element[1] and fit1 < mom_element[1]:
                return [child1_element, fit1]
            return [child1_element, fit1]
        if dad_element[1] < mom_element[1]:
            return dad_element
        else:
            return mom_element

    def select(self, pop):
        '''
        Select from current population and create new population
        '''
        new_pop = []
            
        while len(new_pop) < self.population_size:
            rank = self.cal_rank(pop)
            dad_index = self.wheel_select(pop, rank)
            mom_index = self.wheel_select(pop, rank)
            while dad_index == mom_index:
                mom_index = self.wheel_select(pop, rank)
            dad = pop[dad_index]
            mom = pop[mom_index]
            new_sol1 = self.cross_over(dad, mom)
            new_pop.append(new_sol1)
            
        # for old_parent_idx in range(len(pop) / 5):
        #     new_pop[old_parent_idx] = pop[old_parent_idx]
            
        # sorted(new_pop, key=lambda new_pop: new_pop[1])
        
        return new_pop
    
    def mutate(self, pop):
        '''
        Mutate new population
        '''
        for i in range(len(pop)):
            for j in range(len(pop[i][0])):
                if random.uniform(0.0, 1.0) < self.mutation_rate:
                    pop[i][0][j] += random.gauss(0, self.sigma)
            pop[i][1] = self.compute_fitness(pop[i][0])
        return pop

    def early_stopping(self, array, patience=5):
        if patience <= len(array) - 1:
            value = array[len(array) - patience]
            arr = array[len(array) - patience + 1:]
            check = 0
            for val in arr:
                if val < value:
                    check += 1
            if check != 0:
                return False
            return True
        raise ValueError

    def evolve(self):
        print('|-> Start evolve with genertic algorithms')
        pop = [self.create_solution() for _ in range(self.population_size)]
        gbest = pop[0]
        g_best_arr = [gbest[1]]
        print('g_best at epoch 0: {}'.format(gbest[1]))
        for iter in range(self.epochs):
            print('Iteration {}'.format(iter + 1))
            start_time = time.time()
            pop = self.select(pop)
            pop = self.mutate(pop)

            for i in range(len(pop)):
                pop[i][1] = self.compute_fitness(pop[i][0])

            best_fit = min(pop, key=lambda x: x[1])
            if best_fit[1] < g_best_arr[-1]:
                gbest = best_fit

            g_best_arr.append(gbest[1])
            print('best current fit {}, best fit so far {}, iter {}'.format(best_fit[1], gbest[1], iter))
            print(' Time for running: {}'.format(time.time() - start_time))
        return gbest, np.array(g_best_arr)
