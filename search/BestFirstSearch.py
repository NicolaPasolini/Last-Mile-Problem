from search_algorithm import SearchAlgorithm
from queue import PriorityQueue
from search_algorithm import Nodo, Failure
from last_mile import LastMileProblem

class BestFirstSearch(SearchAlgorithm):
    def __init__(self) -> None:
        self.counter = 0

    def solve(self, problem : LastMileProblem) -> list:
        init_node = Nodo(state=problem.init)
        self.frontiera = PriorityQueue()
        self.frontiera.put(init_node)
        while(not self.frontiera.empty()):
            nodo = self.frontiera.get()
            if(super().is_goal(problem, nodo)):
                return self.extract_solution(nodo)
            espandi = self.espandi(problem, nodo)
            for i in espandi:
                if not(i.action in super().cammino_azioni(nodo)):
                    self.frontiera.put(i)
        return Failure(self.counter)

    def espandi(self, problem : LastMileProblem, nodo : Nodo) -> list:
        res = list()
        s = nodo.state
        successors_states = problem.get_successors(s)
        costo_padre = nodo.g
        for i in successors_states:
            azione = problem.actions[(s, i)]
            costo = costo_padre + azione.cost
            res.append(Nodo(i, nodo, azione, costo))
        self.counter += 1
        return res
    
