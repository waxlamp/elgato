"""Main module for elgato package."""

import argparse
import sys


def turn_on() -> int:
    print("turn_on")
    return 0


def turn_off() -> int:
    print("turn_off")
    return 0


def main() -> int:
    """Run the elgato program."""

    # Parse command line arguments.
    #
    # The main parser just knows how to print help when no subcommand is given,
    # and delegates to subparsers otherwise.
    parser = argparse.ArgumentParser(prog="elgato")
    def print_help():
        parser.print_help()
        return 1
    parser.set_defaults(action=print_help)

    # Define a series of subcommand parsers.
    subparsers = parser.add_subparsers(help="subcommand help")

    # The parser for turning on a light.
    parser_on = subparsers.add_parser("on", help="Turn a light on")
    parser_on.set_defaults(action=turn_on)

    # The parser for turning off a light.
    parser_off = subparsers.add_parser("off", help="Turn a light off")
    parser_off.set_defaults(action=turn_off)

    # Parse the command line arguments and dispatch to the correct subcommand.
    args = parser.parse_args(sys.argv[1:])
    action = args.action
    del args.action
    return action(**vars(args))


if __name__ == "__main__":
    sys.exit(main())
