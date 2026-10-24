"""Survivor."""

# Programmed by CoolCat467

from __future__ import annotations

# Survivor
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

__title__ = "Survivor"
__author__ = "Nathan Roth & CoolCat467"
__license__ = "GNU General Public License Version 3"

import random
from dataclasses import dataclass, field
from typing import ClassVar

from survival_sim.network import OldNetwork


@dataclass(slots=True)
class Survivor:
    MAX_HEALTH: ClassVar = 100
    MAX_HUNGER: ClassVar = 100
    MAX_THIRST: ClassVar = 100
    MAX_SLEEP: ClassVar = 100

    name: str
    network: OldNetwork = field(default_factory=OldNetwork)

    thirst: int = MAX_THIRST
    hunger: int = MAX_HUNGER
    sleep: int = MAX_SLEEP
    health: int = MAX_HEALTH
    food_stash: int = 0
    water_stash: int = 0
    shelter: int = 0
    age: int = 0

    @property
    def alive(self) -> bool:
        return self.health > 0

    def action_eat(self) -> None:
        if self.food_stash <= 0:
            return
        self.food_stash -= 1
        if self.hunger < 90:
            self.hunger += 10
        if self.hunger > 80 and self.health < 95:
            self.health += 2

    def action_drink(self) -> None:
        if self.water_stash <= 0:
            return
        self.water_stash -= 1
        if self.thirst < 92:
            self.thirst += 8
        if self.thirst > 80 and self.health < 95:
            self.health += 2

    def action_sleep(self) -> None:
        self.sleep = min(self.MAX_SLEEP, self.sleep + 10)

    def action_make_shelter(self) -> None:
        if self.shelter < 40:
            self.shelter += 15
        elif self.shelter < 80:
            self.shelter += 10
        elif self.shelter < 95:
            # Old said -= 5 here, I think that's a typo?
            # self.shelter -= 5
            self.shelter += 5
        self.sleep -= 5

    def action_scavenge(self) -> None:
        chance = random.randint(1, 6)  # noqa: S311
        if chance < 5:
            self.food_stash += 1
        self.sleep -= 3

    def action_hunt(self) -> None:
        chance = random.randint(1, 6)  # noqa: S311
        if chance < 3:
            self.food_stash += 3
        self.sleep -= 8

    def action_find_water(self) -> None:
        chance = random.randint(1, 6)  # noqa: S311
        if chance < 5:
            self.water_stash += 1
        elif chance < 6:
            self.water_stash += 3
        self.sleep -= 2

    def advance_time(self, printing: bool = False) -> None:
        # get hungrier, get thirstier, lose energy
        self.hunger = max(self.hunger - 3, 0)
        self.thirst = max(self.thirst - 3, 0)
        self.age += 1

        if self.shelter < 20:
            self.sleep -= 5
        elif self.shelter < 40:
            self.sleep -= 3
        elif self.shelter < 60:
            self.sleep -= 1

        self.sleep = max(self.sleep - 2, 0)
        if self.hunger < 20 or self.thirst < 20 or self.sleep < 20:
            self.health -= 1
        if not self.alive:
            # print(f"{self.name} just died")
            return
        self.decide_action(printing)

    def get_actions(self) -> list[str]:
        return sorted(
            attr[7:] for attr in dir(self) if attr.startswith("action_")
        )

    def decide_action(self, printing: bool = False) -> None:
        self.network.assign_inputs(
            self.thirst,
            self.hunger,
            self.sleep,
            self.shelter,
            self.food_stash,
            self.water_stash,
        )
        self.network.propagate()
        action_title = self.network.get_action()
        action_title = action_title.replace(" ", "_")
        action_function_name = f"action_{action_title}"
        perform_action_function = getattr(self, action_function_name, None)
        if perform_action_function is not None:
            assert callable(perform_action_function)
            perform_action_function()
        if printing:
            print(f"{self.name} just did the {action_title} action")

    def calculate_fitness(self) -> int:
        return self.age + self.health

    def clone_network(self) -> OldNetwork:
        return self.network.copy()

    def print_information(self) -> None:
        print(
            f"{self.name} Hour {self.age}:\tHealth: {self.health}, Hunger: {self.hunger}, Thirst: {self.thirst}, Energy: {self.sleep}, Shelter: {self.shelter}\n",
        )
