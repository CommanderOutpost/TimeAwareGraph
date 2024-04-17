from typing import List, Tuple, Dict
from datetime import timedelta, datetime
from collections import defaultdict
from node import Node
from edge import Edge

class Graph:
def __init__(self):
    self.nodes = set()

    def add_node(self, value):
        node = Node(value)
        self.nodes.append(node)
        return node

    def add_edge(self, from_node, to_node, start_time, end_time, weight, direction=None):
        from_node.add_edge(to_node, weight, start_time, end_time, direction)

    def get_nodes(self):
        return self.nodes

    def shortest_path(self, start_node: Node, end_node: Node, start_time: datetime, end_time: datetime) -> List[Node]:
        distances = {node: (float('infinity'), None) for node in self.nodes}  # Node -> (distance, previous node, current time)
        distances[start_node] = (0, None, start_time)

        unvisited_nodes = self.nodes.copy()

        while unvisited_nodes:
            current_node = min(unvisited_nodes, key=lambda node: distances[node][0])  # Node with the smallest distance
            unvisited_nodes.remove(current_node)

            if current_node == end_node:
                break

            current_distance, _, current_time = distances[current_node]

            for edge in current_node.get_edges_at_time(current_time):
                if edge.end_time > end_time:
                    continue  # Ignore edges outside the time window

                alternative_distance = current_distance + edge.get_duration()

                if alternative_distance < distances[edge.to_node][0]:
                    distances[edge.to_node] = (alternative_distance, current_node, edge.end_time)

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
                active_edges = [edge for edge in node.get_edges_at_time(time) if (edge.direction == 'to' and edge.from_node == node) or (edge.direction == 'from' and edge.to_node == node) or edge.direction is None]
                if active_edges:
                    evolution[time].extend(active_edges)
            time += timedelta(minutes=1)  # Adjust the time step as needed

        return dict(evolution)

    def remove_node(self, node: Node):
        if node in self.nodes:
            self.nodes.remove(node)
            for edge in node.get_edges():
                if (edge.direction == 'to' and edge.from_node == node) or (edge.direction == 'from' and edge.to_node == node) or edge.direction is None:
                    edge.from_node.remove_edge(edge)
                    edge.to_node.remove_edge(edge)

    def get_edge_history(self, node1: Node, node2: Node) -> List[Tuple[datetime, datetime]]:
        history = []
        for edge in node1.get_edges():
            if (edge.to_node == node2 and edge.direction in ['to', None]) or (edge.from_node == node2 and edge.direction in ['from', None]):
                history.append(edge.get_time_range())
        return history

    def get_active_nodes(self, time: datetime) -> List[Node]:
        active_nodes = [node for node in self.nodes if node.get_edges_at_time(time) and node.get_nearest_neighbors(time)]
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
                to_visit.extend(node for node in current.get_nearest_neighbors(time))

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
                        to_visit.extend(node for node in current.get_nearest_neighbors(time))

                components.append(component)

        return components

    def bfs(self, start_node: Node) -> List[Node]:
        visited = set()
        queue = [start_node]
        traversal = []

        while queue:
            current_node = queue.pop(0)
            if current_node not in visited:
                visited.add(current_node)
                traversal.append(current_node)
                queue.extend(edge.to_node for edge in current_node.get_edges() if edge.to_node not in visited)

        return traversal

    def dfs(self, start_node: Node) -> List[Node]:
        visited = set()
        stack = [start_node]
        traversal = []

        while stack:
            current_node = stack.pop()
            if current_node not in visited:
                visited.add(current_node)
                traversal.append(current_node)
                stack.extend(edge.to_node for edge in current_node.get_edges() if edge.to_node not in visited)

        return traversal


    def _dfs(self, node: Node, visited: set, rec_stack: set) -> bool:
        visited.add(node)
        rec_stack.add(node)

        for edge in node.get_edges():
            neighbor = edge.to_node if edge.from_node == node else edge.from_node
            if neighbor not in visited:
                if self._dfs(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    def has_cycle(self) -> bool:
        visited = set()
        rec_stack = set()

        for node in self.nodes:
            if node not in visited:
                if self._dfs(node, visited, rec_stack):
                    return True
        return False
