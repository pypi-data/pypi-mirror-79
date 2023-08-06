from typing import Set, Tuple, Dict


class Node:
    """A node in an abstract argumentation framework, usually a single argument."""
    __default_node_prefix = "A"

    def __init__(self, node_id, name: str = ""):
        self.id = node_id
        self.parents: Set[Node] = set()
        self.parents_edges = dict()  # Dict[Node.id, Edge]
        self.children: Set[Node] = set()
        self.children_edges = dict()  # Dict[Node.id, Edge]
        self.value = None  # float
        self.interval = None  # Tuple[float, float]
        self.prob_var = None  # z3.ArithRef
        if not name:
            self.name = self.__default_node_prefix + str(self.id)
        else:
            self.name = name

    def add_value(self, value: float):
        self.value = value

    def add_interval(self, interval: Tuple[float, float]):
        self.interval = interval

    def is_initial(self):
        return len(self.parents) == 0

    def get_parent_edge(self, node_from):
        if node_from.id in self.parents_edges:
            return self.parents_edges[node_from.id]
        else:
            raise ValueError("Node '" + self.name + "' has no parent edge from node '" + node_from.name + "'.")

    def get_child_edge(self, node_to):
        if node_to.id in self.children_edges:
            return self.children_edges[node_to.id]
        else:
            raise ValueError("Node '" + self.name + "' has no child edge to node '" + node_to.name + "'.")

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id

    def __gt__(self, other):
        return self.id > other.id

    def __hash__(self):
        return hash(self.id)

    def __repr__(self):
        return self.name
        # return "Node(" + self.id + ": " + self.name + ")"


class Edge:
    """A directed edge in an abstract argumentation framework, usually an attack."""
    __default_label_prefix = "s"  # default label "s_A_B" for an attack from node A to node B

    def __init__(self, node_from, node_to, label=""):
        self.node_from: Node = node_from
        self.node_to: Node = node_to
        self.label: str = label
        self.value = None
        self.interval = None
        self.prob_var = None  # z3.ArithRef
        if self.label == "":
            self.label = self.__default_label_prefix + '_' + self.node_from.name + '_' + self.node_to.name
        self.node_from.children.add(self.node_to)
        self.node_from.children_edges[node_to.id] = self
        self.node_to.parents.add(self.node_from)
        self.node_to.parents_edges[node_from.id] = self

    def add_value(self, value: float):
        self.value = value

    def add_interval(self, interval: Tuple[float, float]):
        self.interval = interval


class AF:
    """A class representing an abstract argumentation framework."""
    def __init__(self, name: str = ""):
        self.name = name
        self.nodes: Dict[str, Node] = dict()
        self.edges: Set[Edge] = set()

    def add_node(self, node: Node):
        self.nodes[node.id] = node

    def add_edge(self, edge: Edge):
        self.edges.add(edge)

    def get_node(self, node_id: str):
        return self.nodes[node_id]

    def get_nodes(self):
        return self.nodes.values()

    def get_node_by_name(self, name: str):
        for node in self.get_nodes():
            if node.name == name:
                return node
        raise ValueError("No node with name '" + name + "' found.")

    def get_initial_nodes(self):
        return set([node for node in self.nodes.values() if node.is_initial()])

    def get_edges(self):
        return self.edges

    def print(self):
        print("AF " + self.name)
        print(str(len(self.nodes)) + " nodes: " + ', '.join([node.name for node in self.nodes.values()]))
        print(str(len(self.edges)) + " edges: "
              + ', '.join([edge.node_from.name + '->' + edge.node_to.name for edge in self.edges]))
