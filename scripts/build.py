import argparse
import sys

from logger import log
from sphinx.cmd.build import main as build_main


def build_doc(config):
    """Build Sphinx documentation."""
    build_main(["-b", "html", "doc/source", "./_build/html", "--color", "-vW"])


def get_build_steps():
    return {"build_doc": build_doc}


def get_arg_parser():
    parser = argparse.ArgumentParser(
        description="Build project",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "command",
        nargs="+",
        choices=get_build_steps().keys(),
        help="Operation to perform",
    )

    return parser


def main(args):
    log.info(f"Using python at: {sys.executable}")

    config = {}
    for build_step in args.command:
        command_func = get_build_steps().get(build_step)

        log.info(f"Running: {args.command}")
        command_func(config)
        log.info(f"{build_step.capitalize()} done!")


if __name__ == "__main__":
    parser = get_arg_parser()
    main(parser.parse_args())
