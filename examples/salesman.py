from __future__ import print_function
import math
import random
from simanneal import Annealer
import networkx as nx


def distance(a, b):
    """Calculates distance between two latitude-longitude coordinates."""
    R = 3963  # radius of Earth (miles)
    lat1, lon1 = math.radians(a[0]), math.radians(a[1])
    lat2, lon2 = math.radians(b[0]), math.radians(b[1])
    return math.acos(math.sin(lat1) * math.sin(lat2) +
                     math.cos(lat1) * math.cos(lat2) * math.cos(lon1 - lon2)) * R


class TravellingSalesmanProblem(Annealer):

    """Test annealer with a travelling salesman problem.
    """
    
    # pass extra data (the distance matrix) into the constructor
    def __init__(self, state, distance_matrix):
        self.distance_matrix = distance_matrix
        super(TravellingSalesmanProblem, self).__init__(state)  # important! 

    def move(self):
        """Swaps two cities in the route."""
        a = random.randint(0, len(self.state) - 1)#
        b = random.randint(0, len(self.state) - 1)
        self.state[a], self.state[b] = self.state[b], self.state[a]

    def energy(self):
        """Calculates the length of the route."""
        e = 0
        for i in range(len(self.state)):
            e += self.distance_matrix[self.state[i-1]][self.state[i]]
        return e

class recalculatebySA(Annealer):
    def distance(self , tpath ,graph):
        '''
            cost+=graph[][]['cost']
        '''
        if len(tpath) == 2:
            return self.graph[tpath[0]][tpath[1]]['cost']
        if len(tpath) == 1:
            return 0
        
        else:
            cost = 0
            for i in (0,len(tpath)-2):
                cost = cost + self.graph[tpath[i]][tpath[i+1]]['cost']
        return cost
    def __init__(self , state , graph):
        self.graph = graph
        self.path = {}
        self.flow = {}
        super(recalculatebySA, self).__init__(state) 
    def move(self):
        #2 method to move ?!? 
        '''
        for flowkey in self.flow.keys():
            self.state[flowkey] = self.path[flowkey][random.randint(0, len(self.path[flowkey]) - 1)]
        '''
        #random select a key
        #'''
        li = list(self.flow.keys())
        flowkey = li[random.randint(0, len(li) - 1)]
        #random select a path
        self.state[flowkey] = self.path[flowkey][random.randint(0, len(self.path[flowkey]) - 1)]
        #'''


    def energy(self):
        '''
            all the cost
        '''
        e = 0
        for flowkey in self.flow.keys():
            e = e + self.distance(self.state[flowkey] , self.graph)

        return e



if __name__ == '__main__':
    '''
        test function
    '''
    # init a graph
    g = nx.Graph()
    g.add_edge(1,2,weight=1)
    g.add_edge(1,3,weight=1)
    g.add_edge(2,4,weight=1)
    g.add_edge(3,4,weight=1)
    g[1][2]['cost'] = 2
    g[1][3]['cost'] = 2
    g[2][4]['cost'] = 2
    g[3][4]['cost'] = 2
    g.add_edge(2,3,weight=1)
    g[2][3]['cost'] = 3

    #init some flows
    flow = {}
    path = {}
    selectpath = {}
    app = []
    '''
    for a in nx.shortest_simple_paths(g, source=1,target=4, weight='cost'):
        app.append(a)
    print (app)
    '''
    flow[('10.0.0.1','10.0.0.4')] = {'ip_src':'10.0.0.1','ip_dst':'10.0.0.4','src':1,'dst':4} 
    flow[('10.0.0.2','10.0.0.3')] = {'ip_src':'10.0.0.2','ip_dst':'10.0.0.3','src':2,'dst':3} 
    flow[('10.0.0.4','10.0.0.2')] = {'ip_src':'10.0.0.4','ip_dst':'10.0.0.2','src':4,'dst':2} 
    flow[('10.0.0.4','10.0.0.1')] = {'ip_src':'10.0.0.4','ip_dst':'10.0.0.1','src':4,'dst':1} 
    flow[('10.0.0.3','10.0.0.4')] = {'ip_src':'10.0.0.3','ip_dst':'10.0.0.4','src':3,'dst':4} 
    for flowkey in flow.keys():
            '''
                generator must change to list or dict
            '''
            path[flowkey] = []
            for a in nx.shortest_simple_paths(g, source=flow[flowkey]['src'],
                                             target=flow[flowkey]['dst'], weight='cost'):
                path[flowkey].append(a)
    for flowkey in flow:
            selectpath[flowkey] = path[flowkey][random.randint(0, len(path[flowkey]) - 1)]
            #print self.selectpath[flowkey]
    tsp = recalculatebySA(selectpath , g )
    tsp.path = path
    tsp.flow = flow
    tsp.copy_strategy = "method"
    state, e = tsp.anneal()
    print (selectpath)
    print ("cost %d" % e )
    print (state)
    """
    state results are wrong but the enegry ,or the cost is right
    cost 15
    {('10.0.0.2', '10.0.0.3'): [2, 3], ('10.0.0.1', '10.0.0.4'): [1, 3, 2, 4], ('10.0.0.4', '10.0.0.2'): [4, 2],
    ('10.0.0.3' , '10.0.0.4'): [3, 4], ('10.0.0.4', '10.0.0.1'): [4, 2, 1]}
    3+7+2+2+4???
    """

    # initial state, a randomly-ordered itinerary
    # init_state = list(cities.keys())
    # random.shuffle(init_state)

    # # create a distance matrix
    # distance_matrix = {}
    # for ka, va in cities.items():
    #     distance_matrix[ka] = {}
    #     for kb, vb in cities.items():
    #         if kb == ka:
    #             distance_matrix[ka][kb] = 0.0
    #         else:
    #             distance_matrix[ka][kb] = distance(va, vb)

    # initial_state = ['Phoenix','Columbus','Charlotte','New York City', 'Los Angeles', 'Houston']
    # tsp = TravellingSalesmanProblem(init_state, distance_matrix)
    # # since our state is just a list, slice is the fastest way to copy
    # tsp.copy_strategy = "slice"  
    # state, e = tsp.anneal()

    # while state[0] != 'New York City':
    #     state = state[1:] + state[:1]  # rotate NYC to start
    # print("%i mile route:" % e)
    # for city in state:
    #     print("\t", city)

