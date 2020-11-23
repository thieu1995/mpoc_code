import numpy as np
from math import gamma

from includes.utils import *
from blockchain_network.simulation import Simulator

class QsoEngine():
    ID_POS = 0
    ID_FIT = 1
    def __init__(self, population_size=None, epochs=None, num_simulation_each_solution=None, n_value=None):
        self.population_size = population_size
        self.epoch = epochs
        self.num_simulation_each_solution = num_simulation_each_solution
        self.n_value = n_value
        self.element_length = 10
        self.domain_range = [0, 1]

    def _calculate_queue_length__(self, t1, t2 , t3):
        """
        calculate length of each queue based on  t1, t2,t3
        """
        n1 = (1/t1)/((1/t1) + (1/t2) + (1/t3))
        n2 = (1/t2)/((1/t1) + (1/t2) + (1/t3))
        n3 = (1/t3)/((1/t1) + (1/t2) + (1/t3))
        q1 = int(n1*self.population_size)
        q2 = int(n2*self.population_size)
        q3 = self.population_size - q1 - q2
        return q1, q2, q3
    
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
        return [np.array(_solution), _fitness]
    
    def _amend_solution_and_return__(self, solution=None):
        for i in range(self.element_length):
            if solution[i] < self.domain_range[0] or solution[i] > self.domain_range[1]:
                solution[i] = np.random.uniform(self.domain_range[0], self.domain_range[1])
        return solution

    def _update_bussiness_1__(self, pop, current_iter, max_iter):
        sorted_pop = sorted(pop, key = lambda x: x[1])
        s1, s2, s3 = sorted_pop[0:3]
        A1, A2 , A3 = s1[0], s2[0], s3[0]
        t1, t2 , t3 = s1[1], s2[1], s3[1]
        q1, q2, q3 = self._calculate_queue_length__(t1, t2, t3)
        for i in range(self.population_size):
            if i < q1:
                if i == 0:
                    case = 1
                A = A1
            elif i >= q1 and  i < q1 + q2:
                if i == q1 :
                    case = 1
                A = A2
            else:
                if i == q1 + q2 :
                    case = 1
                A = A3
            beta = np.power(current_iter, np.power(current_iter/max_iter, 0.5))
            alpha = np.random.uniform(-1, 1)
            solution_shape = pop[0][0].shape
            E = np.random.exponential(0.5, solution_shape)
            e = np.random.exponential(0.5)
            F1 = beta*alpha*(E*np.abs(A - pop[i][0])) + e*A - e*pop[i][0]
            F2 = beta*alpha*(E*np.abs(A - pop[i][0]))
            if case == 1:
                X_new = A + F1
                X_new = self._amend_solution_and_return__(X_new)
                new_fit = self.compute_fitness(solution=X_new)
                if new_fit < pop[i][1]:
                    pop[i] = [X_new, new_fit]
                    case = 1
                else:
                    case = 2
            else:
                X_new = pop[i][0] + F2
                X_new = self._amend_solution_and_return__(X_new)
                new_fit = self.compute_fitness(solution=X_new)
                if new_fit < pop[i][1]:
                    pop[i] = [X_new, new_fit]
                    case = 2
                else:
                    case = 1
        return pop

    def _update_bussiness_2__(self, pop):
        sorted_pop = sorted(pop, key=lambda x:x[1])
        s1, s2, s3 = sorted_pop[0:3]
        A1, A2 , A3 = s1[0], s2[0], s3[0]
        t1, t2 , t3 = s1[1], s2[1], s3[1]
        #print("t1 {} , t2 {} , t3 {}".format(t1,t2,t3))
        q1, q2, q3 = self._calculate_queue_length__(t1, t2, t3)
        pr = [i/self.population_size for i in range(1,self.population_size + 1)]
        cv = t1/(t2+t3)
        for i in range(self.population_size):
            if i < q1:
                A = A1
            elif i >= q1 and i < q1 + q2:
                A = A2
            else:
                A = A3
            if np.random.random() < pr[i]:
                i1, i2 = np.random.choice(self.population_size, 2, replace=False)
                X1 = pop[i1][0]
                X2 = pop[i2][0]
                e = np.random.exponential(0.5)
                F1 = e*(X1-X2)
                F2 = e*(A-X1)
                if np.random.random() < cv:
                    X_new = sorted_pop[i][0] + F1
                    X_new = self._amend_solution_and_return__(X_new)
                    fit = self.compute_fitness(X_new)
                else:
                    X_new = sorted_pop[i][0] + F2
                    X_new = self._amend_solution_and_return__(X_new)
                    fit = self.compute_fitness(X_new)
                if fit < sorted_pop[i][1]:
                    sorted_pop[i] = [X_new, fit]
        return sorted_pop      
    
    def _update_bussiness_3__(self, pop):
        sorted_pop = sorted(pop, key=lambda x: x[1])
        pr = [ i/self.population_size for i in range(1, self.population_size + 1)]
        for i in range(self.population_size):
            X_new = np.zeros_like(pop[0][0])
            for j in range(self.element_length):
                if np.random.random() > pr[i]:
                    i1, i2 = np.random.choice(self.population_size, 2, replace=False)
                    e = np.random.exponential(0.5)
                    X1 = pop[i1][0]
                    X2 = pop[i2][0]
                    X_new[j] = X1[j] + e*(X2[j]- sorted_pop[i][self.ID_POS][j])
                else:
                    X_new[j] = sorted_pop[i][self.ID_POS][j]
            X_new = self._amend_solution_and_return__(X_new)
            fit = self.compute_fitness(X_new)
            if fit < sorted_pop[i][1]:
                sorted_pop[i] = [X_new, fit]
        return sorted_pop

    def evolve(self):
        pop = [self.create_solution() for _ in range(self.population_size)]
        sorted_pop = None
        self.loss_train = []
        for current_iter in range(self.epoch):
            pop = self._update_bussiness_1__(pop, current_iter, self.epoch)
            pop = self._update_bussiness_2__(pop)
            pop = self._update_bussiness_3__(pop)
            sorted_pop = sorted(pop, key=lambda x:x[1])
            # if(current_iter%50==0):
            print("best fit ", sorted_pop[0][1]," in gen ", current_iter)
            # print(sorted_pop[0])
            self.loss_train.append(sorted_pop[0][1])
        print("best fit ", sorted_pop[0][1])
        print("best pos", sorted_pop[0][0])
        return sorted_pop[0][0], self.loss_train
