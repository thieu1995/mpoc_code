import numpy as np
from copy import deepcopy

from includes.utils import *
from blockchain_network.simulation import Simulator


class HsgoEngine:
    def __init__(self, population_size=50, n_clusters=5, epochs=500, num_simulation_each_solution=2, n_value=None):
        self.element_length = 10
        self.population_size = population_size
        self.n_clusters = n_clusters
        self.epochs = epochs
        self.num_simulation_each_solution = num_simulation_each_solution
        self.n_value = n_value
        self.n_elements = int(self.population_size / self.n_clusters)

    def compute_fitness(self, solution):
        '''
        Simulate blockchain network by parameters
        '''
        # scenario = [[100, 200, 21, 20, 50]]
        # scenario = [[100, 200, 21, 20, 50], [100, 200, 21, 20, 75], [100, 200, 21, 20, 100]]
        # scenario = [[100, 200, 21, 20, 75]]
        # scenario = [[100, 200, 21, 20, 100], [100, 300, 21, 20, 100]]
        # scenario = [[100, 200, 21, 20, 50], [100, 300, 21, 20, 50], [100, 200, 21, 20, 75], [100, 300, 21, 20, 75], 
        #             [100, 200, 21, 20, 100], [100, 300, 21, 20, 100]]
        if self.n_value == 75:
            scenario = [[100, 200, 21, 20, 75]]
        elif self.n_value == 100:
            scenario = [[100, 200, 21, 20, 100]]
        elif self.n_value == 125:
            scenario = [[100, 200, 21, 20, 125]]
        elif self.n_value == 'all':
            scenario = [[100, 200, 21, 20, 75], [100, 200, 21, 20, 100], [100, 200, 21, 20, 125]]

        fitness = 0
        for _scenario in scenario:
            for i in range(self.num_simulation_each_solution):
                simulator = Simulator(solution, _scenario[0], _scenario[1], _scenario[2], _scenario[3], _scenario[4])
                simulation_result = simulator.simulate_mdpos()
                fitness += simulation_result
        fitness /= (self.num_simulation_each_solution * len(scenario))
        return fitness

    def create_population(self):
        pop = []
        group = []

        for i in range(self.n_clusters):
            team = []
            for j in range(self.n_elements):
                solution = random_parameter_combination(self.element_length)
                fitness = self.compute_fitness(solution)
                team.append([solution, fitness, i])
                pop.append([solution, fitness, i])
            group.append(team)
        return pop, group

    def _get_best_solution_in_team(self, group=None):
        list_best = []
        for i in range(len(group)):
            sorted_team = sorted(group[i], key=lambda temp: temp[1])
            list_best.append(deepcopy(sorted_team[0]) )
        return list_best

    def evolve(self):
        T0 = 298.15
        K = 1.0
        beta = 1.0
        alpha = 1
        epxilon = 0.05

        l1 = 5E-2
        l2 = 100.0
        l3 = 1E-2
        H_j = l1 * np.random.uniform()
        P_ij = l2 * np.random.uniform()
        C_j = l3 * np.random.uniform()

        pop, group = self.create_population()

        g_best = max(pop, key=lambda x: x[1])     # single element  ??? Need check max
        
        p_best = self._get_best_solution_in_team(group) 

        loss_train = []
        for epoch in range(self.epochs):
            ## Loop based on the number of cluster in swarm (number of gases type)
            for i in range(self.n_clusters):
                ### Loop based on the number of individual in each gases type
                for j in range(self.n_elements):
                    F = -1.0 if np.random.uniform() < 0.5 else 1.0
                    ##### Based on Eq. 8, 9, 10
                    H_j = H_j * np.exp(-C_j * ( 1.0/np.exp(-epoch/self.epochs) - 1.0/T0 ))

                    S_ij = K * H_j * P_ij
                    # print(np.array((S_ij * g_best[0] - group[i][j][0])))
                    gama = beta * np.exp(- ((p_best[i][1] + epxilon) / (group[i][j][1] + epxilon)))
                    X_ij = group[i][j][0] + F * np.random.uniform() * gama * (np.array(p_best[i][0]) - np.array(group[i][j][0])) + \
                        F * np.random.uniform() * alpha * np.array((S_ij * np.array(g_best[0]) - group[i][j][0]))
                    fit = self.compute_fitness(X_ij)
                    group[i][j] = [X_ij, fit, i]
                    pop[i * self.n_elements + j] = [X_ij, fit, i]
            ## Update Henry's coefficient using Eq.8
            H_j = H_j * np.exp(-C_j * (1.0 / np.exp(-epoch / self.epochs) - 1.0 / T0))
            ## Update the solubility of each gas using Eq.9
            S_ij = K * H_j * P_ij
            ## Rank and select the number of worst agents using Eq. 11
            N_w = int(self.population_size * (np.random.uniform(0, 0.1) + 0.1))
            ## Update the position of the worst agents using Eq. 12
            sorted_id_pos = np.argsort([ x[1] for x in pop ])

            for item in range(N_w):
                id = sorted_id_pos[item]
                j = id % self.n_elements
                i = int((id-j) / self.n_elements)
                X_new = np.random.uniform(0, 1, self.element_length)
                fit = self.compute_fitness(X_new)
                pop[id] = [X_new, fit, i]
                group[i][j] = [X_new, fit, i]

            p_best = self._get_best_solution_in_team(group)
            current_best = min(pop, key=lambda x: x[1])
            if current_best[1] < g_best[1]:
                g_best = deepcopy(current_best)
            loss_train.append(g_best[1])
            print("Generation : {0}, best result so far: {1}".format(epoch + 1, g_best[1]))
        print('=== results ===')
        print(g_best[0])
        print(loss_train)
        print('====')
        return g_best[0], np.array(loss_train)
