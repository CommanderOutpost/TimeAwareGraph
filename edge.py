class Edge:
    def __init__(self, from_node, to_node, weight, start_time, end_time, direction=None):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.start_time = start_time
        self.end_time = end_time
        self.direction = direction  # None for undirected edges, 'to' for directed edges from 'from_node' to 'to_node', and 'from' for the opposite


    def get_weight(self):
        return self.weight

    def get_nodes(self):
        return self.from_node, self.to_node

    def get_time_range(self):
        return self.start_time, self.end_time

    def get_duration(self):
        return (self.end_time - self.start_time).total_seconds()
    
