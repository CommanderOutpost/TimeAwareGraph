class Edge:
    def __init__(self, from_node, to_node, start_time, end_time):
        self.from_node = from_node
        self.to_node = to_node
        self.start_time = start_time
        self.end_time = end_time

    def get_nodes(self):
        return self.from_node, self.to_node

    def get_time_range(self):
        return self.start_time, self.end_time

