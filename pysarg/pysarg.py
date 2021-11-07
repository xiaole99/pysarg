import sys
from argparse import ArgumentParser
import subprocess

from .stage_one import stage_one
from .stage_two import stage_two

def parse_options(argv):

    parser = ArgumentParser(prog='pysarg')
    subparsers = parser.add_subparsers(help='Running modes', metavar='{stage_one, stage_two}')

    ## stage_one parameters
    parser_stage_one = subparsers.add_parser('stage_one', help='run stage_one')
    mandatory_one = parser_stage_one.add_argument_group('MANDATORY')
    mandatory_one.add_argument('-i','--indir', help='input files directory', metavar='DIR', required=True)
    mandatory_one.add_argument('-o','--outdir', help='output files directory', metavar='DIR', required=True)

    optional_one = parser_stage_one.add_argument_group('OPTIONAL')
    optional_one.add_argument('-x', '--e_cutoff', help='evalue cutoff, default 3', default=3)
    optional_one.add_argument('-y', '--id_cutoff', help='identity cutoff, default 0.45', default=0.45)

    parser_stage_one.set_defaults(func=stage_one)

    ## stage_one parameters
    parser_stage_two = subparsers.add_parser('stage_two', help='run stage_two')
    mandatory_two = parser_stage_two.add_argument_group('MANDATORY')
    mandatory_two.add_argument('-i','--infile', help='stage_one extracted file', metavar='FILE', required=True)
    mandatory_two.add_argument('-o','--outdir', help='output files directory', metavar='DIR', required=True)
    mandatory_two.add_argument('-m','--metafile', help='stage_one meta file', metavar='FILE', required=True)

    optional_two = parser_stage_two.add_argument_group('OPTIONAL')
    optional_two.add_argument('-x', '--e_cutoff', help='evalue cutoff, default 1e-7', default=1e-7)
    optional_two.add_argument('-y', '--id_cutoff', help='identity cutoff, default 80', default=80)
    optional_two.add_argument('-z', '--len_cutoff', help='length cutoff, default 25', default=25)

    parser_stage_two.set_defaults(func=stage_two)

    if len(argv) < 2:
        parser.print_help()
        sys.exit(1)

    if len(argv) < 3:
        if argv[1] == 'stage_one':
            parser_stage_one.print_help()
        elif argv[1] == 'stage_two':
            parser_stage_two.print_help()
        else:
            parser.print_help()
        sys.exit(1)

    return(parser.parse_args(argv[1:]))

def main(argv=sys.argv):

    options = parse_options(argv)
    options.func(options)

if __name__ == "__main__":
    main(sys.argv)
