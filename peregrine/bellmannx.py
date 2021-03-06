import math
import networkx as nx
from utils import last_index_in_list


class NegativeWeightFinder:

    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.predecessor = {}
        self.distance_to = {}
    
    def initialize(self, source):
        for node in self.graph:
            # Initialize all distance_to values to infinity and all predecessor values to None
            self.distance_to[node] = float('Inf')
            self.predecessor[node] = None
        # The distance from any node to (itself) == 0
        self.distance_to[source] = 0

    def bellman_ford(self, source):
        """
        :param source: The node in graph from which the values in distance_to will be calculated.
        """
        self.initialize(source)
        # After len(graph) - 1 passes, algorithm is complete.
        for i in range(len(self.graph) - 1):
            # for each node in the graph, test if the distance to each of its siblings is shorter by going from
            # source->base_currency + base_currency->quote_currency
            for edge in self.graph.edges(data=True):
                if self.distance_to[edge[0]] + edge[2]['weight'] < self.distance_to[edge[1]]:
                    self.distance_to[edge[1]] = self.distance_to[edge[0]] + edge[2]['weight']
                    self.predecessor[edge[1]] = edge[0]

        # todo: if a negative cycle is found, does that mean source is definitely in it? (probably not)
        # todo: how to (efficiently) tell if a found negative cycle contains source?
        # would checking if edge[1] or edge[0] == source indicate it is a cycle ending at source?
        found_negative = False
        for edge in self.graph.edges(data=True):
            if self.distance_to[edge[0]] + edge[2]['weight'] < self.distance_to[edge[1]]:
                self.distance_to[edge[1]] = self.distance_to[edge[0]] + edge[2]['weight']
                self.predecessor[edge[1]] = edge[0]
                found_negative = True

        if found_negative:
            return retrace_negative_loop(self.predecessor, source)


def bellman_ford(graph, source):
    return NegativeWeightFinder(graph).bellman_ford(source)


def retrace_negative_loop(predecessor, start):
    arbitrage_loop = [start]
    next_node = start
    while True:
        next_node = predecessor[next_node]
        if next_node not in arbitrage_loop:
            arbitrage_loop.insert(0, next_node)
        else:
            arbitrage_loop.insert(0, next_node)
            arbitrage_loop = arbitrage_loop[:last_index_in_list(arbitrage_loop, next_node) + 1]
            return arbitrage_loop


def calculate_profit_ratio_for_path(graph, path):
    money = 1
    for i in range(len(path)):
        if i + 1 < len(path):
            start = path[i]
            end = path[i + 1]
            rate = math.exp(-graph[start][end])
            money *= rate
    return money
