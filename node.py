from typing import List
from datetime import datetime
from edge import Edge 

class Node:
    def __init__(self, value):
        self.value = value
        self.edges = []

    def add_edge(self, node, start_time, end_time):
        self.edges.append(Edge(self, node, start_time, end_time))

    def get_edges(self):
        return self.edges

    def get_edges_at_time(self, time: datetime) -> List[Edge]:
        return [edge for edge in self.edges if edge.start_time <= time <= edge.end_time]

    def get_nodes_at_time(self, time: datetime) -> List['Node']:
        return [node for node in self.nodes if node.get_edges_at_time(time)]

    def remove_edge(self, edge: Edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def get_nearest_neighbors(self, time: datetime) -> List['Node']:
        neighbors = [edge.to_node if edge.from_node == self else edge.from_node for edge in self.get_edges_at_time(time)]
        return neighbors

    def get_degree(self, time: datetime) -> int:
        return len(self.get_edges_at_time(time))

    def __str__(self):
        return f"Node: {self.value}"

    def __repr__(self):
        return f"Node: {self.value}"