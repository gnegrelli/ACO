import numpy as np


class Ant:

    def __init__(self, ID):
        self.road = [ID]
        self.ID = ID
        self.cost = 0.

    def ref_trail(self, node, cost):
        self.road.append(node)
        self.cost += cost

    def clear(self):
        self.road = [self.ID]
        self.cost = 0.


class Lane:

    def __init__(self, cost):
        self.cost = cost
        self.phero = 1.

    def ref_phero(self, phero):
        self.phero += phero


colony_size = 5

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

for i in range(5):
    for j in range(5):
        lanes[str(i) + '-' + str(j)] = Lane(cost[i, j])

for k in range(100):

    # Wipe ants
    for ant in ants.values():
        ant.clear()

    while 1:
        try:
            for ant in ants.values():

                total = 0
                prob = []

                # Evaluate probability of remaining lanes
                for node in range(colony_size):
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
                    ant.ref_trail(prob[-1][1])
        except IndexError:
            break

    print("\n\nRound #%d" % k)

    # for keys in lanes.keys():
    #     print(keys, lanes[keys].phero)

    # Evaporate old pheromone from lanes
    for lane in lanes.values():
        lane.ref_phero(-lane.phero*evap)

    for ant in ants.values():
        # Ants return to initial node
        ant.ref_trail(ant.ID, cost[ant.road[-1], ant.ID])

        # Update pheromone on lanes
        for i in range(len(ant.road) - 1):
            lanes[str(ant.road[i]) + '-' + str(ant.road[i+1])].ref_phero(delta/ant.cost)
            lanes[str(ant.road[i+1]) + '-' + str(ant.road[i])].ref_phero(delta/ant.cost)

    for ant in ants.values():
        print(ant.road, ant.cost)

print("\n\nFinal Solution:")

for ant in ants.values():
    print(ant.road)
