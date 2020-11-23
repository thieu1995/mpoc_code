import time 

import numpy as np

class WoaEngine:
    def __init__(self, population_size=100, epochs=500, num_simulation_each_solution=2):
        self.population_size = population_size
        self.epochs = epochs
        self.num_simulation_each_solution = num_simulation_each_solution

        self.particles = []
        self.gbest_value = float('inf')
        self.gbest_position = None
        self.gbest_particle = None

    def set_gbest(self):
        for particle in self.particles:
            fitness_candidate = particle.fitness(self.num_simulation_each_solution)

            if fitness_candidate < self.gbest_value:
                self.gbest_value = fitness_candidate
                self.gbest_position = particle.position
                self.gbest_particle = particle
    
    def evolve(self):
        fitness_arr = []
        for epoch in range(self.epochs):
            epoch_start_time = time.time()
            self.set_gbest()
            a = 2 * np.cos(epoch / (self.epochs - 1))

            for particle in self.particles:

                r = np.random.rand()
                A = 2 * a * r - a
                C = 2 * r
                l = np.random.uniform(-1, 1)
                b = 1
                p = np.random.rand()

                if p < 0.5:
                    if np.abs(A) < 1:
                        D = np.abs(C * self.gbest_position - particle.position)
                        particle.position = self.gbest_position - A * D
                    else:
                        random_agent_idx = np.random.randint(0, len(self.particles))
                        random_particle = self.particles[random_agent_idx]
                        D = np.abs(C * random_particle.position - particle.position)
                        particle.position = random_particle.position - A * D
                else:
                    D = np.abs(self.gbest_position - particle.position)
                    particle.position = D * np.exp(b * l) * np.cos(2 * np.pi * l) + self.gbest_position
                
                particle.fix_parameter_after_update()
                # particle.move()
            fitness_arr.append(self.gbest_value)
            print('===> self.gbest_position: {}'.format(self.gbest_position))
            training_history = 'Iteration {}, best fitness = {} with time = {}'\
                .format(epoch, fitness_arr[-1], round(time.time() - epoch_start_time, 4))
            print(training_history)
        return self.gbest_particle.position, np.array(fitness_arr)
