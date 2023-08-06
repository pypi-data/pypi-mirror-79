import argparse

import af_parser
import semantics as sem
import labeling_scheme as lab
import tasks
import z3_instance

# TODO:
#  - Flag for extensions
#  - flag to generate unsat core; this needs named assertions, see assert_and_track() in z3.py
#  - check why seemingly the same labeling still can appear multiple times for AL
#  - af_constrainst in z3i overlaps with AF semantics


def main():
    #########################
    # set up argument parser
    #########################
    arg_parser = argparse.ArgumentParser(description="CPrAA - a Checker for Probabilistic Abstract Argumentation ",
                                         add_help=False)
    base_group = arg_parser.add_argument_group("basic parameters")
    base_group.add_argument("-f", "--file", help="the argumentation framework as .tgf file")
    base_group.add_argument("-s", "--semantics", nargs="+", default=[],
                            help="the probabilistic semantics to check against")

    ac_group = arg_parser.add_argument_group("acceptance checking")
    ac_group.add_argument("-a", "--argument", help="the argument from the AF to be checked")
    ac_group.add_argument("-CA", "--credulous_acceptance",
                          nargs="?", metavar="THRESHOLD", type=float, const=1.0,
                          help="check credulous acceptance of given argument, "
                               "optionally taking a threshold into account")
    ac_group.add_argument("-SA", "--skeptical_acceptance",
                          nargs="?", metavar="THRESHOLD", type=float, const=1.0,
                          help="check skeptical acceptance of given argument, "
                               "optionally taking a threshold into account")

    lab_group = arg_parser.add_argument_group("generate labelings")
    lab_group.add_argument("-l", "--labeling_scheme", metavar="SCHEME", help="the labeling scheme to use")
    lab_group.add_argument("-OL", "--one_labeling", action="store_true",
                           help="compute one labeling satisfying the semantics")
    lab_group.add_argument("-AL", "--all_labelings", action="store_true",
                           help="compute all labelings satisfying the semantics")
    lab_group.add_argument("-lt", "--labeling_threshold", nargs="+", metavar="T", type=float,
                           help="the optional thresholds needed for some labeling schemes")

    info_group = arg_parser.add_argument_group('informational parameters')
    info_group.add_argument("-h", "--help", action="help", help="show this help message")
    info_group.add_argument("-ls", "--list_semantics", action="store_true", help="list all available semantics")
    info_group.add_argument("-ll", "--list_labeling_schemes", action="store_true",
                            help="list all available labeling schemes")

    ##################
    # parse arguments
    ##################
    args = arg_parser.parse_args()

    af = None
    z3i = None
    labeling_scheme = None
    semantics = []
    argument = None

    if args.list_semantics:
        print("Available semantics:", ", ".join(sem.all_semantics_short_names()))

    if args.list_labeling_schemes:
        print("Available labeling schemes:", ", ".join(lab.get_all_labeling_scheme_names()))

    if args.file:
        af = af_parser.parse_tgf(args.file)
        z3i = z3_instance.Z3Instance(af)

    if args.semantics:
        if not af:
            arg_parser.error("an AF must be provided when checking semantics")

        for semantics_name in args.semantics:
            semantics_class = sem.get_semantics_class_by_name(semantics_name)
            semantics.append(semantics_class(z3i))

    if args.labeling_scheme:
        labeling_scheme_class = lab.get_labeling_scheme_class(args.labeling_scheme)
        if not labeling_scheme_class:
            arg_parser.error("no labeling scheme called '" + args.labeling_scheme + "' exists")
        num_args_required = labeling_scheme_class.num_args
        if args.labeling_threshold:
            num_args_given = len(args.labeling_threshold)
        else:
            num_args_given = 0
        if num_args_given < num_args_required:
            error_message = "mismatch in the number of thresholds: required by labeling scheme '" \
                            + args.labeling_scheme + "': " + str(num_args_required) + ", given: " + str(num_args_given)
            arg_parser.error(error_message)
        if num_args_given > num_args_required:
            warning_message = "warning: mismatch in the number of thresholds: required by labeling scheme '" \
                              + args.labeling_scheme + "': " + str(num_args_required) + ", given: " \
                              + str(num_args_given) + " - i'm ignoring the surplus ones"
            print(warning_message)
        if num_args_required == 0:
            labeling_scheme = labeling_scheme_class()
        elif num_args_required == 1:
            labeling_scheme = labeling_scheme_class(args.labeling_threshold[0])
        elif num_args_required == 2:
            labeling_scheme = labeling_scheme_class(args.labeling_threshold[0], args.labeling_threshold[1])
        else:
            raise NotImplementedError("labeling schemes with more than 2 thresholds")

    if args.argument:
        if not af:
            arg_parser.error("an AF must be provided when checking acceptance")
        argument = af.get_node_by_name(args.argument)

    ########
    # tasks
    ########

    # TODO: credulous and skeptical acceptance wrt. a labeling scheme

    if args.one_labeling:
        if not af:
            arg_parser.error("an AF must be provided to compute a labeling")
        if not labeling_scheme:
            arg_parser.error("no labeling provided")

        print("Computing one", args.labeling_scheme, "labeling satisfying the following semantics:",
              ", ".join(args.semantics))
        labeling = tasks.get_satisfying_labeling(z3i, labeling_scheme, semantics)
        print(labeling)

    if args.all_labelings:
        if not af:
            arg_parser.error("an AF must be provided to compute a labeling")
        if not labeling_scheme:
            arg_parser.error("no labeling provided")

        print("Computing all", args.labeling_scheme, "labelings satisfying the following semantics:",
              ", ".join(args.semantics))
        labelings = tasks.get_all_satisfying_labelings(z3i, labeling_scheme, semantics)

        for labeling in labelings:
            print(labeling)
            # print(labeling.model)
            # z3i.print_distribution(labeling.model, only_positive=True)
            z3_instance.print_model(af, labeling.model)
        # for labeling in sorted(list(set(map(repr, labelings)))):
        #     print(labeling)

    if args.credulous_acceptance is not None:
        if not af:
            arg_parser.error("an AF must be provided to check acceptance")
        if not argument:
            arg_parser.error("argument to be checked is missing")

        threshold = args.credulous_acceptance

        print("Checking credulous acceptance of argument", args.argument, "with threshold", threshold,
              "under the following semantics:", ", ".join(args.semantics))
        (acceptable, model) = tasks.check_credulous_threshold_acceptance(z3i, semantics, threshold, argument)
        if acceptable:
            print(args.argument, "is credulously accepted.")
            print("Satisfying distribution:")
            z3i.print_distribution(model, only_positive=True)
            z3_instance.print_model(af, model)
        else:
            print(args.argument, "is not credulously accepted.")

    if args.skeptical_acceptance is not None:
        if not af:
            arg_parser.error("an AF must be provided to check acceptance")
        if not argument:
            arg_parser.error("argument to be checked is missing")

        threshold = args.skeptical_acceptance

        print("Checking skeptical acceptance of argument", args.argument, "with threshold", threshold,
              "under the following semantics:", ", ".join(args.semantics))
        (acceptable, counterexample) = tasks.check_skeptical_threshold_acceptance(z3i, semantics, threshold, argument)
        if acceptable:
            print(args.argument, "is skeptically accepted.")
        else:
            print(args.argument, "is not skeptically accepted.")
            print("Counterexample:", counterexample)
            z3i.print_distribution(counterexample, only_positive=True)
            z3_instance.print_model(af, counterexample)


main()

# ---------------------------------------------------------


def test_all_semantics():
    # path = "AFs/af01.tgf"
    path = "AFs/af_references_noisy.tgf"
    af = af_parser.parse_tgf(path)
    z3i = z3_instance.Z3Instance(af)

    for semantics_class in tasks.Semantics.__subclasses__():
        try:
            semantics = semantics_class(z3i)
            print(semantics_class.__name__, semantics.constraints)
        except NotImplementedError:
            print(semantics_class.__name__, "(not implemented)")


# test_all_semantics()
