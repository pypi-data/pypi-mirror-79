from typing import Dict, List, Tuple, Any

import AF
import z3


class Z3Instance:
    """Class to bundle the declared probabilistic variables, the underlying full joint distribution."""

    def __init__(self, af: AF.AF):
        self.af = af
        self.context = z3.Context()
        self.solver = z3.Solver(ctx=self.context)
        self.full_joint_prob_vars: Dict[str, z3.ArithRef] = dict()
        self.other_prob_vars: Dict[str, z3.ArithRef] = dict()
        self.real_vars: Dict[str, z3.ArithRef] = dict()
        self.constraints = set()
        self.af_constraints = set()

        self._generate_full_prob_vars()

        # Add a prob_var for each node in the AF
        for node in self.af.get_nodes():
            node.prob_var = self.get_prob_var([(node, True)])
            # if node.value is not None:
            #     self.af_constraints.add(node.prob_var == node.value)
            #     assert node.interval is None, "both node.value and node.interval where given"
            # elif node.interval is not None:
            #     (val_min, val_max) = node.interval
            #     self.af_constraints.add(z3.And(node.prob_var >= val_min, node.prob_var <= val_max))

    def generate_edge_vars(self):
        """
        Generates a probabilistic variable for each edge. If an edge has a value or interval given, those are added as
        constraints to af_constraints.
        """
        for edge in self.af.get_edges():
            if edge.prob_var is not None:
                # There might be several calls to generate_edge_vars, but we want to add the constraints only once.
                continue
            edge.prob_var = z3.Real(edge.label, self.context)

            if edge.value is not None:
                self.af_constraints.add(edge.prob_var == edge.value)
                assert edge.interval is None, "both edge.value and edge.interval where given"
            elif edge.interval is not None:
                (val_min, val_max) = edge.interval
                self.af_constraints.add(z3.And(edge.prob_var >= val_min, edge.prob_var <= val_max))
            else:
                self.af_constraints.add(edge.prob_var >= 0)
                self.af_constraints.add(edge.prob_var <= 1)

    def _generate_full_prob_vars(self):
        """Adds variables for the full joint distribution to the context. Adds the constraint that they sum to one."""
        constraint = 0
        for assignment in assignments(self.af.get_nodes()):
            assignment_prob_name = prob_name(assignment)

            prob_var = z3.Real(assignment_prob_name, self.context)
            self.full_joint_prob_vars[assignment_prob_name] = prob_var
            self.constraints.add(prob_var >= 0)
            self.constraints.add(prob_var <= 1)
            constraint += prob_var

        constraint = 1 == constraint
        self.constraints.add(constraint)

    def get_prob_var(self, assignment: List[AF.Tuple[AF.Node, bool]]):
        """
        Get the probabilistic variable corresponding to a full or partial assignment.
        If it does not exist yet, it is created along with the constraints 'new_var >= 0', 'new_var <= 1' and the
        representation of new_var as sum of the full joint variables.
        """
        assert assignment, "empty assignment given"
        prob_var_name = prob_name(assignment)
        if prob_var_name in self.other_prob_vars:
            prob_var = self.other_prob_vars[prob_var_name]
        else:
            prob_var = z3.Real(prob_var_name, self.context)
            self.other_prob_vars[prob_var_name] = prob_var
            self.constraints.add(prob_var >= 0)
            self.constraints.add(prob_var <= 1)
            self.constraints.add(self.sum_out(assignment, prob_var))
        return prob_var

    def create_real_var(self, name: str):
        """
        Creates and returns an auxiliary z3 real variable.
        """
        if name in self.real_vars:
            raise ValueError("A real var with name '" + name + "' already exists.")
        real_var = z3.Real(name, self.context)
        self.real_vars[name] = real_var
        return real_var

    def sum_out(self, part_assignment: List[AF.Tuple[AF.Node, bool]], part_assignment_prob_var):
        """[(A,True),(B,False)], [A,B,C] -> p_A_nB = p_A_nB_C + p_A_nB_nC"""
        part_assignment_args = [arg for (arg, _) in part_assignment]
        remaining_args = [arg for arg in self.af.get_nodes() if arg not in part_assignment_args]
        summation = 0
        for assignment in assignments(remaining_args):

            full_assignment = part_assignment + assignment
            full_assignment_name = prob_name(full_assignment)
            prob_var = self.full_joint_prob_vars[full_assignment_name]
            summation += prob_var
        constraint = part_assignment_prob_var == summation
        return constraint
    
    def add_constraints(self, constraints):
        for cons in constraints:
            self.constraints.add(cons)

    def run(self, prob_constraints):
        """
        TODO

        :param prob_constraints: a list of constraints
        :return: A z3 CheckSatResult, i.e. sat, unsat or unknown
        """
        self.solver.reset()
        self.solver.add(self.constraints)
        # print("self.constraints:", self.constraints)
        self.solver.add(self.af_constraints)
        # print("self.af_constraints", self.af_constraints)
        self.solver.add(prob_constraints)
        # print("prob_constraints", prob_constraints)

        result = self.solver.check()
        # print(result)
        # if result == z3.sat:
        #     model = self.solver.model()
        #     print(model)
        #     for node in self.af.get_nodes():
        #         prob = model.eval(node.prob_var)
        #         print(node.name, prob)
        return result

    def print_distribution(self, model: z3.ModelRef, nodes=None, only_positive=False):
        """
        Print distribution given by the model over the assignments of the given nodes.
        If no list of nodes is given, the distributions over all nodes in the AF is given.
        """
        if not nodes:
            nodes = self.af.get_nodes()
        node_assignments = assignments(nodes)
        for assignment in node_assignments:
            prob_var = self.get_prob_var(assignment)
            value = get_prob_var_value(prob_var, model)
            if not only_positive or value > 0:
                print(prob_var, "=", value)


def prob_name(argument_combo: List[AF.Tuple[AF.Node, bool]]) -> str:
    """
    Expects a list of tuples of nodes matched to True or False, i.e. [(node_B, False), (node_C, True)].
    Generates a name for the probability of the conjunction of the nodes, i.e. 'p_nB_C'.
    The order is determined by node IDs.
    """
    name = "p"
    argument_combo.sort()
    for (arg, b) in argument_combo:
        name += "_"
        if not b:
            name += "n"
        name += arg.name
    return name


def assignments(ar: list, br: list = None) -> List[List[Tuple[Any, Any]]]:
    """Generates all possible assignments of the elements in list 'ar' to elements of list 'br'.
     E.g. ar = [x,y], br = [0,1] -> [[(x,0),(y,0)],[(x,0),(y,1)],[(x,1),(y,0)],[(x,1),(y,1)]]"""
    if br is None:
        br = [False, True]
    combinations = [[]]

    for a in ar:
        next_combinations = []
        for c in combinations:
            for b in br:
                new_c = c.copy()
                new_c.append((a, b))
                next_combinations.append(new_c)
        combinations = next_combinations
    return combinations


def get_prob_var_value(prob_var, model: z3.ModelRef):
    """
    Get the value assigned to a probabilistic variable by the given model.
    :return: The value as float
    """
    # Based on https://stackoverflow.com/a/12600208/6620204
    value = model.eval(prob_var)
    if z3.is_int_value(value):
        return value.as_long()
    elif z3.is_rational_value(value):
        return float(value.numerator_as_long())/float(value.denominator_as_long())
    elif z3.is_algebraic_value(value):
        approx_value = value.approx(20)
        return float(approx_value.numerator_as_long())/float(approx_value.denominator_as_long())
    else:
        raise ValueError("Unable to convert to float: " + str(value))


def print_model(af: AF.AF, model: z3.ModelRef):
    for node in af.get_nodes():
        print(node.name, "=", get_node_value(node, model))


def get_node_value(node: AF.Node, model: z3.ModelRef):
    """
    Get the value assigned to a node's probabilistic variable by the given model.
    :return: The value as float
    """
    return get_prob_var_value(node.prob_var, model)
