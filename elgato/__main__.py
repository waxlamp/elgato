"""Main module for elgato package."""

import argparse
import leglight
import sys
from typing import Optional


def first_light() -> leglight.LegLight:
    """Return the first light found in the network."""
    lights = []
    timeout = 0
    while not lights:
        timeout += 0.5
        lights = leglight.discover(timeout)
    return lights[0]


def turn_on(light: Optional[leglight.LegLight] = None) -> int:
    """Turn on the first light in the network."""
    if light is None:
        light = first_light()
    light.on()
    return 0


def turn_off(light: Optional[leglight.LegLight] = None) -> int:
    """Turn off the first light in the network."""
    if light is None:
        light = first_light()
    light.off()
    return 0


def toggle() -> int:
    """Toggle the first light in the network."""
    light = first_light()
    return turn_on(light) if light.isOn == 0 else turn_off(light)


def set_color(color: int) -> int:
    """Set the first light's color temperature."""
    light = first_light()
    return light.color(color)


def set_brightness(brightness: int) -> int:
    """Set the first light's brightness."""
    light = first_light()
    return light.brightness(brightness)


def main() -> int:
    """Run the elgato program."""

    # Parse command line arguments.
    #
    # The main parser just knows how to print help when no subcommand is given,
    # and delegates to subparsers otherwise.
    parser = argparse.ArgumentParser(prog="elgato")

    def print_help() -> int:
        parser.print_help()
        return 1

    parser.set_defaults(action=print_help)

    # Define a series of subcommand parsers.
    subparsers = parser.add_subparsers(help="subcommand help")

    parser_on = subparsers.add_parser("on", help="Turn a light on")
    parser_on.set_defaults(action=turn_on)

    parser_off = subparsers.add_parser("off", help="Turn a light off")
    parser_off.set_defaults(action=turn_off)

    parser_toggle = subparsers.add_parser("toggle", help="Toggle a light")
    parser_toggle.set_defaults(action=toggle)

    parser_color = subparsers.add_parser(
        "color", help="Set a light's color temperature"
    )
    parser_color.add_argument(
        "color",
        metavar="COLOR_TEMPERATURE",
        type=int,
        default=None,
        help="Color temperature in Kelvin (2900-7000)",
        choices=range(2900, 7001, 100),
    )
    parser_color.set_defaults(action=set_color)

    parser_brightness = subparsers.add_parser(
        "brightness", help="Set a light's brightness"
    )
    parser_brightness.add_argument(
        "brightness",
        metavar="BRIGHTNESS",
        type=int,
        default=None,
        help="Brightness level (1-100)",
        choices=range(1, 101),
    )
    parser_brightness.set_defaults(action=set_brightness)

    # Parse the command line arguments and dispatch to the correct subcommand.
    args = parser.parse_args(sys.argv[1:])
    action = args.action
    del args.action
    return action(**vars(args))


if __name__ == "__main__":
    sys.exit(main())
