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
    from collections.abc import Iterable


def clone_best(survivors: list[Survivor], fraction: int) -> list[Survivor]:
    fitness_sorted = sorted(
        survivors,
        key=lambda survivor: survivor.calculate_fitness(),
        reverse=True,
    )
    new_survivors = []
    for parent in fitness_sorted[: len(fitness_sorted) // fraction]:
        for _j in range(fraction):
            child = Survivor(
                name=parent.name,
                network=parent.clone_network(),
            )
            new_survivors.append(child)
    return new_survivors


# INEFFICIENT...JUST USE PICK BEST
def generate_new_population(survivors: list[Survivor]) -> list[Survivor]:
    return clone_best(survivors, 2)


def simulate_survival_trial(survivors: list[Survivor], max_time: int) -> None:
    for _t in range(max_time):
        for survivor in survivors:
            if survivor.alive:
                survivor.advance_time()


def mutate(survivor: Survivor) -> None:
    survivor.network.mutate()


def initialize_population(count: int = 100) -> list[Survivor]:
    return [Survivor(name=f"survivor {i}") for i in range(count)]


def print_population_results(survivors: list[Survivor]) -> None:
    for best_survivor in survivors:
        print(
            f"{best_survivor.name}: {best_survivor.calculate_fitness()} - alive for {best_survivor.age} and current health of {best_survivor.health}",
        )


def print_top_best(survivors: list[Survivor], num: int) -> None:
    fitness_sorted = sorted(
        survivors,
        key=lambda survivor: survivor.calculate_fitness(),
        reverse=True,
    )
    for survivor in fitness_sorted[:num]:
        print(
            f"{survivor.name}: {survivor.calculate_fitness()} - alive for {survivor.age} and current health of {survivor.health}",
        )


def get_best_fitness(survivors: Iterable[Survivor]) -> tuple[int, Survivor]:
    high = 0
    survivor = None
    for best_survivor in survivors:
        if best_survivor.calculate_fitness() > high:
            high = best_survivor.calculate_fitness()
            survivor = best_survivor
    if survivor is None:
        raise ValueError("Must have survivors to iterate over")
    return high, survivor


def genetic_algorithm(
    generations: int,
    population_size: int = 100,
    max_simulation_hours: int = 200,
) -> Survivor:

    # randomly initialize population
    # determine fitness of population
    # repeat
    # select parents from population
    # generate new population
    # perform mutation on new population
    # calculate fitness on new population

    # randomly initialize population
    survivors = initialize_population(population_size)
    high_score = 0
    last_print_generation = 0
    try:
        for generation in range(generations):
            # print(f"**********\nGENERATION {generation}\n**********\n")
            simulate_survival_trial(survivors, max_simulation_hours)
            # print_population_results(survivors)
            # print_top_best(survivors, 3)
            best_fitness, best_survivor = get_best_fitness(survivors)

            if best_fitness > high_score:
                print(
                    f"New high value of {best_fitness} in generation {generation}",
                )
                high_score = best_fitness
                print()
                print(f"{best_survivor.network = }")
                print()
                last_print_generation = generation
            elif (
                generation - last_print_generation >= 5 and not generation % 5
            ):
                last_print_generation = generation
                print(f"{generation = }")
                # print(f"Current high: {get_best_fitness(survivors)[0]}, generation: {generation}")
            survivors = generate_new_population(survivors)
            for survivor in survivors:
                mutate(survivor)
    except KeyboardInterrupt:
        print("Genetic algorithm interrupted.")
    return best_survivor


def test() -> None:
    best_survivor = genetic_algorithm(180)
    print(f"{best_survivor = }")

    survivor = Survivor(
        best_survivor.name,
        network=best_survivor.clone_network(),
    )
    for _t in range(200):
        if survivor.alive:
            survivor.advance_time(True)
            survivor.print_information()
            # survivor.advanceTime()
            # survivor.print_information()


if __name__ == "__main__":
    test()
