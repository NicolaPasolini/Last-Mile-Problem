from search_algorithm import SearchAlgorithm
from DLFS import DLFS

class IterativeSearch(SearchAlgorithm):
    def __init__(self) -> None:
        self.counter = 0
        self.depth = 0

    def solve(self, problem) -> list:
        while True:
            self.depth += 1
            solver = DLFS(self.depth)
            solution = solver.solve(problem)
            if solution != self.depth:
                return solution 