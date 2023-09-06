from mappa import Mappa

class LastMileProblem():
    def __init__(self, init, goal : list, world_type, size):
        self.init = init #init state
        self.goal = goal #place to be visited
        self.world = self.World(size, world_type) #create the world
        self.actions = self.add_actions(self.world.mappa) #add actions

    #add the actions based on the world
    def add_actions(self, mappa):
        actions = dict()
        vertici = mappa.graph.vs()
        for v in vertici:
            for n in v.neighbors():
                name = f"{v['name']}_to_{n['name']}"
                partenza = v['name']
                destinazione = n['name']
                costo = mappa.graph.es[mappa.get_edge_id(partenza, destinazione)]['distance']
                actions[(partenza, destinazione)] = self.Move(name, partenza, destinazione, costo)
        
        return actions

    #given a state returns a set with the next states
    def get_successors(self, state) -> set:
        res = set()
        for a in self.actions:
            if(self.actions[a].partenza == state):
                res.add(self.actions[a].destinazione)
        return res
    
    #given a state returns a set with the possible actions in the state
    def get_actions(self, state):
        res = list()
        for action in self.actions:
            a = self.actions[action]
            if(a.partenza == state):
                res.append(a)
        return res

    class Action:
        def __init__(self, name, cost):
            self.name = name
            self.cost = cost
        
        def __repr__(self) -> str:
            return f"{self.name} ({self.cost})"

    class Move(Action):
        def __init__(self, name, partenza, destinazione, cost):
            self.partenza = partenza
            self.destinazione = destinazione
            super().__init__(name, cost)

    class World:
        def __init__(self, size, world_type):
            self.mappa = Mappa(size, world_type)
            self.states = self.mappa.get_states()
