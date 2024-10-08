import argparse
import t2tools


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="sub commands")
    parser_centel = subparsers.add_parser('centel', help='Identify centromeres and telomeres')
    parser_centel.add_argument("-f", "--fasta", help="fasta file or directory", required=True)
    parser_centel.add_argument("-p", "--split", help="split fasta or not, only for single fasta",
                               action="store_true")
    parser_centel.add_argument("-w", "--window_size", help="window size for splitting fasta, "
                                                           "must be integer or scientific notation, "
                                                           "like: 10000, 1e4")
    parser_centel.add_argument("-s", "--step_size", help="step size for splitting fasta, "
                                                         "must be integer or scientific notation, "
                                                         "like: 10000, 1e4")
    parser_centel.add_argument('--lower', help="lower size of centromere repeat monomer, "
                                               "default=50", type=int, default=50)
    parser_centel.add_argument('--upper', help="upper size of centromere repeat monomer, "
                                               "default=200", type=int, default=200)
    parser_centel.add_argument('--copy', help="minium copy number of centromere repeat monomer, "
                                              "default=10", type=int, default=10)
    parser_centel.add_argument('--score', help="minium score of centromere repeat monomer, "
                                               "default=2000", type=int, default=1000)
    parser_centel.add_argument("-o", "--output", help="output directory", required=True)
    parser_centel.add_argument("-t", "--threads", help="threads, default: 10", type=int, default=10)
    parser_centel.set_defaults(func=t2tools.workflow.centel_pipe.main)

    parser_gap_cnt = subparsers.add_parser('gapcount', help='Get gap counts')
    parser_gap_cnt.add_argument('-f', '--fasta', help="fasta file", required=True)
    parser_gap_cnt.add_argument('-o', '--output', help="output statistic, if not set, output to stdout")
    parser_gap_cnt.set_defaults(func=t2tools.workflow.gap_cnt_pipe.main)

    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.print_help()
