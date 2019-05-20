class Ant:

    def __init__(self, ID):
        self.road = [ID]
        self.ID = ID
        self.cost = 0.

    def ref_trail(self, node):
        self.road.append(node)
        # self.cost += cost

    def clear(self):
        self.road = [self.ID]
        self.cost = 0.


class Lane:

    def __init__(self, cost):
        self.cost = cost
        self.phero = 1.

    def ref_phero(self, phero):
        self.phero += phero


import numpy as np
# import random

colony_size = 5

evap = 0.2
delta = 1

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

# for key in lanes.keys():
#   print(key, lanes[key].cost, lanes[key].phero)
for k in range(10):
    while 1:
        try:
            for ant in ants.values():

                total = 0
                prob = []

                for node in range(colony_size):
                    if node not in ant.road:
                        prob.append([lanes[str(ant.road[-1]) + '-' + str(node)].phero/cost[ant.road[-1], node], node])
                        # print(type(lanes[str(ant.road[-1]) + '-' + str(node)].phero))
                        total += lanes[str(ant.road[-1]) + '-' + str(node)].phero/cost[ant.road[-1], node]
                for i in range(len(prob)):
                    if i > 0:
                        prob[i][0] = prob[i][0]/total + prob[i-1][0]
                    else:
                        prob[i][0] /= total

                val = np.random.random()

                for i in prob:
                    if val <= i[0]:
                        ant.ref_trail(i[1])
                        break
                else:
                    ant.ref_trail(prob[-1][1])
        except IndexError:
            break

    for lane in lanes.values():
        lane.ref_phero(-lane.phero*evap)
        # print(lane.phero)

    for ant in ants.values():
        ant.ref_trail(ant.ID)
        # print(ant.road)
        for i in range(len(ant.road) - 1):
            lanes[str(ant.road[i]) + '-' + str(ant.road[i+1])].ref_phero(delta)
            lanes[str(ant.road[i+1]) + '-' + str(ant.road[i])].ref_phero(delta)

    if k < 9:
        for ant in ants.values():
            ant.clear()

for ant in ants.values():
    print(ant.road)
