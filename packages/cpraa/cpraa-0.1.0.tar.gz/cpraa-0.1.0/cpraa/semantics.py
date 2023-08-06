from typing import List

import z3
import AF
import z3_instance as zi


class Semantics:
    def __init__(self, z3i: zi.Z3Instance):
        self.context = z3i.context
        self.af = z3i.af
        self.z3_instance = z3i
        self.constraints: List[z3.BoolRef] = []

        self.generate_constraints()

    def generate_constraints(self):
        # implemented by subclasses
        pass

    def get_constraints(self):
        return self.constraints


####################
# trivial semantics
####################

class SemanticsMin(Semantics):
    """Minimality semantics: All nodes must hold with probability 0."""
    def generate_constraints(self):
        for node in self.af.get_nodes():
            self.constraints.append(node.prob_var == 0)


class SemanticsNeu(Semantics):
    """Neutrality semantics: All nodes must hold with probability 0.5."""
    def generate_constraints(self):
        for node in self.af.get_nodes():
            self.constraints.append(node.prob_var == 0.5)


class SemanticsMax(Semantics):
    """Maximality semantics: All nodes must hold with probability 1."""
    def generate_constraints(self):
        for node in self.af.get_nodes():
            self.constraints.append(node.prob_var == 1)


class SemanticsDirac(Semantics):
    """Dirac semantics: All nodes must hold with either probability 0 or 1."""
    def generate_constraints(self):
        for node in self.af.get_nodes():
            self.constraints.append(z3.Or(node.prob_var == 0, node.prob_var == 1))


class SemanticsTer(Semantics):
    """Ternary semantics: All nodes must hold with either probability 0, 0.5 or 1."""
    def generate_constraints(self):
        for node in self.af.get_nodes():
            self.constraints.append(z3.Or(node.prob_var == 0, node.prob_var == 0.5, node.prob_var == 1))


################################
# semantics by Hunter and Thimm
################################

class SemanticsFou(Semantics):
    """Foundedness semantics: Initial nodes must hold with probability 1."""
    def generate_constraints(self):
        for node in self.af.get_initial_nodes():
            self.constraints.append(node.prob_var == 1)


class SemanticsSFou(Semantics):
    """Semi-Foundedness semantics: Initial nodes must hold with probability >= 0.5."""
    def generate_constraints(self):
        for node in self.af.get_initial_nodes():
            self.constraints.append(node.prob_var >= 0.5)


class SemanticsInv(Semantics):
    """Involution semantics: p_A = 1 - p_B for all attacks A -> B."""
    def generate_constraints(self):
        for edge in self.af.get_edges():
            var_from = edge.node_from.prob_var
            var_to = edge.node_to.prob_var
            self.constraints.append(var_from == 1 - var_to)


class SemanticsRat(Semantics):
    """Rationality semantics: p_A >= 0.5 implies p_B <= 0.5 for all attacks A -> B."""
    def generate_constraints(self):
        for edge in self.af.get_edges():
            var_from = edge.node_from.prob_var
            var_to = edge.node_to.prob_var
            self.constraints.append(z3.Implies(var_from >= 0.5, var_to <= 0.5, ctx=self.context))


class SemanticsCoh(Semantics):
    """Coherency semantics: p_A <= 1 - p_B for all attacks A -> B."""
    def generate_constraints(self):
        for edge in self.af.get_edges():
            var_from = edge.node_from.prob_var
            var_to = edge.node_to.prob_var
            self.constraints.append(var_from <= 1 - var_to)


class SemanticsOpt(Semantics):
    """Optimism semantics: p_A >= 1 - Sum p_B for all attackers B of A."""
    def generate_constraints(self):
        for node in self.af.get_nodes():
            summation = 0
            for attacker in node.parents:
                summation += attacker.prob_var
            self.constraints.append(node.prob_var >= 1 - summation)


class SemanticsSOpt(Semantics):
    """Semi-optimism semantics: p_A >= 1 - Sum p_B for all attackers B of A iff A has at least one attacker."""
    def generate_constraints(self):
        for node in self.af.get_nodes():
            if node.is_initial():
                continue
            summation = 0
            for attacker in node.parents:
                summation += attacker.prob_var
            self.constraints.append(node.prob_var >= 1 - summation)


class SemanticsJus(Semantics):
    """Justifiability semantics: Coherency and optimism constraints hold."""
    def generate_constraints(self):
        cOpt = SemanticsOpt(self.z3_instance)
        cCoh = SemanticsCoh(self.z3_instance)
        self.constraints.extend(cOpt.get_constraints() + cCoh.get_constraints())


######################
# semantics by Baier
######################

class SemanticsCF(Semantics):
    """Conflict-freeness semantics: p_A_B = 0 for all attacks A -> B."""
    def generate_constraints(self):
        for edge in self.af.get_edges():
            assignment = [(edge.node_from, True), (edge.node_to, True)]
            prob_var = self.z3_instance.get_prob_var(assignment)
            self.constraints.append(prob_var == 0)


# Admissibility

def almost_sure_defense_constraint(z3i: zi.Z3Instance, node: AF.Node):
    """
    Generate a constraint for an argument A to be almost-surely defended.
    This means for all attackers B->A, the probability that B is in turn attacked (and thus A is defended) is 1.
    That is, P(C1 or C2 or ... Cn) = 1 for attackers C1...Cn of B, or, equivalently, P(nC1, nC2, ..., nCn) = 0.
    If an attacker B of A has no attackers, then A cannot be almost-surely defended, i.e. the impossible constraint is
    added.
    """
    constraint = z3.BoolVal(True, ctx=z3i.context)
    for attacker in node.parents:
        if attacker.parents:
            assignment = []
            for defender in attacker.parents:
                assignment.append((defender, False))
            prob_var = z3i.get_prob_var(assignment)
            constraint = z3.And(constraint, prob_var == 0)
        else:
            return z3.BoolVal(False, ctx=z3i.context)
    return constraint


class SemanticsWAdm(Semantics):
    """Weak admissibility semantics: p_A = 1 implies A is almost-surely defended."""
    def generate_constraints(self):
        for node in self.af.get_nodes():
            as_defense_constraint = almost_sure_defense_constraint(self.z3_instance, node)
            self.constraints.append(z3.Implies(node.prob_var == 1, as_defense_constraint, ctx=self.context))


class SemanticsPrAdm(Semantics):
    def generate_constraints(self):
        raise NotImplementedError


class SemanticsMinAdm(Semantics):
    def generate_constraints(self):
        raise NotImplementedError


class SemanticsJntAdm(Semantics):
    def generate_constraints(self):
        raise NotImplementedError


class SemanticsElmAdm(Semantics):
    def generate_constraints(self):
        raise NotImplementedError


# Completeness

class SemanticsWCmp(Semantics):
    """Weak completeness semantics: p_A = 1 if and only if A is almost-surely defended."""
    def generate_constraints(self):
        for node in self.af.get_nodes():
            as_defense_constraint = almost_sure_defense_constraint(self.z3_instance, node)
            self.constraints.append(z3.Implies(node.prob_var == 1, as_defense_constraint, ctx=self.context))
            self.constraints.append(z3.Implies(as_defense_constraint, node.prob_var == 1, ctx=self.context))


class SemanticsPrCmp(Semantics):
    def generate_constraints(self):
        raise NotImplementedError


class SemanticsMinCmp(Semantics):
    def generate_constraints(self):
        raise NotImplementedError


class SemanticsJntCmp(Semantics):
    def generate_constraints(self):
        raise NotImplementedError


class SemanticsElmCmp(Semantics):
    def generate_constraints(self):
        raise NotImplementedError


#####################
# semantics by Käfer
#####################

class SemanticsWNorS(Semantics):
    """
    Weak not-or semantics without CF: Generates constraints p_A <= p_nB1_nB2_..._nBi for every non-initial argument A
    with attackers B1, ..., Bi for some i > 0.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            if node.is_initial():
                continue  # for initial nodes, the constraint would be 'p_A <= 1' which already exists
            assignment = [(attacker, False) for attacker in node.parents]
            attacker_prob_var = self.z3_instance.get_prob_var(assignment)
            self.constraints.append(node.prob_var <= attacker_prob_var)


class SemanticsNorS(Semantics):
    """
    Not-or semantics without CF: Generates constraints p_A = p_nB1_nB2_..._nBi for every non-initial argument A with
    attackers B1, ..., Bi for some i > 0.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            if node.is_initial():
                continue
            assignment = [(attacker, False) for attacker in node.parents]
            attacker_prob_var = self.z3_instance.get_prob_var(assignment)
            self.constraints.append(node.prob_var == attacker_prob_var)


class SemanticsSNorS(Semantics):
    """
    Strong not-or semantics without CF. Generates constraints p_A = 1 for initial arguments and p_A = p_nB1_nB2_..._nBi
    for every non-initial argument A with attackers B1, ..., Bi for some i>0.
    Also the intersection of Nor and Fou.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            if node.is_initial():
                self.constraints.append(node.prob_var == 1)
            else:
                assignment = [(attacker, False) for attacker in node.parents]
                attacker_prob_var = self.z3_instance.get_prob_var(assignment)
                self.constraints.append(node.prob_var == attacker_prob_var)


class SemanticsWNor(Semantics):
    """
    Weak not-or semantics: Generates constraints for conflict-freeness and p_A <= p_nB1_nB2_..._nBi for every
    non-initial argument A with attackers B1, ..., Bi for some i > 0.
    """
    def generate_constraints(self):
        sCF = SemanticsCF(self.z3_instance)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            if node.is_initial():
                continue  # for initial nodes, the constraint would be 'p_A <= 1' which already exists
            assignment = [(attacker, False) for attacker in node.parents]
            attacker_prob_var = self.z3_instance.get_prob_var(assignment)
            self.constraints.append(node.prob_var <= attacker_prob_var)


class SemanticsNor(Semantics):
    """
    Not-or semantics: Generates constraints for conflict-freeness and p_A = p_nB1_nB2_..._nBi for every non-initial
    argument A with attackers B1, ..., Bi for some i > 0.
    """
    def generate_constraints(self):
        sCF = SemanticsCF(self.z3_instance)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            if node.is_initial():
                continue
            assignment = [(attacker, False) for attacker in node.parents]
            attacker_prob_var = self.z3_instance.get_prob_var(assignment)
            self.constraints.append(node.prob_var == attacker_prob_var)


class SemanticsSNor(Semantics):
    """
    Strong not-or semantics: Generates constraints for conflict-freeness, p_A = 1 for initial arguments and
    p_A = p_nB1_nB2_..._nBi for every non-initial argument A with attackers B1, ..., Bi for some i>0.
    Also the intersection of Nor and Fou and CF.
    """
    def generate_constraints(self):
        sCF = SemanticsCF(self.z3_instance)
        self.constraints.extend(sCF.constraints)
        for node in self.af.get_nodes():
            if node.is_initial():
                self.constraints.append(node.prob_var == 1)
            else:
                assignment = [(attacker, False) for attacker in node.parents]
                attacker_prob_var = self.z3_instance.get_prob_var(assignment)
                self.constraints.append(node.prob_var == attacker_prob_var)


class SemanticsAF(Semantics):
    """
    Special semantics to add constraints for probability values or intervals specified in the AF input file.
    """
    def generate_constraints(self):
        for node in self.af.get_nodes():
            if node.value is not None:
                assert node.interval is None, "node with both value and interval set"
                self.constraints.append(node.prob_var == node.value)
            elif node.interval is not None:
                low, high = node.interval
                self.constraints.append(node.prob_var >= low)
                self.constraints.append(node.prob_var <= high)


class SemanticsNNor(Semantics):
    """
    Noisy not-or semantics:  TODO
    per default without prior probabilities
    p_A_nB_nC = 1 * p_nB_nC
    p_A_nB_C  = (1 - t) * p_nB_C
    p_A_B_nC  = (1 - s) * p_B_nC
    p_A_B_C   = (1 - s ) * (1 - t) * p_B_C
    """
    def __init__(self, z3i: zi.Z3Instance, use_prior_probs=False):
        self.use_prior_probs = use_prior_probs
        super().__init__(z3i)

    def generate_constraints(self):
        # we use attack strength, so a prob_var should be created for each edge
        self.z3_instance.generate_edge_vars()

        for node in self.af.get_nodes():

            node_prior_prob_var = self.z3_instance.create_real_var("pr_" + node.name)  # e.g. pr_A
            if self.use_prior_probs:
                if node.value is not None:
                    self.constraints.append(node_prior_prob_var == node.value)
                elif node.interval is not None:
                    i_min, i_max = node.interval
                    self.constraints.append(z3.And(node_prior_prob_var >= i_min, node_prior_prob_var <= i_max))
                else:
                    self.constraints.append(z3.And(node_prior_prob_var >= 0, node_prior_prob_var <= 1))
            else:
                self.constraints.append(node_prior_prob_var == 1)

            if node.is_initial():
                self.constraints.append(node.prob_var == node_prior_prob_var)
                continue

            for parent_assignment in zi.assignments(node.parents):
                parent_prob_var = self.z3_instance.get_prob_var(parent_assignment)  # e.g. p_nB_C
                prob_var = self.z3_instance.get_prob_var(parent_assignment + [(node, True)])  # e.g. p_A_nB_C

                product = node_prior_prob_var * parent_prob_var
                for (parent, status) in parent_assignment:
                    if status:
                        edge: AF.Edge = node.get_parent_edge(parent)
                        product *= (1 - edge.prob_var)
                self.constraints.append(prob_var == product)


class SemanticsNNorAF(SemanticsNNor):
    """
    Noisy not-or semantics:  TODO
    with prior probabilities
    p_A_nB_nC = prA * p_nB_nC
    p_A_nB_C  = prA * (1 - t) * p_nB_C
    p_A_B_nC  = prA * (1 - s) * p_B_nC
    p_A_B_C   = prA * (1 - s ) * (1 - t) * p_B_C
    """
    def __init__(self, z3i: zi.Z3Instance):
        super().__init__(z3i, use_prior_probs=True)


class SemanticsCFs(Semantics):
    """Conflict-freeness semantics with attack strengths: p_A_B <= 1-s for all attacks A -s-> B."""
    def generate_constraints(self):
        # we use attack strength, so a prob_var should be created for each edge
        self.z3_instance.generate_edge_vars()

        for edge in self.af.get_edges():
            assignment = [(edge.node_from, True), (edge.node_to, True)]
            prob_var = self.z3_instance.get_prob_var(assignment)
            self.constraints.append(prob_var <= 1 - edge.prob_var)


###################
# Helper functions
###################

def get_semantics_class_by_name(name: str):
    """
    By dark magic, get the semantics class given its name as string, e.g. "wNor" to yield the class 'SemanticsWNor'.

    :param name: the short name of the semantics (case insensitive)
    :return: The semantics class corresponding to the name
    """
    name = "semantics" + name.lower()
    queue = Semantics.__subclasses__().copy()
    while queue:
        semantics_class = queue.pop()
        if name == semantics_class.__name__.lower():
            return semantics_class
        queue.extend(semantics_class.__subclasses__())
    print("Error: No semantics called 'name' was found.")
    return None


def all_semantics_short_names():
    """
    :return: A list of the short names of all semantics declared in this file
    """
    names = []
    queue = Semantics.__subclasses__().copy()
    while queue:
        semantics_class = queue.pop()
        queue.extend(semantics_class.__subclasses__())
        name = semantics_class.__name__
        if name[0:9] == "Semantics":
            name = name[9:]  # strip away leading 'Semantics'
        names.append(name)
    return names
