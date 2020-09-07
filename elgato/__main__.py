"""Main module for elgato package."""

import argparse
import json
import leglight
import os
import sys
from typing import List, Literal, Optional, TypedDict

LightInfo = TypedDict(
    "LightInfo",
    {
        "name": str,
        "power": Literal["off", "on"],
        "brightness": int,
        "color": int,
        "address": str,
        "port": int,
    },
)


class Discovered:
    """Active record class for retrieving/saving light list."""

    path: str
    data: List[LightInfo]

    def __init__(self, path: str) -> None:
        """Initialize with a path to a JSON file."""
        self.path = path
        with open(path) as f:
            self.data = json.loads(f.read())

    def save(self) -> None:
        """Save the current data to the file this instance was opened from."""
        with open(self.path, "w") as f:
            f.write(json.dumps(self.data))


Settings = TypedDict(
    "Settings",
    {
        "config_dir": str,
        "discovered_file": str,
        "discovered": Discovered,
    },
)


def get_settings() -> Settings:
    """Return the current settings."""
    config_dir = os.getenv("ELGATO_CONFIG_DIR", os.path.expanduser("~/.config/elgato"))
    discovered_file = os.path.join(config_dir, "discovered.json")

    # Ensure config directory exists.
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)

    # Ensure discovered lights file exists.
    if not os.path.exists(discovered_file):
        with open(discovered_file, "w") as f:
            f.write("[]")

    discovered = Discovered(discovered_file)

    return {
        "config_dir": config_dir,
        "discovered_file": discovered_file,
        "discovered": discovered,
    }


settings = get_settings()


def light_info(light: leglight.LegLight) -> LightInfo:
    """Map a leglight light object to a dict of printable values."""
    return {
        "name": f"{light.productName} {light.serialNumber}",
        "power": "off" if light.isOn == 0 else "on",
        "brightness": light.isBrightness,
        "color": int(light.isTemperature),
        "address": light.address,
        "port": light.port,
    }


def print_light_info(light: LightInfo) -> None:
    """Print an instance of a LightInfo to stdout."""
    spacing = max(len(key) for key in light.keys())
    for key in light:
        print(f"    {key.rjust(spacing)}: {light[key]}")  # type: ignore


def discover(refresh: bool) -> int:
    """Discover the lights on the network, and display them."""
    discovered = settings["discovered"]

    if refresh:
        lights = leglight.discover(5)
        discovered.data = [light_info(light) for light in lights]
        discovered.save()

    for index, light in enumerate(discovered.data):
        print(f"Light {index}")
        print_light_info(light)

    return 0


def get_light(which: int) -> leglight.LegLight:
    """Return a LegLight object from an index."""
    try:
        info = settings["discovered"].data[which]
    except IndexError:
        raise RuntimeError(f"Light {which} does not exist")

    return leglight.LegLight(info["address"], info["port"])


def turn_on(which: int) -> int:
    """Turn on the requested light."""
    light = get_light(which)
    light.on()
    return 0


def turn_off(which: int) -> int:
    """Turn off the requested light."""
    light = get_light(which)
    light.off()
    return 0


def toggle(which: int) -> int:
    """Toggle the requested light."""
    light = get_light(which)
    return turn_on(which) if light.isOn == 0 else turn_off(which)


def set_color(which: int, color: Optional[int]) -> int:
    """Set the first light's color temperature."""
    light = get_light(which)

    if color is None:
        print(int(light.isTemperature))
        return 0

    light.color(color)
    return 0


def set_brightness(which: int, brightness: Optional[int]) -> int:
    """Set the first light's brightness."""
    light = get_light(which)

    if brightness is None:
        print(light.isBrightness)
        return 0

    light.brightness(brightness)
    return 0


def validate_color_temperature(s: str) -> int:
    """Validate color temperature argument."""

    try:
        value = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{s} is not an integer")

    if value < 2900 or value > 7000:
        raise argparse.ArgumentTypeError(
            "color temperature must be between 2900 and 7000"
        )

    if value % 100 != 0:
        raise argparse.ArgumentTypeError("color temperate must be divisible by 100")

    return value


def validate_brightness(s: str) -> int:
    """Validate brightness argument."""

    try:
        value = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"{s} is not an integer")

    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError("brightness must be between 0 and 100")

    return value


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

    parser_discover = subparsers.add_parser(
        "discover", help="Find and display existing lights"
    )
    parser_discover.add_argument(
        "--refresh",
        action="store_true",
        help="Query the network for lights and save the results",
    )
    parser_discover.set_defaults(action=discover)

    parser_on = subparsers.add_parser("on", help="Turn a light on")
    parser_on.add_argument(
        "which",
        metavar="WHICH",
        nargs="?",
        default=0,
        type=int,
        help="Which light to operate on",
    )
    parser_on.set_defaults(action=turn_on)

    parser_off = subparsers.add_parser("off", help="Turn a light off")
    parser_off.add_argument(
        "which",
        metavar="WHICH",
        nargs="?",
        default=0,
        type=int,
        help="Which light to operate on",
    )
    parser_off.set_defaults(action=turn_off)

    parser_toggle = subparsers.add_parser("toggle", help="Toggle a light")
    parser_toggle.add_argument(
        "which",
        metavar="WHICH",
        nargs="?",
        default=0,
        type=int,
        help="Which light to operate on",
    )
    parser_toggle.set_defaults(action=toggle)

    parser_color = subparsers.add_parser(
        "color", help="Set a light's color temperature"
    )
    parser_color.add_argument(
        "which",
        metavar="WHICH",
        nargs="?",
        default=0,
        type=int,
        help="Which light to operate on",
    )
    parser_color.add_argument(
        "color",
        metavar="COLOR_TEMPERATURE",
        type=validate_color_temperature,
        nargs="?",
        default=None,
        help="Color temperature in Kelvin (2900-7000)",
    )
    parser_color.set_defaults(action=set_color)

    parser_brightness = subparsers.add_parser(
        "brightness", help="Set a light's brightness"
    )
    parser_brightness.add_argument(
        "which",
        metavar="WHICH",
        nargs="?",
        default=0,
        type=int,
        help="Which light to operate on",
    )
    parser_brightness.add_argument(
        "brightness",
        metavar="BRIGHTNESS",
        type=validate_brightness,
        nargs="?",
        default=None,
        help="Brightness level (1-100)",
    )
    parser_brightness.set_defaults(action=set_brightness)

    # Parse the command line arguments and dispatch to the correct subcommand.
    args = parser.parse_args(sys.argv[1:])
    action = args.action
    del args.action

    try:
        return action(**vars(args))
    except RuntimeError as e:
        print(e, file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
