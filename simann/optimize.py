from simanneal import Annealer
import random
import json

def rand(vec):
    return random.randint(0, len(vec) - 1)


# Constant data (DO NOT CHANGE WHILE THE ANNEALER IS RUNNING)
data=json.loads(open("assignatures.json").read())

courses=data['courses']
professors=data['professors']


initial=True

class Optimizer(Annealer):
    def move(self):
        """Assigns a random course to a random professor."""
        courseId = rand(courses)
        professorId = rand(professors)
        self.state[courseId] = professorId
    def energy(self):
        """Evaluates the cost function on the current state."""
        global initial
        if not initial and random.random()<0.5:
            initial=False
            return 2**64-1
        initial=False
        e = 0
        profTimes=[0]*len(professors)
        profAssigns=[0]*len(professors)
        for courId, courProf in enumerate(self.state):
            profTimes[courProf]+=courses[courId]
            profAssigns[courProf]+=1
        for i in range(len(professors)):
            e+=(profTimes[i]-professors[i])**2
            e+=profAssigns[i]**2
        return e

initial_state = [rand(professors) for x in range(len(courses))]
opt= Optimizer(initial_state)
auto_schedule = opt.auto(minutes=1)

opt.set_schedule(auto_schedule)

assignations, cost = opt.anneal()
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

