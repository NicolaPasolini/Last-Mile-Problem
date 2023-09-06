import igraph as ig
import networkx as nx
import matplotlib.pyplot as plt
import string, random, json

FIRST_POINT = - 4
SECOND_POINT = 1
FIRST_RAND = 5
LAST_RAND = 40

class Mappa:
    def __init__(self, size, type) -> None:
        self.graph_creator = GraphManager()
        self.graph = self.graph_creator.create_graph(size, type)
    
    def get_edge_id(self, start, end):
        for i in range(len(self.graph.get_edgelist())):
            v = self.graph.get_edgelist()[i]
            partenza = self.graph.vs[v[0]]['name']
            arrivo = self.graph.vs[v[1]]['name']

            if(partenza == start and arrivo == end):
                return i
            if(partenza == end and arrivo == start):
                return i

    def get_costo(self, start, end):
        id = self.get_edge_id(start, end)
        return self.graph.es["distance"][id]
    
    def get_vertex(self, name):
        for i in self.graph.vs():
            if(i['name'] == name):
                return i
        return None
    
    def get_states(self):
        return self.graph.vs()

class GraphManager:
    def grafo_random(self, node_number, folder):
        #elementi per definire il grafo
        archi = list()
        costi = list()
        vertexes = list()

        #definizione dei vertici
        for i in range(node_number):
            vertexes.append(string.ascii_uppercase[i])
        
        #definizione degli archi
        for i in range(len(vertexes)):
            for j in range(i,len(vertexes)):
                if i != j:
                    value = random.randint(FIRST_POINT, SECOND_POINT)
                    if value > 0:
                        value = int(value / value) * random.randint(FIRST_RAND, LAST_RAND)
                        archi.append((vertexes[i], vertexes[j]))
                        costi.append(value)
        
        return self.to_json(archi, vertexes, costi, folder+'/grafo-random')

    def mappa_romana(self, size, folder):
        #elementi per definire il grafo
        vertexes = list()
        archi = list()
        costi = list()

        #definizione dei vertici del grafo
        for i in range(size*size):
            vertexes.append(string.ascii_uppercase[i])
        
        count = 0
        matrix = list()
        for i in range(size):
            matrix.append(list())
            for j in range(size):
                matrix[i].append(vertexes[count])
                count += 1

        #definizione degli archi del grafo
        for i in range(size):
            for j in range(size-1):
                archi.append((matrix[i][j], matrix[i][j+1]))
        for i in range(size):
            for j in range(size-1):
                archi.append((matrix[j][i], matrix[j+1][i]))
        
        #definizione dei costi degli archi del grafo
        for i in range(len(archi)):
            costi.append(random.randint(FIRST_RAND, LAST_RAND))

        return self.to_json(archi, vertexes, costi, folder+'/grafo-square')

    def to_json(self, archi, vertici, costi, name = None):
        res = {
            'archi' : archi,
            'vertici' : vertici,
            'costi' : costi
        }
        res = json.dumps(res)

        if name is not None:
            with open(name+'.json', 'w') as f:
                f.write(res)

        return res

    def plot_graph(self, graph : ig.Graph, path):
        g = graph
        visual_style = {}
        visual_style['vertex_size'] = 40
        visual_style['vertex_label'] = g.vs['name']
        visual_style["vertex_label"] = g. vs ["name"]
        visual_style["edge_label"] = g.es ["distance"]
        visual_style["layout"] = g.layout("kk")
        ig.plot (g, target=path, **visual_style)

    def plot_subgraph(self, vertex, edges, costs, path):
        g = ig.Graph()
        g.add_vertices(vertex)
        g.add_edges(edges)
        g.es["distance"] = costs
        self.plot_graph(g, path)
        
    def create_graph(self, size, type) -> ig.Graph:
        g = ig.Graph()

        #definizione del tipo di grafo da creare
        params = type.split(' ')
        type = params[0]
        if type == 'random':
            json_res = self.grafo_random(size, params[1]) #un grafo randomico con size nodi
        elif type == 'square':
            json_res = self.mappa_romana(size, params[1]) #un grafo rettangolare con size*size nodi
        elif type == 'fixed':
            json_res = self.mappa_statica('mappa.json')
        
        json_res = json.loads(json_res)

        #aggiunta degli elementi definiti negli altri metodi al grafo vero e proprio
        g.add_vertices(json_res['vertici'])
        g.add_edges(json_res['archi'])
        g.es["distance"] = json_res['costi']

        return g
    
    def mappa_statica(self, json_file : None):
        if json_file is not None:
            with open(json_file, 'r') as f:
                json_res = f.read()
            
            return json_res
            
