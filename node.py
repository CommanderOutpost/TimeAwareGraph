from typing import List
from datetime import datetime
from edge import Edge 

class Node:
    def __init__(self, value):
        self.value = value
        self.edges = []

def add_edge(self, node, weight, start_time, end_time, direction=None):
    edge = Edge(self, node, weight, start_time, end_time, direction)
    self.edges.append(edge)
    def get_edges(self):
        return self.edges

    def get_edges_at_time(self, time: datetime) -> List[Edge]:
        return [edge for edge in self.edges if edge.start_time <= time <= edge.end_time]

def get_nearest_neighbors(self, time: datetime) -> List['Node']:
    neighbors = [edge.to_node if (edge.direction == 'to' or edge.direction is None) and edge.from_node == self else edge.from_node for edge in self.get_edges_at_time(time)]
    return neighbors

def remove_edge(self, edge: Edge):
    if edge in self.edges and ((edge.direction == 'to' and edge.from_node == self) or (edge.direction == 'from' and edge.to_node == self) or edge.direction is None):
        self.edges.remove(edge)
                
    def get_degree(self, time: datetime) -> int:
        return len(self.get_nearest_neighbors(time))

    def __str__(self):
        return f"{self.value}"

    def __repr__(self):
        return f"{self.value}"
