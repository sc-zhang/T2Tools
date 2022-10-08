#!/usr/bin/env python3
import argparse
import t2tools


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="sub commands")
    parser_centrotelo = subparsers.add_parser('centrotelo', help='Identify centromeres and telomeres')
    parser_centrotelo.add_argument("-f", "--fasta", help="fasta file or directory", required=True)
    parser_centrotelo.add_argument("-p", "--split", help="split fasta or not, only for single fasta",
                                   action="store_true")
    parser_centrotelo.add_argument("-w", "--window_size", help="window size for splitting fasta, must be integer or "
                                                               "scientific notation, like: 10000, 1e4")
    parser_centrotelo.add_argument("-s", "--step_size", help="step size for splitting fasta, must be integer or "
                                                             "scientific notation, like: 10000, 1e4")
    parser_centrotelo.add_argument("-o", "--output", help="output directory", required=True)
    parser_centrotelo.add_argument("-t", "--threads", help="threads, default: 10", type=int, default=10)
    parser_centrotelo.set_defaults(func=t2tools.centrotelo.pipeline.main)

    try:
        args = parser.parse_args()
        args.func(args)
    except AttributeError:
        parser.print_help()


if __name__ == "__main__":
    main()
