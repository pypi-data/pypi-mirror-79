from typing import NewType

import z3
import AF
from z3_instance import get_node_value

# label constants
Label = NewType("Label", str)
l_in = Label("in")
l_out = Label("out")
l_undec = Label("undec")


class LabelingScheme:

    num_args = 0  # The number of arguments each labeling scheme takes

    def get_label(self, argument: AF.Node, model: z3.ModelRef) -> Label:
        """
        Get the label of the given argument according the given model and the labeling approach.
        :return: l_in, l_out or l_undec
        """
        # implemented by subclasses
        pass

    def get_constraints(self, node: AF.Node):
        """
        Return a list of constraints on the probabilistic variable of the node where each constraint corresponds to a
        different label. I.e. for cautious labeling and node A, return [p_A == 1, p_A == 0, And(p_A < 1, p_A > 0)].
        Used to compute all labelings.
        """
        # implemented by subclasses
        return []


class Threshold(LabelingScheme):
    """
    Given two thresholds t_in and t_out, all nodes with probability
     - greater equal t_in are labeled 'in',
     - less than or equal to t_out are labeled 'out',
     - and between t_in and t_out are labeled 'undec'.
     """
    num_args = 2

    def __init__(self, t_in: float, t_out: float):
        self.t_in = t_in
        self.t_out = t_out

    def get_label(self, node: AF.Node, model):
        prob = get_node_value(node, model)
        if prob >= self.t_in:
            return l_in
        elif prob <= self.t_out:
            return l_out
        else:
            return l_undec

    def get_constraints(self, node: AF.Node):
        in_const = node.prob_var >= self.t_in
        out_const = node.prob_var <= self.t_out
        undec_const = z3.And(node.prob_var < self.t_in, node.prob_var > self.t_out)
        return [in_const, out_const, undec_const]


class Cautious(Threshold):
    """
    Arguments with probability 1 are labeled 'in', those with probability 0 are labeled 'out' and all others are
    labeled 'undec'.
    """
    num_args = 0

    def __init__(self):
        super().__init__(1.0, 0.0)


class Firm(LabelingScheme):
    """
    Arguments with probability 0.5 are labeled 'undec', those with probability >0.5 are labeled 'in' and all those with
    probability <0.5 are labeled 'out'.
    """
    def get_label(self, node: AF.Node, model):
        prob = get_node_value(node, model)
        if prob > 0.5:
            return l_in
        elif prob < 0.5:
            return l_out
        else:
            return l_undec

    def get_constraints(self, node: AF.Node):
        in_const = node.prob_var > 0.5
        out_const = node.prob_var < 0.5
        undec_const = node.prob_var == 0.5
        return [undec_const, in_const, out_const]
        # undec first because checking for equality is probably easier than inequalities


class ThresholdClassic(LabelingScheme):
    """
    Requires two thresholds t_in and t_min_attack_out. A node is labeled
     - 'in' if its probability is greater or equal t_in,
     - 'out' if it is not labeled 'in' and one of its attackers has probability greater or equal t_min_attack_out, and
     - 'undec' in all other cases.
     """
    num_args = 2

    def __init__(self, t_in: float, t_min_attack_out: float):
        self.t_in = t_in
        self.t_att_out = t_min_attack_out

    def get_label(self, node: AF.Node, model):
        node_prob = get_node_value(node, model)
        if node_prob >= self.t_in:
            return l_in
        else:
            label = l_undec
            for attacker in node.parents:
                attacker_prob = get_node_value(attacker, model)
                if attacker_prob >= self.t_att_out:
                    label = l_out
                    break
            return label

    def get_constraints(self, node: AF.Node):
        if self.t_in == self.t_att_out:
            in_const = node.prob_var >= self.t_in
            not_in_const = node.prob_var < self.t_in
            return [in_const, not_in_const]
        else:
            t_max = max(self.t_in, self.t_att_out)
            t_min = min(self.t_in, self.t_att_out)
            first_const = node.prob_var >= t_max
            second_const = node.prob_var < t_min
            third_const = z3.And(node.prob_var < t_max, node.prob_var >= t_min)
            return [first_const, second_const, third_const]


class Classic(ThresholdClassic):
    """
    A node is labeled
     - 'in' if it holds with probability 1,
     - 'out' if it is not labeled 'in' and one of its attackers holds with probability 1, and
     - 'undec' in all other cases.
    """
    num_args = 0

    def __init__(self):
        super().__init__(1.0, 1.0)


class Optimistic(LabelingScheme):
    """
    A node is labeled
     - 'in' if it holds with probability larger than 0, and
     - 'out' otherwise.
     """

    def get_label(self, node: AF.Node, model):
        prob = get_node_value(node, model)
        if prob > 0.0:
            return l_in
        else:
            return l_out

    def get_constraints(self, node: AF.Node):
        in_const = node.prob_var > 0
        out_const = node.prob_var == 0
        return [in_const, out_const]


class Pessimistic(LabelingScheme):
    """
    A node is labeled
     - 'in' if it holds with probability 1, and
     - 'out' otherwise.
     """

    def get_label(self, node: AF.Node, model):
        prob = get_node_value(node, model)
        if prob == 1.0:
            return l_in
        else:
            return l_out

    def get_constraints(self, node: AF.Node):
        in_const = node.prob_var == 1
        out_const = node.prob_var < 1
        return [in_const, out_const]


def get_labeling_scheme_class(name: str):
    """
    By dark magic, get the labeling scheme class given its name as string, e.g. "firm" to yield the class 'Firm'.

    :param name: the name of the labeling scheme class (case insensitive)
    :return: The labeling scheme class corresponding to the name, or None if no match was found
    """
    name = name.lower()
    queue = LabelingScheme.__subclasses__().copy()
    while queue:
        labeling_class = queue.pop()
        if name == labeling_class.__name__.lower():
            return labeling_class
        queue.extend(labeling_class.__subclasses__())
    return None


def get_all_labeling_scheme_names():
    """
    :return: A list of the names of all available labeling schemes
    """
    names = []
    queue = LabelingScheme.__subclasses__().copy()
    while queue:
        labeling_class = queue.pop()
        queue.extend(labeling_class.__subclasses__())
        names.append(labeling_class.__name__)
    return names
