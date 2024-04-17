class Edge:
    """ Represents an edge in a graph with optional directional properties.

    Attributes:
        from_node (Any): The starting node of the edge.
        to_node (Any): The ending node of the edge.
        weight (float): The weight of the edge.
        start_time (datetime): The start time of the edge's validity.
        end_time (datetime): The end time of the edge's validity.
        direction (Optional[str]): The direction of the edge ('to', 'from', or None for undirected).
    """
    def __init__(self, from_node: Any, to_node: Any, weight: float, start_time: datetime, end_time: datetime, direction: Optional[str] = None):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
        self.start_time = start_time
        self.end_time = end_time
        self.direction = direction  # None for undirected edges, 'to' for directed edges from 'from_node' to 'to_node', and 'from' for the opposite

    @property
    def weight(self) -> float:
        return self._weight

    @weight.setter
    def weight(self, value: float):
        if value < 0:
            raise ValueError("Weight cannot be negative.")
        self._weight = value

    @property
    def nodes(self) -> Tuple[Any, Any]:
        return self.from_node, self.to_node

    @property
    def time_range(self) -> Tuple[datetime, datetime]:
        return self.start_time, self.end_time

    @property
    def duration(self) -> float:
        return (self.end_time - self.start_time).total_seconds()
