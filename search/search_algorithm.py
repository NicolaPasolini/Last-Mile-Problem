from last_mile import LastMileProblem

class Nodo:
    def __init__(self, state, padre = None, action = None, g : int = 0 ) -> None:
        self.state = state #ad un nodo corrisponde uno stato
        self.padre = padre #da un nodo si deve poter risalire al nodo padre
        self.action = action #azione che ha portato a quel nodo
        self.g = g #costo totale per arrivare a quel nodo
    
    def __lt__(self, other):
        return self.g < other.g

    def __repr__(self) -> str:
        if(self.padre is None):
            return f"Stato: {self.state}, Padre: {self.padre}, Costo: {self.g}, Azione: {self.action}\n"
        else:
            return f"Stato: {self.state}, Padre: {self.padre.state}, Costo: {self.g}, Azione: {self.action}\n"

class Solution:
    def __init__(self, actions, total_cost, expanded_nodes, depth = None) -> None:
        self.actions = actions
        self.total_cost = total_cost
        self.expanded_nodes = expanded_nodes
        self.depth = depth

    def visited_states(self):
        visited = set()
        for i in self.actions:
            if not(i in visited):
                visited.add(i.partenza)
        
        return list(visited)
    
    def actions_applied(self):
        actions = list()
        cost = list()
        for i in self.actions:
            if not((i.destinazione, i.partenza) in actions):
                actions.append((i.partenza, i.destinazione))
                cost.append(i.cost)

        return actions, cost
    
class Failure():
    def __init__(self, expanded_nodes = None) -> None:
        self.expanded_nodes = expanded_nodes
 
class SearchAlgorithm:
    def __init__(self) -> None:
        self.counter = 0 #counter of expanded nodes

    def solve(self, problem) -> Solution:
        raise Exception('Must be implemented by subclasses')
    
    def extract_solution(self,node, depth = None) -> Solution:
        sol = list()
        cost = 0
        while (node.padre is not None):
            sol.insert(0,node.action)
            cost += node.action.cost
            node = node.padre
        return Solution(sol, cost, self.counter, depth)
    
    def is_goal(self, problem, nodo):
        if nodo.state != problem.init:
            return False
        
        reached = list()
        parent = nodo
        while(parent is not None):
            reached.append(parent.state)
            parent = parent.padre
        
        goal = problem.goal
        for i in goal:
            if(i not in reached):
                return False    
        return True
    
    def cammino_azioni(self, node) -> set:
        cammino = set()
        nodo = node
        while nodo.padre is not None:
            cammino.add(nodo.action)
            nodo = nodo.padre
        return cammino

    def espandi(self, problem, nodo) -> list:
        res = list()
        s = nodo.state
        successors_states = problem.get_successors(s)
        costo_padre = nodo.g
        for i in successors_states:
            azione = problem.actions[(s, i)]
            res.append(Nodo(i, nodo, azione, costo_padre + 1))
        self.counter += 1
        return res
    

