import argparse
import importlib
import sys
from pathlib import Path
from signal import SIG_DFL, SIGPIPE, signal
from typing import List

from flupy import __version__, flu


def read_file(filename):
    with open(filename, "r") as f:
        yield from f


def parse_args(args: List[str]):
    """Parse input arguments"""
    parser = argparse.ArgumentParser(
        description="flupy: a fluent interface for python collections", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-v", "--version", action="version", version="%(prog)s " + __version__)
    parser.add_argument("command", help="command to execute against input")
    parser.add_argument("-f", "--file", help="path to input file")
    parser.add_argument(
        "-i",
        "--import",
        nargs="*",
        default=[],
        help="modules to import\n"
        "Syntax: <module>:<object>:<alias>\n"
        "Examples:\n"
        "\t'import os' = '-i os'\n"
        "\t'import os as op_sys' = '-i os::op_sys'\n"
        "\t'from os import environ' = '-i os:environ'\n"
        "\t'from os import environ as env' = '-i os:environ:env'\n",
    )
    return parser.parse_args(args)


def execute_imports(imps: List[str]):
    """Execute CLI scoped imports"""
    for imp_stx in imps:
        module, _, obj_alias = imp_stx.partition(":")
        obj, _, alias = obj_alias.partition(":")
        if not obj:
            globals()[alias or module] = importlib.import_module(module)
        else:
            _garb = importlib.import_module(module)
            globals()[alias or obj] = getattr(_garb, obj)


def main():
    """CLI Entrypoint"""
    args = parse_args(sys.argv[1:])

    _command = args.command
    _file = args.file
    _import = getattr(args, "import")

    execute_imports(_import)

    if _file:
        _ = flu(read_file(_file)).map(str.rstrip)
    else:
        # Do not raise exception for Broken Pipe
        signal(SIGPIPE, SIG_DFL)
        _ = flu(sys.stdin).map(str.rstrip)

    pipeline = eval(_command)

    if hasattr(pipeline, "__iter__") and not isinstance(pipeline, (str, bytes)):
        for r in pipeline:
            sys.stdout.write(str(r) + "\n")

    elif pipeline is None:
        pass
    else:
        sys.stdout.write(str(pipeline) + "\n")


def precommit():
    """Secondary entrypoing for pre-commit hook to handle multiple files
    as positional arguments

    For internal use only
    """

    def precommit_parse_args(args: List[str]):
        parser = argparse.ArgumentParser(
            description="flupy: a fluent interface for python", formatter_class=argparse.RawTextHelpFormatter
        )
        parser.add_argument("files", type=str, nargs="+", help="file pathes")
        parser.add_argument("--command", help="command to execute against input")
        parser.add_argument("-i", "--import", nargs="*", default=[])
        return parser.parse_args(args)

    args = precommit_parse_args(sys.argv[1:])

    # Pull command from
    _command = args.command
    _files = args.files
    _import = getattr(args, "import")

    execute_imports(_import)

    if _files:

        _ = flu(_files).map(Path).filter(lambda x: x.is_file())
    else:
        # Do not raise exception for Broken Pipe
        signal(SIGPIPE, SIG_DFL)
        _ = flu(sys.stdin).map(str.rstrip)

    pipeline = eval(_command)

    if hasattr(pipeline, "__iter__") and not isinstance(pipeline, (str, bytes)):
        for r in pipeline:
            sys.stdout.write(str(r) + "\n")

    elif pipeline is None:
        pass
    else:
        sys.stdout.write(str(pipeline) + "\n")
