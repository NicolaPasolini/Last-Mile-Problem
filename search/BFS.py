from search_algorithm import SearchAlgorithm
from queue import Queue
from search_algorithm import Nodo, Failure
from last_mile import LastMileProblem

class BFS(SearchAlgorithm):
    def solve(self, problem : LastMileProblem):
        initNode = Nodo(problem.init)
        if super().is_goal(problem, initNode):
            return super().extract_solution(initNode)
        frontiera = Queue()
        frontiera.put(initNode)
        while(not frontiera.empty()):
            nodo = frontiera.get()
            for f in super().espandi(problem, nodo):
                s = f.state
                if super().is_goal(problem, f):
                    return super().extract_solution(f)
                if (not(f.action in super().cammino_azioni(nodo))):
                    frontiera.put(f)
        return Failure(self.counter)
    