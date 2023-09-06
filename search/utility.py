from search_algorithm import Solution, Failure
from last_mile import LastMileProblem
from BestFirstSearch import BestFirstSearch
from BFS import BFS
from DLFS import DLFS
from IterativeSearch import IterativeSearch
import time

class Solver:
    def __init__(self, solver_type, prob : LastMileProblem, folder) -> None:
        self.solver_type = solver_type #type code to select an algorithm
        self.prob = prob #Last Mile problem
        self.folder = folder #folder to save results

    #method that solve the problem using a specific algorithm
    def solve(self): 
        #get the right solver
        solver = self.SolverSelector().get_solver(self.solver_type)

        #solve and calculate execution time
        start_time = time.time()
        solution = solver.solve(self.prob)
        stop_time = time.time()
        elapsed_time = stop_time-start_time

        #getting a solution description
        sol_description, solved = self.solution_description(solution, elapsed_time)
        if solved:
            self.plot_subgraph(solution)
        description = f"Solved with {self.solver_type}{sol_description}"
        
        #printing and writing the solution to a file
        FileWriter(self.folder).write_file(description)

    #method to plot a subgraph with visited places by the solution
    def plot_subgraph(self, solution : Solution):
        vertex = solution.visited_states()
        edges,costs = solution.actions_applied()
        self.prob.world.mappa.graph_creator.plot_subgraph(vertex, edges, costs, f'{self.folder}/{self.solver_type}-visited-places.svg')

    def solution_description(self, solution, elapsed): #function that gives a string descriptor of the solution
        res = ''
        solved = False

        #values to append to res if solution is valid
        if isinstance(solution, Solution):
            azioni = solution.actions
            cost = solution.total_cost
            res += "\n\tResult" + str(azioni)
            res += "\n\tCosto totale: "+ str(cost)
            res += '\n\tNumero azioni: ' + str(len(solution.actions))
            if solution.depth:
                res += '\n\tProfondità: ' + str(solution.depth)
            solved = True
        
        #values to append to res if solution is Failure
        elif isinstance(solution, Failure):
            res += "\nNessuna soluzione ammissibile"
            solved = False
        
        #values to appen in both cases
        res += f"\n\tTempo impiegato: {elapsed} secondi"
        
        if not isinstance(solution, int):
            res += "\n\tNodi espansi: " + str(solution.expanded_nodes)
            res += '\n\tNodi elaborati al secondo: ' + str(solution.expanded_nodes/elapsed)
        
        return res, solved

    class SolverSelector: 
        def __init__(self, depth = 15) -> None:
            self.solvers = {
                'BestFirstSearch' : BestFirstSearch(),
                'BFS' : BFS(),
                'DLFS' : DLFS(depth),
                'IterativeSearch' : IterativeSearch()
                }

        #get the right solver based on type code
        def get_solver(self, solver_type):
            return self.solvers[solver_type]

#class to write some strings in a txt file
class FileWriter:
    def __init__(self, folder) -> None:
        self.folder = folder

    def write_file(self, to_append):
        print(to_append)
        with open(self.folder + "/results.txt", "a")as f:
            f.write(f'{to_append}\n')

