from typing import List, Tuple, Dict
from datetime import timedelta
from datetime import datetime
from node import Node
from edge import Edge

class Graph:
    def __init__(self):
        self.nodes = []

    def add_node(self, value):
        node = Node(value)
        self.nodes.append(node)
        return node

    def add_edge(self, from_node, to_node, start_time, end_time):
        from_node.add_edge(to_node, start_time, end_time)

    def get_nodes(self):
        return self.nodes

    def shortest_path(self, start_node: Node, end_node: Node, start_time: datetime, end_time: datetime) -> List[Node]:
        distances = {node: (float('infinity'), None) for node in self.nodes}  # Node -> (distance, previous node)
        distances[start_node] = (0, None)
        distances[end_node] = (float('infinity'), None)  # Add end_node to distances dictionary

        unvisited_nodes = self.nodes.copy()

        while unvisited_nodes:
            current_node = min(unvisited_nodes, key=lambda node: distances[node][0])  # Node with the smallest distance
            unvisited_nodes.remove(current_node)

            if current_node == end_node:
                break

            current_distance, _ = distances[current_node]

            for edge in current_node.get_edges_at_time(start_time):
                if edge.end_time > end_time:
                    continue  # Ignore edges outside the time window

                alternative_distance = current_distance + (edge.end_time - start_time).total_seconds()

                if alternative_distance < distances[edge.to_node][0]:
                    distances[edge.to_node] = (alternative_distance, current_node)

        path = []
        current_node = end_node
        while current_node is not None:
            path.append(current_node)
            _, current_node = distances[current_node]
        path.reverse()

        return path if distances[end_node][0] != float('infinity') else None

    def get_evolution(self, start_time: datetime, end_time: datetime) -> Dict[datetime, List[Edge]]:
        evolution = defaultdict(list)
        time = start_time

        while time <= end_time:
            for node in self.nodes:
                active_edges = node.get_edges_at_time(time)
                if active_edges:
                    evolution[time].extend(active_edges)
            time += timedelta(minutes=1)  # Adjust the time step as needed

        return dict(evolution)

    def remove_node(self, node: Node):
        if node in self.nodes:
            self.nodes.remove(node)
            for edge in node.get_edges():
                edge.from_node.remove_edge(edge)
                edge.to_node.remove_edge(edge)

    def get_edge_history(self, node1: Node, node2: Node) -> List[Tuple[datetime, datetime]]:
        history = []
        for edge in node1.get_edges():
            if edge.to_node == node2 or edge.from_node == node2:
                history.append(edge.get_time_range())
        return history

    def get_active_nodes(self, time: datetime) -> List[Node]:
        active_nodes = [node for node in self.nodes if node.get_edges_at_time(time)]
        return active_nodes

    
    def is_connected(self, time: datetime) -> bool:
        if not self.nodes:
            return True

        visited = set()
        to_visit = [self.nodes[0]]

        while to_visit:
            current = to_visit.pop()
            if current not in visited:
                visited.add(current)
                to_visit.extend(node for edge in current.get_edges_at_time(time) for node in edge.get_nodes() if node != current)

        return len(visited) == len(self.nodes)


    def get_connected_components(self, time: datetime) -> List[List[Node]]:
        visited = set()
        components = []

        for node in self.nodes:
            if node not in visited:
                component = []
                to_visit = [node]

                while to_visit:
                    current = to_visit.pop()
                    if current not in visited:
                        visited.add(current)
                        component.append(current)
                        to_visit.extend(node for edge in current.get_edges_at_time(time) for node in edge.get_nodes() if node != current)

                components.append(component)

        return components
