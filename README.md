# elgato
Control program for El Gato brand keylights

This Python package provides the `elgato` program for controlling El Gato brand
lights in your local network. It wraps the excellent
[`leglight`](https://pypi.org/project/leglight/) package, providing a consistent
CLI interface.

## Installation

Check out this repository, and use `pipenv` to bootstrap a development
environment:

```
$ pipenv install
$ pipenv shell
```

Then, the `elgato` command will be available in your environment.

## Usage

`elgato` maintains a list of lights that it knows about, allowing you to control
the power state, color temperature, and brightness via index.

### Light Discovery

To get started, perform a light discovery:

```
$ elgato lights --discover
```

This will create a file `~/.config/elgato/discovered.json` containing a list of
discovered lights. At any time, running

```
$ elgato lights
```

will display information about these lights, while including the `--discover`
flag will refresh the information with a discovery operation.

### Power State

Among the information included is an index for each light. To turn on the first
light:

```
$ elgato on 0
```

To turn it off:

```
$ elgato off 0
```

And, to toggle it:

```
$ elgato toggle 0
```

(Most people have only one light; therefore, this index argument can be omitted
if you wish to operate on Light 0: `elgato on`, `elgato off`, and `elgato
toggle` have the same effect as including the `0` argument as in the examples
above. The `brightness` and `color` subcommands also support this argument
scheme.)

### Brightness

Use the `brightness` subcommand to control the brightness of a light:

```
$ elgato brightness --level 50
$ elgato brightness --brighter
$ elgato brightness --dimmer
```

The `--brighter` and `--dimmer` options take an optional parameter: a value from
0 to 100 by which to adjust the brightness; it is 10 by default.

You can also find out the current brightness level by just doing:

```
$ elgato brightness
```

### Color Temperature

Use the `color` subcommand to control the color temperature of a light. El Gato
lights range from a color temperature of 2900K to 7000K:

```
$ elgato color --level 5300
$ elgato color --warmer
$ elgato color --cooler
```

The `--warmer` and `--cooler` options take an optional parameter: a value from 0
to 4100 by which to adjust the color temperature; it is 500 by default.

You can find out the current color temperature with:

```
$ elgato color
```

## Bug Reports

I would love to hear from you about what you like and don't like about this
package. If you have a question, comment, or run into a problem, please file a
report on [the issue tracker](https://github.com/waxlamp/elgato/issues).
