import argparse
import sys
from nxfvars import __version__
from nxfvars.execute import nxfvars_execute


def main():
    parser = argparse.ArgumentParser("nxfvars")
    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="subcommand",
        required=True,
    )
    parser_version = subparsers.add_parser("version", help="Print the version and exit")
    parser_execute = subparsers.add_parser(
        "execute", help="Execute a jupyter/jupytext notebook and create a HTML report."
    )
    parser_execute.add_argument(
        "notebook",
        help="A jupyter notebook in any format compatible with jupytext.",
    )
    parser_execute.add_argument("report", help="Path to write the HTML report to.")
    parser_execute.add_argument(
        "-k",
        "--kernel_name",
        default="python3",
        help="The kernel used to execute the notebook. [Default: python3]",
        required=False,
    )
    args = parser.parse_args()

    if args.subcommand == "execute":
        nxfvars_execute(args.notebook, args.report, kernel_name=args.kernel_name)
    elif args.subcommand == "version":
        print(__version__)
        sys.exit(0)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
