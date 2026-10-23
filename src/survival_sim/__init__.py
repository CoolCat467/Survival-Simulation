"""Survival Simulation."""

# Programmed by CoolCat467

from __future__ import annotations

# Survival Simulation
# Copyright (C) 2025  Nathan Roth
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__title__ = "Survival Simulation"
__author__ = "Nathan Roth & CoolCat467"
__version__ = "0.0.0"
__license__ = "GNU General Public License Version 3"


from survival_sim.survivor import Survivor


def run() -> None:
    """Run program."""
    s1 = Survivor()
    s2 = Survivor()
    s1.name="Alice"
    s2.name = "Bob"
    s = [s1, s2]
    for t in range(200):
        for person in s:
            if person.alive:
                person.advanceTime()
                person.printToConsole()


def cli_run() -> None:
    """CLI entrypoint."""
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    run()


if __name__ == "__main__":
    cli_run()
