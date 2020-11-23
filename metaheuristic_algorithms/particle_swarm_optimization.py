import numpy as np

from config import *
from blockchain_network.simulation import Simulator
from includes.utils import *


class Particle:
    def __init__(self, n_value=None):
        self.n_value = n_value
        self.element_length = 10
        self.position = random_parameter_combination(self.element_length)
        self.position = np.array(self.position)
        self.pbest_position = self.position
        self.velocity = np.zeros(self.position.shape)
        self.pbest_value = float('inf')

    def fix_parameter_after_update(self):
        for i in range(len(self.position)):
            if self.position[i] > 1:
                self.position[i] = random.uniform(0.9, 1)
            elif self.position[i] < 0:
                self.position[i] = random.uniform(0, 0.1)
        # sum_abs_position = 0
        # for i in range(len(self.position)):
            # sum_abs_position += np.abs(self.position[i])
        # for i in range(len(self.position)):
            # self.position[i] = self.position[i] / sum_abs_position

    def fitness(self, num_simulation_each_solution):
        # scenario = [[100, 200, 21, 20, 50]]
        # scenario = [[100, 200, 21, 20, 50], [100, 200, 21, 20, 75], [100, 200, 21, 20, 100]]

        # scenario = [[100, 200, 21, 20, 75]]
        # scenario = [[100, 200, 21, 20, 75], [100, 300, 21, 20, 75]]
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
        for i in range(num_simulation_each_solution):
            for _scenario in scenario:
                simulator = Simulator(self.position, _scenario[0], _scenario[1], _scenario[2], _scenario[3], _scenario[4])
                simulation_result = simulator.simulate_mdpos()
                fitness += simulation_result
        fitness /= (num_simulation_each_solution * len(scenario))

        return fitness


class PSOEngine:

    def __init__(self, population_size=10, epochs=200, num_simulation_each_solution=2):
        self.population_size = population_size
        self.epochs = epochs
        self.num_simulation_each_solution = num_simulation_each_solution

        self.particles = []
        self.gbest_value = float('inf')
        self.gbest_position = None
        self.gbest_particle = None
        self.max_w_old_velocation = 0.9
        self.min_w_old_velocation = 0.4
        self.w_local_best_position = 1.2
        self.w_global_best_position = 1.2

    def create_solution(self):
        pass

    def print_particle(self):
        pass

    def set_gbest(self):

        for particle in self.particles:
            fitness_candidate = particle.fitness(self.num_simulation_each_solution)
            if particle.pbest_value > fitness_candidate:
                particle.pbest_value = fitness_candidate
                particle.pbest_position = particle.position
            
            if self.gbest_value > fitness_candidate:
                self.gbest_value = fitness_candidate
                self.gbest_position = particle.position
                self.gbest_particle = particle

    def move_particles(self):
        for particle in self.particles:
            r1 = np.random.random_sample()
            r2 = np.random.random_sample()

            change_base_on_old_velocity = self.w_old_velocation * particle.velocity
            change_base_on_local_best = self.w_local_best_position * r1 * (particle.pbest_position - particle.position)
            change_base_on_global_best = self.w_global_best_position * r2 * (self.gbest_position - particle.position)

            new_velocity = change_base_on_old_velocity + change_base_on_local_best + change_base_on_global_best

            particle.velocity = new_velocity
            particle.position = particle.position + particle.velocity
            particle.fix_parameter_after_update()
            # particle.move()

    def early_stopping(self, array, patience=20):
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

    def check_most_n_value(self, fitness_arr, n):
        check = 0
        for i in range(len(fitness_arr) - 2, len(fitness_arr) - n, -1):
            if fitness_arr[i] == fitness_arr[-1]:
                check += 1
            if check == 4:
                return True
        return False

    def evolve(self):
        print('|-> Start tuning by particle swarm optimization')
        fitness_arr = []
        for iteration in range(self.epochs):
            self.w_old_velocation = (self.epochs - iteration) / self.epochs * (self.max_w_old_velocation - self.min_w_old_velocation) + self.min_w_old_velocation
            start_time = time.time()
            self.set_gbest()
            self.move_particles()
            # print('===> self.gbest_particle.position: {}'.format(self.gbest_particle.position))
            fitness_arr.append(round(self.gbest_value, 8))
            training_history = 'iteration: %d fitness = %.8f with time for running: %.2f '\
                % (iteration, self.gbest_value, time.time() - start_time)

            print(training_history)
            if iteration % 100 == 0:
                print(fitness_arr)
            # if len(fitness_arr) > 20:
            #     if self.early_stopping(fitness_arr):
            #         print('[X] -> Early stoping because the profit is not increase !!!')
            #         break
        print("The best solution in iterations: {} has fitness = {} in train set".format(iteration, self.gbest_value))
        return self.gbest_particle.position, np.array(fitness_arr)

