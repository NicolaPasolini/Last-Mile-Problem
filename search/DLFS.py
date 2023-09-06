from search_algorithm import SearchAlgorithm
from queue import LifoQueue, PriorityQueue
from search_algorithm import Nodo, Solution, Failure

class DLFS(SearchAlgorithm):
    def __init__(self, depth) -> None:
        self.depth = depth
        self.counter = 0

    def solve(self, problem) -> list:
        result = Failure()
        frontiera = LifoQueue()
        initNode = Nodo(problem.init)
        frontiera.put(initNode)
        while not frontiera.empty():
            nodo = frontiera.get()
            if(super().is_goal(problem, nodo)):
                return super().extract_solution(nodo, self.depth)
            if(nodo.g > self.depth):
                result = self.depth
            else:
                for i in super().espandi(problem, nodo):
                    if not(i.action in super().cammino_azioni(nodo)):
                        frontiera.put(i)              
        if isinstance(result, Failure):
            result.expanded_nodes = self.counter
        return result
    
