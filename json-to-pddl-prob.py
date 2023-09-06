import json

PATH = 'pddl/problem.pddl'
MAPPA = 'search/mappa.json'
CONFIG = 'search/config.json'

class PDDLINitializer:
    def __init__(self, mappa, config) -> None:
        with open(mappa) as f:
            self.data = json.loads(f.read())
        with open(config) as c:
            self.info = json.loads(c.read())
 
    def init_state(self):
        res = self.data
        val = '\t\t'

        for i in res['vertici']:
            val += f'{i} '

        val+= '- location'
        return val

    def init_functions(self):
        res = self.data
        val = ''

        for i in res['archi']:
            val+= f'\t\t(connected {i[0]} {i[1]})\n'
            val+= f'\t\t(connected {i[1]} {i[0]})\n'
        val+='\n'

        for i in range(len(res['archi'])):
            arco = res['archi'][i]
            cost = res['costi'][i]

            val+= f'\t\t(= (distance {arco[0]} {arco[1]}) {cost})\n'
            val+= f'\t\t(= (distance {arco[1]} {arco[0]}) {cost})\n'

        return val
    
    def init_goal(self):
        res = self.data
        val = ''
        val += f'and (at {self.info["init"]}) '
        for i in self.info['goal']:
            val += f'(delivered {i}) '
        
        return val

    def write_file(self, val):
        with open('init.txt', 'w') as f:
            f.write(val)

    def create_doc(self):
        res = '(define (problem trasporto-problema)\n\t(:domain trasporto)\n\t\t(:requirements :fluents)\n\n'
        res += f'\t(:objects\n{self.init_state()}\n\t)\n\n'
        res += f'\t(:init\n\t\t(at {self.info["init"]})\n\t\t(= (distanzaPercorsa) 0)\n{self.init_functions()}\n\t)\n'
        res += f'\t(:goal(\n\t\t{self.init_goal()}\n\t\t)\n\t)\n'
        res += '\t(:metric minimize (total-cost))\n)'
        return res

    def write_pddl(self, path):
        with open(path, 'w') as f:
            f.write(self.create_doc())

def run():
    pddl_initializer = PDDLINitializer(MAPPA, CONFIG)
    pddl_initializer.write_pddl(PATH)

if __name__ == '__main__':
    run()