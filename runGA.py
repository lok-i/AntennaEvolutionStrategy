import pygad
import numpy
from src.AntennaArray import PatchAntennaArray


param_opt_range = {'x':{'equal_to':0.},
                   'y':{'equal_to':0.},
                   'z':{'equal_to':0.},
                   'A':{'greater_than':0.,'lesser_than':5.},
                   'beta':{'equal_to':0.},
                   'W':{'equal_to':10.7e-3},
                   'L':{'equal_to':10.47e-3},
                   'h':{'equal_to':3e-3},}

PatchArray = PatchAntennaArray(n_patches=2,
                               Freq=14e9,
                               Er=2.5,
                               param_range=param_opt_range)

print('Opt_values_range:\n',PatchArray.params_to_opt_range)

# print('initial_elements:\n',PatchArray.element_array)
# update_to = [0.,0.,1.,0.,0.,1.]
# PatchArray.update_array_params(update_to)
# print('updates_elements:\n',PatchArray.element_array)


def fitness_func(solution, solution_idx):
    # Calculating the fitness value of each solution in the current population.
    # The fitness function calulates the sum of products between each input and its corresponding weight.
    # print("Solution:",solution)
    PatchArray.CalculateFieldSumPatch()
    PatchArray.update_array_params(solution)
    fitness = PatchArray.get_gain()
    return fitness

fitness_function = fitness_func

num_generations = 500 # Number of generations.
num_parents_mating = 20 # Number of solutions to be selected as parents in the mating pool.

# To prepare the initial population, there are 2 ways:
# 1) Prepare it yourself and pass it to the initial_population parameter. This way is useful when the user wants to start the genetic algorithm with a custom initial population.
# 2) Assign valid integer values to the sol_per_pop and num_genes parameters. If the initial_population parameter exists, then the sol_per_pop and num_genes parameters are useless.
sol_per_pop = 100 # Number of solutions in the population.
num_genes = len(PatchArray.params_to_opt_range)
gene_ranges = [numpy.arange(start=p_2_opt_range[0],
                             stop=p_2_opt_range[1],
                             step=(p_2_opt_range[1]-p_2_opt_range[0])/10.).tolist()
               for p_2_opt_range in PatchArray.params_to_opt_range  ]
print(gene_ranges)
# init_range_low = -1.#[2,-2,-2,-2,-2,-2]
# init_range_high = 1.#[5,5,5,5,5,5]

parent_selection_type = "sss" # Type of parent selection.
keep_parents = 7 # Number of parents to keep in the next population. -1 means keep all parents and 0 means keep nothing.

crossover_type = "single_point" # Type of the crossover operator.

# Parameters of the mutation operation.
mutation_type = "random" # Type of the mutation operator.
mutation_percent_genes = 10 # Percentage of genes to mutate. This parameter has no action if the parameter mutation_num_genes exists or when mutation_type is None.

last_fitness = 0
def callback_generation(ga_instance):
    global last_fitness
    print("Generation = {generation}".format(generation=ga_instance.generations_completed))
    print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution()[1]))
    print("Change     = {change}".format(change=ga_instance.best_solution()[1] - last_fitness))
    last_fitness = ga_instance.best_solution()[1]

# Creating an instance of the GA class inside the ga module. Some parameters are initialized within the constructor.
ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating, 
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop, 
                       num_genes=num_genes,
                    #    init_range_low=init_range_low,
                    #    init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes,
                       on_generation=callback_generation,
                       gene_space = gene_ranges,
                       )

# Running the GA to optimize the parameters of the function.
ga_instance.run()

# After the generations complete, some plots are showed that summarize the how the outputs/fitenss values evolve over generations.
ga_instance.plot_result()

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution()
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))


if ga_instance.best_solution_generation != -1:
    print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

# Saving the GA instance.
filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
ga_instance.save(filename=filename)

# Loading the saved GA instance.
loaded_ga_instance = pygad.load(filename=filename)
loaded_ga_instance.plot_result()