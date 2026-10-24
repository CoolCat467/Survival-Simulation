"""Genetic."""

# Programmed by CoolCat467

from __future__ import annotations

# Genetic
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

__title__ = "Genetic"
__author__ = "Nathan Roth & CoolCat467"
__license__ = "GNU General Public License Version 3"


from typing import TYPE_CHECKING

from survival_sim.survivor import Survivor

if TYPE_CHECKING:
    from collections.abc import Generator, Iterable


def clone_best(survivors: list[Survivor], fraction: int) -> list[Survivor]:
    """Return a clone of the top 1/fraction survivors and cull everything below."""
    fitness_sorted = sorted(
        survivors,
        key=lambda survivor: survivor.calculate_fitness(),
        reverse=True,
    )
    new_survivors = []
    for parent in fitness_sorted[: len(fitness_sorted) // fraction]:
        for _j in range(fraction):
            child = Survivor(
                parent.name,
                network=parent.network,
            )
            new_survivors.append(child)
    ##    new_survivors[-1] = Survivor(fitness_sorted[-1].name)
    return new_survivors


# INEFFICIENT...JUST USE PICK BEST
def generate_new_population(
    survivors: list[Survivor],
    cull_fraction: int = 2,
) -> list[Survivor]:
    """Return a new population after culling 1/cull_fraction and cloning the rest."""
    return clone_best(survivors, cull_fraction)


def while_truthy_gen(obj: object) -> Generator[int, None, None]:
    """Yield increasing count number while obj is truthy."""
    i = 0
    while obj:
        yield i
        i += 1


def simulate_survival_trial(
    survivors: Iterable[Survivor],
    iterations: int | None = None,
) -> None:
    """Simulate a population of survivors for a given number if iterations."""
    # Get a copy of references to the survivors. Only need to tick the
    # ones that are alive.
    active_survivors = list(survivors)

    iterate: Iterable[int]
    if iterations is not None:
        iterate = range(iterations)
    else:
        iterate = while_truthy_gen(active_survivors)

    for _t in iterate:
        index = 0
        for survivor in tuple(active_survivors):
            survivor.advance_time()
            if survivor.alive:
                index += 1
                continue
            del active_survivors[index]


def mutate(survivor: Survivor) -> None:
    """Potentially mutate a survivor's network *IN-PLACE*."""
    survivor.mutate_network()


def initialize_population(count: int, hidden_layers: int) -> list[Survivor]:
    """Return a population of new survivors."""
    return [
        Survivor(
            f"survivor {i}",
            network=Survivor.create_network(hidden_layers),
        )
        for i in range(count)
    ]


def print_population_results(survivors: list[Survivor]) -> None:
    """Print information about all survivors in a given population."""
    for survivor in survivors:
        print(
            f"{survivor.name}: {survivor.calculate_fitness()} - alive for {survivor.age} and current health of {survivor.health}",
        )


def print_top_best(survivors: list[Survivor], count: int) -> None:
    """Print the top count survivors by fitness."""
    fitness_sorted = sorted(
        survivors,
        key=lambda survivor: survivor.calculate_fitness(),
        reverse=True,
    )
    for survivor in fitness_sorted[:count]:
        print(
            f"{survivor.name}: {survivor.calculate_fitness()} - alive for {survivor.age} and current health of {survivor.health}",
        )


def get_best_fitness(survivors: Iterable[Survivor]) -> tuple[int, Survivor]:
    """Return the survivor with the best fitness."""
    fitness_survivors = [
        (survivor.calculate_fitness(), survivor) for survivor in survivors
    ]
    return max(
        fitness_survivors,
        key=lambda fitness_survivor: fitness_survivor[0],
    )


def genetic_algorithm(
    generations: int,
    population_size: int = 100,
    max_simulation_iterations: int | None = None,
    cull_fraction: int = 2,
    hidden_layers: int = 1,
) -> Survivor:
    """Return the survivor with the best fitness after given number of generations."""
    # randomly initialize population
    # determine fitness of population
    # repeat
    # select parents from population
    # generate new population
    # perform mutation on new population
    # calculate fitness on new population

    # randomly initialize population
    survivors = initialize_population(population_size, hidden_layers)
    high_score = 0
    last_print_generation = 0
    try:
        for generation in range(generations):
            # print(f"**********\nGENERATION {generation}\n**********\n")
            simulate_survival_trial(survivors, max_simulation_iterations)
            # print_population_results(survivors)
            # print_top_best(survivors, 3)
            best_fitness, survivor = get_best_fitness(survivors)

            if best_fitness > high_score:
                print(
                    f"New high value of {best_fitness} in generation {generation}",
                )
                high_score = best_fitness
                print()
                print(f"{survivor.network = }")
                print()
                last_print_generation = generation
            elif (
                generation - last_print_generation >= 5 and not generation % 5
            ):
                last_print_generation = generation
                print(f"{generation = }")
                # print(f"Current high: {get_best_fitness(survivors)[0]}, generation: {generation}")
            survivors = generate_new_population(survivors, cull_fraction)
            for survivor in survivors:
                mutate(survivor)
    except KeyboardInterrupt:
        print("Genetic algorithm interrupted.")
    return survivor


def main() -> None:
    """Run genetic algorithm simulation."""
    best_survivor = genetic_algorithm(2000)
    print(f"{best_survivor = }")

    survivor = Survivor(
        best_survivor.name,
        network=best_survivor.clone_network(),
    )
    # for _t in range(200):
    while survivor.alive:
        if survivor.alive:
            survivor.advance_time(True)
            survivor.print_information()
            # survivor.advanceTime()
            # survivor.print_information()


if __name__ == "__main__":
    main()
