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

import dataclasses
import random
from typing import TYPE_CHECKING, ClassVar

from survival_sim.network import ActionNetwork

if TYPE_CHECKING:
    from collections.abc import Generator


@dataclasses.dataclass(slots=True)
class BaseSurvivor:
    MAX_HEALTH: ClassVar = 100
    MAX_HUNGER: ClassVar = 100
    MAX_THIRST: ClassVar = 100
    MAX_SLEEP: ClassVar = 100

    name: str

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
        """Return if health is greater than zero."""
        return self.health > 0

    def action_eat(self) -> None:
        """Perform eat action."""
        if self.food_stash <= 0:
            return
        self.food_stash -= 1
        if self.hunger < 90:
            self.hunger += 10
        if self.hunger > 80 and self.health < 95:
            self.health += 2

    def action_drink(self) -> None:
        """Perform drink action."""
        if self.water_stash <= 0:
            return
        self.water_stash -= 1
        if self.thirst < 92:
            self.thirst += 8
        if self.thirst > 80 and self.health < 95:
            self.health += 2

    def action_sleep(self) -> None:
        """Perform sleep action."""
        self.sleep = min(self.MAX_SLEEP, self.sleep + 10)

    def action_make_shelter(self) -> None:
        """Perform make shelter action."""
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
        """Perform scavenge action."""
        chance = random.randint(1, 6)  # noqa: S311
        if chance < 5:
            self.food_stash += 1
        self.sleep -= 3

    def action_hunt(self) -> None:
        """Perform hunt action."""
        chance = random.randint(1, 6)  # noqa: S311
        if chance < 3:
            self.food_stash += 3
        self.sleep -= 8

    def action_find_water(self) -> None:
        """Perform find water action."""
        chance = random.randint(1, 6)  # noqa: S311
        if chance < 5:
            self.water_stash += 1
        elif chance < 6:
            self.water_stash += 3
        self.sleep -= 2

    def decide_action(self) -> str:
        """Return an action to perform."""
        return "rest"

    def advance_time(self, printing: bool = False) -> None:
        """Advance time and perform an action."""
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
            if printing:
                print(f"{self.name} is dead")
            return

        action = self.decide_action()
        self.perform_action(action)
        if printing:
            print(f"{self.name} just did the {action} action")

    def perform_action(self, action: str) -> None:
        """Perform the given action."""
        action_title = action.replace(" ", "_")
        perform_action_function = getattr(self, f"action_{action_title}", None)
        if perform_action_function is not None:
            assert callable(perform_action_function)
            perform_action_function()

    def calculate_fitness(self) -> int:
        """Return fitness."""
        return self.age + self.health

    def print_information(self) -> None:
        """Print general status information."""
        print(
            f"{self.name} Hour {self.age}:\tHealth: {self.health}, Hunger: {self.hunger}, Thirst: {self.thirst}, Energy: {self.sleep}, Shelter: {self.shelter}\n",
        )

    @classmethod
    def get_action_functions(cls) -> list[str]:
        """Return a list of all action functions."""
        return [attr[7:] for attr in dir(cls) if attr.startswith("action_")]

    @classmethod
    def yield_input_fields(cls) -> Generator[str, None, None]:
        """Yield all dataclass fields that are pre-initialized and not factory fields."""
        for field in dataclasses.fields(cls):
            if field.default is dataclasses.MISSING:
                continue
            if field.default_factory is not dataclasses.MISSING:
                continue
            yield field.name

    @classmethod
    def create_network(cls) -> ActionNetwork[int]:
        """Return a new ActionNetwork with all input fields and actions."""
        input_fields = sorted(cls.yield_input_fields())
        actions = sorted(["relax", *cls.get_action_functions()])
        return ActionNetwork.new_network(input_fields, actions)

    def get_inputs(self) -> dict[str, int]:
        """Return dictionary of network input fields."""
        input_fields = set(self.yield_input_fields())
        return {
            k: v
            for k, v in dataclasses.asdict(self).items()
            if k in input_fields
        }


# Would have loved to do this all in one class, but not possible to
# define a field with a factory default that uses a class method as it's
# build function.


@dataclasses.dataclass(slots=True)
class Survivor(BaseSurvivor):
    network: ActionNetwork[int] = dataclasses.field(
        default_factory=BaseSurvivor.create_network,
    )

    def decide_action(self) -> str:
        return self.network.get_action(self.get_inputs())

    def clone_network(self) -> ActionNetwork[int]:
        """Return a copy of the network."""
        return self.network.copy()
