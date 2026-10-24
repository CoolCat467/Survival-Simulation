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


import argparse
from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING

from survival_sim.genetic import (
    genetic_algorithm,
    initialize_population,
)
from survival_sim.network import ActionNetwork
from survival_sim.survivor import Survivor

if TYPE_CHECKING:
    from collections.abc import Generator


def test() -> None:
    """Run program."""
    s1 = Survivor("Alice")
    s2 = Survivor("Bob")
    survivors = [s1, s2]
    for _t in range(200):
        for survivor in survivors:
            if survivor.alive:
                survivor.advance_time()
                survivor.print_information()


def current_iso_timestamp() -> str:
    """Return current ISO timestamp up to seconds."""
    return datetime.today().isoformat(timespec="seconds")


def save_survivor(saved_survivors_folder: Path, survivor: Survivor) -> None:
    """Save given survivor to file."""
    default_name = current_iso_timestamp().replace(":", "-")
    name = input(f"Enter custom name (default {default_name!r} if blank): ")
    if not name:
        name = default_name
    filename = f"{name}.json"
    if not saved_survivors_folder.exists():
        saved_survivors_folder.mkdir()

    filepath = saved_survivors_folder / filename
    filepath.write_bytes(survivor.serialize())
    print(f"Saved survivor as {str(filepath)!r}")


def load_network(network_filepath: Path) -> ActionNetwork[int]:
    """Return network loaded from given filepath."""
    return ActionNetwork[int].from_bytes(network_filepath.read_bytes())


def load_survivor(survivor_filepath: Path) -> Survivor:
    """Return network loaded from given filepath."""
    return Survivor.from_bytes(survivor_filepath.read_bytes())


def yield_json_files(folder: Path) -> Generator[Path, None, None]:
    """Yield json files from given folder."""
    if not folder.exists():
        return
    for file in folder.iterdir():
        if not file.is_file():
            continue
        if file.suffix != ".json":
            continue
        yield file


def load_population(
    saved_survivors_folder: Path,
) -> list[Survivor]:
    """Load all survivors from folder."""
    survivors = []
    for index, survivor_filepath in enumerate(
        yield_json_files(saved_survivors_folder),
    ):
        original_survivor = load_survivor(survivor_filepath)
        survivors.append(
            Survivor(
                f"loaded survivor {index}",
                network=original_survivor.network,
            ),
        )

    return survivors


def main() -> None:
    """Run genetic algorithm simulation."""
    parser = argparse.ArgumentParser(
        description="Run genetic algorithm for survival simulation.",
        suggest_on_error=True,
        color=True,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"{__title__} v{__version__}",
        help="Show the program version and exit.",
    )
    parser.add_argument(
        "--generations",
        type=int,
        default=2000,
        help="Genetic algorithm generation count",
    )
    parser.add_argument(
        "--population-size",
        type=int,
        default=100,
        help="Population batch size per generation",
    )
    parser.add_argument(
        "--max-simulation-iterations",
        type=int,
        default=200,
        help="Maximum number of simulation iterations per batch",
    )
    parser.add_argument(
        "--new-network-hidden-layer-count",
        type=int,
        default=0,
        help="Number of hidden layers for new networks",
    )
    parser.add_argument(
        "--cull-fraction",
        type=int,
        default=1,
        help="Cull the lower 1/(cull fraction) of the population sorted by fitness",
    )

    args = parser.parse_args()

    population_size = int(args.population_size)
    hidden_layers = max(0, int(args.new_network_hidden_layer_count))
    generations = int(args.generations)
    max_simulation_iterations = int(args.max_simulation_iterations)
    cull_fraction = max(1, int(args.cull_fraction))

    this_file = Path(__file__).absolute()
    this_folder = this_file.parent
    saved_survivors_folder = this_folder / "survivor_data"

    load_survivors = False
    if saved_survivors_folder.exists():
        load_survivors = (
            input(
                "Would you like to load initial survivors instead starting with new random survivors? (y/N): ",
            ).lower()
            == "y"
        )

    if load_survivors:
        survivors = load_population(saved_survivors_folder)
        print(f"Loaded {len(survivors)} survivors from files.")

        # Pad missing with new random survivors
        missing = population_size - len(survivors)
        survivors.extend(initialize_population(missing, hidden_layers))
        print(f"Created {missing} new random survivors.\n")
    else:
        # randomly initialize population
        survivors = initialize_population(population_size, hidden_layers)

    input("Press enter to start.\n")

    best_survivor = genetic_algorithm(
        survivors,
        generations,
        max_simulation_iterations,
        cull_fraction,
    )
    # print(f"{best_survivor = }")

    survivor = Survivor(
        best_survivor.name,
        network=best_survivor.clone_network(),
    )

    print()
    if input("Would you like to save this survivor? (Y/n): ").lower() != "n":
        save_survivor(saved_survivors_folder, best_survivor)

    # for _t in range(200):
    while survivor.alive:
        if survivor.alive:
            survivor.advance_time(True)
            survivor.print_information()
            # survivor.advanceTime()
            # survivor.print_information()


def cli_run() -> None:
    """CLI entrypoint."""
    main()


if __name__ == "__main__":
    print(f"{__title__} v{__version__}\nProgrammed by {__author__}.\n")
    cli_run()
