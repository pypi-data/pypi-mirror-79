# Link to the Past Palette Randomizer

Python Console application to randomize palettes in The Legend of Zelda: A
Link to the Past.

## Table of Contents

- [Link to the Past Palette Randomizer](#link-to-the-past-palette-randomizer)
  - [Table of Contents](#table-of-contents)
  - [What is a palette randomizer?](#what-is-a-palette-randomizer)
  - [Advantages over other palette randomizers](#advantages-over-other-palette-randomizers)
  - [How to use](#how-to-use)
  - [Contributions](#contributions)
  - [Credits](#credits)
  - [License](#license)

## What is a palette randomizer?

A palette randomizer is, as the name suggests, something that randomizes a
game's _palettes_ (its color collections). This randomizer is designed to
randomize colors according to their groupings. For example, all colors that
represent grass will be randomized with the same logic, whereas water's colors
will be randomized with different logic. This creates a consistent color scheme
without any disconnects in colors (e.g. grass having two different colors).

A set of colors is randomized according to the following rules:

- Shift a color's hue by at least 2.5%. This ensures a color is actually changed.
- If increasing saturation, do so very gently and proportional to current value.
- Saturation is okay to be reduced all the way to zero.
- Increasing brightness is similar increasing saturation.
- If a lot of saturation was removed, allow increasing the brightness slightly
  more.
- If reducing brightness, do so by no more than half (this may be restricted
  further in the future).

![example1](https://cdn.discordapp.com/attachments/329059206030295051/641420281608405022/unknown.png)
![example2](https://cdn.discordapp.com/attachments/329059206030295051/641445510074466304/unknown.png)

## Advantages over other palette randomizers

While [Link to the Past Randomizer](https://alttpr.com) already has a built-in
palette randomizer, it does not take the necessary care to ensure every palette
can be randomized. Certain items like houses and rocks are never randomized.
Further, the overworld palette randomizer does not have as much control as this
app does, which allows for much richer variety of colors.

TODO: Add pictures

- The overworld map palette is updated to reflect the new overworld palette.
- Sprite palettes of rocks and bushes match their object palettes.
- Ice golem palettes match Ice Palace palettes.

![example3](https://media.discordapp.net/attachments/329059206030295051/712227454248550450/unknown.png?width=783&height=684)
![example4](https://media.discordapp.net/attachments/329059206030295051/712228332552323112/unknown.png?width=783&height=684)
![example5](https://media.discordapp.net/attachments/329059206030295051/712383831268786216/unknown.png?width=782&height=684)

## How to use

Go to our [Releases](https://github.com/Maseya/z3pr-py/releases)
page. From there, download _z3pr.zip_ under the _Assets_ tab of
the latest release.

Or you can install it through pip with `pip install --user maseya.z3pr`

It is recommended that your logic randomizer app keep the vanilla palette, or
you may still experience ugly colors after using this app.

The following command-line arguments are supported by the app:

```text
[args...] inputFile <outputFile>

inputFile           Input path of ROM. Required

outputFile          Output destination. Optional
                    If no path is specified, the app will
                    decide an appropriate file name.

args:
-w --overworld      Randomize overworld palettes. Default
-W --no-overworld   Do not randomize overworld palettes.

-d --dungeon        Randomize dungeon palettes. Default
-D --no-dungeon     Do not randomize dungeon palettes.

-l --link-sprite    Randomize Link sprite palette.
-L --no-link-sprite Do not randomize Link sprite palette. Default

--sword             Randomize sword palettes.
--no-sword          Do not randomize sword palettes. Default

--shield            Randomize shield palettes.
--no-shield         Do not randomize shield palettes. Default

--hud               Randomize HUD palettes.
--no-hud            Do not randomize HUD palettes. Default

--seed=value        Use specific seed for random generator.
                    Hex is supported with "0x" prefix. Default value
                    is -1, which specifies not using predetermined
                    seed.

--data-dir=value    Read JSON offset files from custom directory.

--mode=value        None: Makes no changes to rom.

                    Default: Default color mixing algorithm.
                    Maseya: Same as "Default".

                    Negative: Invert all colors.

                    Grayscale: Desaturate all colors.

                    Blackout: Set all colors to black.

                    Classic: Randomize palette similar to classic web API.
                        Produces less aesthetic colors if that's your thing.

                    Dizzy: Randomize each color without logic but preserve
                        saturation and lightness.

                    Sick: Randomize each color without logic but preserve
                        lightness.

                    Puke: Randomize each color without logic.
```

You can override the default arguments in the `args.config` file located
in the application folder.

## Contributions

Do you want to add a feature, report a bug, or propose a change to the
project? That's awesome! First, please refer to our
[Contributing](CONTRIBUTING.md) file. We use it in hopes having the best
working environment we can.

## Credits

- [Nelson Garcia](https://github.com/bonimy): Project leader and main
programmer

## License

Python Console App for randomizing Link to the Past palettes
Copyright (C) 2018-2020 Nelson Garcia

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

[issues]: https://github.com/Maseya/z3pr-py/issues
