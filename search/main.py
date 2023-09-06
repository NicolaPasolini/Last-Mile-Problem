from last_mile import LastMileProblem
from utility import FileWriter, Solver
import os, json
from datetime import datetime

#here we can define the 'configuration' of the problem
def get_info():

    now = datetime.now()
    now_string = now.strftime("%d-%m-%Y-%H:%M")

    with open('config.json') as f:
        info = json.loads(f.read())
    
    init = info['init']
    goal = info['goal']
    size = info['size']
    world_type = info['world_type']
    solvers = info['solvers']
    folder = f'{info["folder_path"]}/{now_string}-{world_type}-{len(goal)}locations'
    world_params = f'{world_type} {folder}' 
    
    try:
        os.makedirs(folder)
    except:
        pass
    
    return init, goal, size, world_params, folder, solvers

#core of the application
def run():
    #initialization
    init, goal, size, world_type, folder, solvers = get_info()
    prob = LastMileProblem(init, goal, world_type, size)
    
    #print general info about the problem and save the map to a file
    general_info = f'Init state ->{init}\nGoal ->{str(goal)}'
    FileWriter(folder).write_file(general_info)
    prob.world.mappa.graph_creator.plot_graph(prob.world.mappa.graph, folder + '/mappa.svg')
    
    #getting solutions
    for s in solvers:
        Solver(s, prob, folder).solve()

if __name__ == '__main__':
    run()
