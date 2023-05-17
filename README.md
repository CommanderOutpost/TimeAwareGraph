# Time-Aware Graph
The Time-Aware Graph is a data structure that represents a graph, whose edges and nodes are subject to change over time. This type of graph is particularly useful in domains that require modeling of dynamic relationships such as social network analysis, transport logistics, and epidemic modeling.

In this document, we describe each component of the Time-Aware Graph data structure, including the `Node`, `Edge`, and `Graph` classes, and their respective methods.

## Node
The `Node` class is a basic unit of the Time-Aware Graph. Each node can be connected to other nodes via edges.
```
class Node:
    def __init__(self, value):
        self.value = value
        self.edges = []
```
In the constructor, a node is initialized with a value that can be any data type, and an empty list of edges.
### Methods
1.  `add_edge`: Adds an edge to the current node.
```
def add_edge(self, node, weight, start_time, end_time, direction=None):
    self.edges.append(Edge(self, node, weight, start_time, end_time, direction))
```
This function accepts five parameters:
* `node` : The node at the other end of the edge.
* `weight`: The weight of the edge. This could be any metric relevant to the specific problem domain such as distance, cost, etc.
* `start_time` and `end_time`: The datetime objects specifying when the edge starts and ends.
* `direction`: The direction of the edge. Can be `None` for undirected edges, `'to'` for directed edges from `from_node` to `to_node`, and `'from'` for the opposite.

2. `get_edges` : Returns all edges connected to the current node.
```
def get_edges(self):
    return self.edges
```

3. `get_edges_at_time`: Returns all edges that are active at a given time.
```
def get_edges_at_time(self, time: datetime) -> List[Edge]:
    return [edge for edge in self.edges if edge.start_time <= time <= edge.end_time]
```
This function filters the edges based on their start_time and end_time attributes.

4. `get_nearest_neighbors`: Returns all neighboring nodes that are reachable at a given time.
```
def get_nearest_neighbors(self, time: datetime) -> List['Node']:
    neighbors = [edge.to_node if (edge.direction == 'to' or edge.direction is None) and edge.from_node == self else edge.from_node for edge in self.get_edges_at_time(time) if edge.start_time <= time <= edge.end_time]
    return neighbors
```
This function uses the get_edges_at_time method to identify active edges, and checks the direction of each edge to determine the neighboring nodes.

5. `remove_edge`: Removes a specified edge from the node.
```
def remove_edge(self, edge: Edge):
    if edge in self.edges:
        if (edge.direction == 'to' and edge.from_node == self) or (edge.direction == 'from' and edge.to_node == self) or edge.direction is None:
            self.edges.remove(edge)
```
This function removes the edge if it exists in the node's edge list and if the edge's direction allows removal from the current node.

6. `get_degree`: Returns the degree of the node (i.e., the number of edges) at a given time.
```
def get_degree(self, time: datetime) -> int:
    return len(self.get_nearest_neighbors(time))
```
This function uses the get_nearest_neighbors method to identify the number of active neighboring nodes at the given time.

7. `__str__` and `__repr__`: These are special methods in Python classes that return a string representation of the object. In this case, they return the value of the node.
```
def __str__(self):
    return f"{self.value}"

def __repr__(self):
    return f"{self.value}"
```

## Edge
The `Edge` class represents a connection between two nodes in the Time-Aware Graph.
```
class Edge:
    def __init__(self, from_node, to_node, weight, start_time, end_time, direction=None):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.start_time = start_time
        self.end_time = end_time
        self.direction = direction  # None for undirected edges, 'to' for directed edges from 'from_node' to 'to_node', and 'from' for the opposite
```
In the constructor, an edge is initialized with the following parameters:

* `from_node` and `to_node`: The nodes at either end of the edge.
* `weight`: The weight of the edge.
* `start_time` and `end_time`: The datetime objects specifying when the edge starts and ends.
* `direction`: The direction of the edge. Can be `None` for undirected edges, 'to' for directed edges from from_node to to_node, and 'from' for the opposite.
### Methods
1. `get_weight`: Returns the weight of the edge.
```
def get_weight(self):
    return self.weight
```
2. `get_nodes`: Returns a tuple containing the source node 'from_node' and the destination node 'to_node' of the edge.
```
def get_nodes(self):
    return self.from_node, self.to_node
```
3. `get_time_range`: Returns a tuple containing the start time and end time of the edge.
```
def get_time_range(self):
    return self.start_time, self.end_time

```
4. `get_duration`: Calculates and returns the duration of the edge, which is the difference in seconds between the start time and end time.
```
def get_duration(self):
    return (self.end_time - self.start_time).total_seconds()
```
## Graph
```
def __init__(self):
    self.nodes = []
```

1. `add_node`: 
