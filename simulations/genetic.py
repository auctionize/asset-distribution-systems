from pyeasyga import pyeasyga
import random
import json

def rand(vec):
    return random.randint(0, len(vec) - 1)


# Constant data (DO NOT CHANGE WHILE THE GA IS RUNNING)
data=json.loads(open("assignatures.json").read())

courses=data['courses']
professors=data['professors']


initial=True

# initialise the GA
ga = pyeasyga.GeneticAlgorithm(data,
                            population_size=200,
                            generations=5000,
                            crossover_probability=0.6,
                            mutation_probability=0.4,
                            elitism=True,
                            maximise_fitness=False)

# define and set function to create a candidate solution representation
def create_individual(data):
    return [rand(data['professors']) for x in range(len(data['courses']))]

ga.create_individual = create_individual

# define and set the GA's crossover operation
def crossover(parent_1, parent_2):
    index = random.randrange(1, len(parent_1))
    child_1 = parent_1[:index] + parent_2[index:]
    child_2 = parent_2[:index] + parent_1[index:]
    return child_1, child_2

ga.crossover_function = crossover

# define and set the GA's mutation operation
def mutate(individual):
    courseId = rand(courses)
    professorId = rand(professors)
    individual[courseId] = professorId

ga.mutate_function = mutate

# define and set the GA's selection operation
def selection(population):
    return random.choice(population)

ga.selection_function = selection

# define a fitness function
def fitness (individual, data):
    ''' Simulate restrictions
    global initial
    if not initial and random.random()<0.5:
        initial=False
        return 2**64-1
    initial=False
    '''
    e = 0
    profTimes=[0]*len(professors)
    profAssigns=[0]*len(professors)
    #print(individual)
    for courId, courProf in enumerate(individual):
        profTimes[courProf]+=courses[courId]
        profAssigns[courProf]+=1
    for i in range(len(professors)):
        e+=(profTimes[i]-professors[i])**2
        e+=profAssigns[i]**2
    return e

ga.fitness_function = fitness       # set the GA's fitness function
ga.run()                            # run the GA

# ALGO FINISHED

cost, assignations = ga.best_individual()
#cost = fitness(assignations, [])
print("Cost", cost)
print("Assignations", assignations)

profTimes=[0]*len(professors)
profAssigns=[0]*len(professors)
for courId, courProf in enumerate(assignations):
    profTimes[courProf]+=courses[courId]
    profAssigns[courProf]+=1
print("profTimes", profTimes)
print("profTimes-profs", [profTimes[i]-professors[i] for i in range(len(profTimes))])
print("profAssigns", profAssigns)

