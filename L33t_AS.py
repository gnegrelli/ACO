import numpy as np
import copy


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


# Method configuration
colony_size = 100

max_gen = 1000
gen = 0

evap = 0.1
delta = 1.
a = 2
b = 3.

# Create lanes (edges of graph) reading file
lanes = dict()

data = open('Cities5.txt').read().split("\n")
n_nodes = int(data[0].strip())
for row in data[1:]:
    if row.strip() and row[0] is not '#':
        i, j, d = row.split(",")
        lanes[i + '-' + j] = Lane(float(d))
        lanes[j + '-' + i] = Lane(float(d))

# Create ants
ants = dict()

for ID in range(colony_size):
    ants[ID] = Ant(ID)

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
                        try:
                            prob.append([(lanes[str(ant.road[-1]) + '-' + str(node)].phero**a)/(lanes[str(ant.road[-1]) + '-' + str(node)].cost**b), node])
                            total += (lanes[str(ant.road[-1]) + '-' + str(node)].phero**a)/(lanes[str(ant.road[-1]) + '-' + str(node)].cost**b)
                        except KeyError:
                            lanes[str(ant.road[-1]) + '-' + str(node)] = Lane(9999)
                            lanes[str(node) + '-' + str(ant.road[-1])] = Lane(9999)
                            prob.append([(lanes[str(ant.road[-1]) + '-' + str(node)].phero**a)/(lanes[str(ant.road[-1]) + '-' + str(node)].cost**b), node])
                            total += (lanes[str(ant.road[-1]) + '-' + str(node)].phero**a)/(lanes[str(ant.road[-1]) + '-' + str(node)].cost**b)
                for i in range(len(prob)):
                    if i > 0:
                        prob[i][0] = prob[i][0]/total + prob[i-1][0]
                    else:
                        prob[i][0] /= total

                val = np.random.random()

                for i in prob:
                    if val <= i[0]:
                        ant.ref_trail(i[1], lanes[str(ant.road[-1]) + '-' + str(i[1])].cost)
                        break
                else:
                    ant.ref_trail(prob[-1][1], lanes[str(ant.road[-1]) + '-' + str(prob[-1][1])].cost)
        except IndexError:
            break

    # Evaporate old pheromone from lanes
    for lane in lanes.values():
        lane.ref_phero(-lane.phero*evap)

    for ant in ants.values():
        # Ants return to initial node
        ant.ref_trail(ant.road[0], lanes[str(ant.road[-1]) + '-' + str(ant.road[0])].cost)

        # Update pheromone on lanes
        for i in range(len(ant.road) - 1):
            lanes[str(ant.road[i]) + '-' + str(ant.road[i+1])].ref_phero(delta/ant.cost)
            lanes[str(ant.road[i+1]) + '-' + str(ant.road[i])].ref_phero(delta/ant.cost)

    # Initialize best ant
    if gen == 0:
        best_ant = copy.copy(ants[0])

    # Check if there is a better ant in this generation
    for ant in ants.values():
        if ant.cost < best_ant.cost:
            best_ant = copy.copy(ant)

    # Update pheromone on lanes travelled by the best ant
    for i in range(len(best_ant.road) - 1):
        lanes[str(best_ant.road[i]) + '-' + str(best_ant.road[i + 1])].ref_phero(5*delta/best_ant.cost)
        lanes[str(best_ant.road[i + 1]) + '-' + str(best_ant.road[i])].ref_phero(5*delta/best_ant.cost)

    # print("\n\nRound #%d" % gen)
    # for ant in ants.values():
    #     print(ant.road, ant.cost)

    # print("Best:")
    # print(best_ant.road)

    gen += 1.

# print("\n")
# print(50*'\u2660')
# print("\nFinal Solution:")

# for ant in ants.values():
#     print("Ant #%d: \t%s -> %.2f" % (ant.ID, ant.road, ant.cost))
print("%s, %.4f" % (best_ant.road, best_ant.cost))