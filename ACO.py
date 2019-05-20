import numpy as np


class Ant:

    def __init__(self, ID):
        self.ID = ID
        self.road = []
        self.cost = 0.

    def ref_trail(self, node, cost):
        self.road.append(node)
        self.cost += cost

    def start(self, node):
        self.road = [node]
        self.cost = 0.


class Lane:

    def __init__(self, cost):
        self.cost = cost
        self.phero = 1.

    def ref_phero(self, phero):
        self.phero += phero


colony_size = 5
n_nodes = 5

max_gen = 100
gen = 0

evap = 0.2
delta = 1.
a = 1.
b = 1.

ants = dict()
lanes = dict()

# Create ants
for ID in range(colony_size):
    ants[ID] = Ant(ID)

# Cost matrix
cost = np.array([[0., 1., 2.2, 2., 4.1],
                 [1., 0., 1.4, 2.2, 4.],
                 [2.2, 1.4, 0., 2.2, 3.2],
                 [2., 2.2, 2.2, 0., 2.2],
                 [4.1, 4., 3.2, 2.2, 0.]])

# Create lanes (edges of graph)
for i in range(n_nodes):
    for j in range(i + 1, n_nodes):
        lanes[str(i) + '-' + str(j)] = Lane(cost[i, j])
        lanes[str(j) + '-' + str(i)] = Lane(cost[i, j])

while gen < max_gen:

    # Start ants
    for ant in ants.values():
        ant.start(np.random.randint(n_nodes))

    while 1:
        try:
            for ant in ants.values():

                total = 0
                prob = []

                # Evaluate probability of remaining lanes
                for node in range(n_nodes):
                    if node not in ant.road:
                        prob.append([(lanes[str(ant.road[-1]) + '-' + str(node)].phero**a)/(cost[ant.road[-1], node]**b), node])
                        total += (lanes[str(ant.road[-1]) + '-' + str(node)].phero**a)/(cost[ant.road[-1], node]**b)
                for i in range(len(prob)):
                    if i > 0:
                        prob[i][0] = prob[i][0]/total + prob[i-1][0]
                    else:
                        prob[i][0] /= total

                val = np.random.random()

                for i in prob:
                    if val <= i[0]:
                        ant.ref_trail(i[1], cost[ant.road[-1], i[1]])
                        break
                else:
                    ant.ref_trail(prob[-1][1], cost[ant.road[-1], prob[-1][1]])
        except IndexError:
            break

    # Evaporate old pheromone from lanes
    for lane in lanes.values():
        lane.ref_phero(-lane.phero*evap)

    for ant in ants.values():
        # Ants return to initial node
        ant.ref_trail(ant.road[0], cost[ant.road[-1], ant.road[0]])

        # Update pheromone on lanes
        for i in range(len(ant.road) - 1):
            lanes[str(ant.road[i]) + '-' + str(ant.road[i+1])].ref_phero(delta/ant.cost)
            lanes[str(ant.road[i+1]) + '-' + str(ant.road[i])].ref_phero(delta/ant.cost)

    print("\n\nRound #%d" % gen)
    for ant in ants.values():
        print(ant.road, ant.cost)

    gen += 1.

print("\n")
print(50*'\u2660')
print("\nFinal Solution:")

for ant in ants.values():
    print(ant.road)
