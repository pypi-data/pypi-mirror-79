import AF


def parse_interval(string, obj):
    """Parse a value or an interval and add it to either the node or edge passed as obj.
    '0.2:0.8' -> add interval (0.2, 0.8)
    '0.5' -> add value 0.5
    'ABC' -> print warning, add nothing"""

    split = string.split(':')

    p1 = float(split[0])
    if len(split) == 1:
        obj.add_value(p1)
    elif len(split) == 2:
        p2 = float(split[1])
        obj.add_interval((p1, p2))
    else:
        print("Warning: Ill-formed probability '" + string + "'")


def parse_tgf(path):
    """Parse a file in trivial graph format. Return an AF object."""
    with open(path, "r") as file:
        tgf_file = file.read()

    af = AF.AF(path)

    # remove blank lines and line comments (starting with ';')
    lines = tgf_file.split('\n')
    node_declarations = []
    edge_declarations = []
    start_edges = False
    for line in lines:

        split = line.split(";")
        if split[0].strip() == "#":
            start_edges = True
            continue
        if split[0].strip() != "":
            if start_edges:
                edge_declarations.append(split[0])
            else:
                node_declarations.append(split[0])

    # parse nodes and edges
    for d in node_declarations:
        # format: <node_id> [<node_name>] [<node_prob>|<node_prob_min>:<node_prob_max>]
        # if d.strip() == "":
        #     continue
        tokens = [token for token in d.split(' ') if token.strip()]
        node_id = tokens[0]
        node = AF.Node(node_id)

        if len(tokens) > 1:
            next_token = tokens[1]
            if next_token[0].isalpha():  # <node_name> is given
                node.name = next_token
                if len(tokens) > 2:
                    next_token = tokens[2]
                else:
                    next_token = None
            if next_token:
                parse_interval(next_token, node)
        af.add_node(node)

    for d in edge_declarations:
        # if d.strip() == "":
        #     continue

        tokens = [token for token in d.split(' ') if token.strip()]
        node_from_id = tokens[0]
        node_from = af.get_node(node_from_id)
        node_to_id = tokens[1]
        node_to = af.get_node(node_to_id)
        edge = AF.Edge(node_from, node_to)
        if len(tokens) > 2:
            next_token = tokens[2]
            if next_token[0].isalpha():
                edge.label = next_token
                if len(tokens) > 3:
                    next_token = tokens[3]
                else:
                    next_token = None
            if next_token:
                parse_interval(next_token, edge)
        af.add_edge(edge)

    af.print()
    return af
