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
from functools import wraps
from typing import TYPE_CHECKING, ClassVar

import orjson

from survival_sim.network import ActionNetwork

if TYPE_CHECKING:
    from collections.abc import Callable, Generator, Iterable

    from typing_extensions import Self


def combine_end(data: Iterable[str], final: str = "and") -> str:
    """Join values of text, and have final with the last one properly."""
    data = list(map(str, data))
    if len(data) >= 2:
        data[-1] = f"{final} {data[-1]}"
    if len(data) > 2:
        return ", ".join(data)
    return " ".join(data)


def costs(
    **kwargs: int,
) -> Callable[
    [Callable[[BaseSurvivor], None]],
    Callable[[BaseSurvivor], bool],
]:
    """Return a decorator to require an action to cost an attribute."""

    def action_decorator(
        action_function: Callable[[BaseSurvivor], None],
    ) -> Callable[[BaseSurvivor], bool]:
        """Return wrapped action function that incurs an attribute and won't run if not enough of an attribute."""

        @wraps(action_function)
        def wrapper(self: BaseSurvivor) -> bool:
            """Return True if wrapped action function incurred cost and ran."""
            if not self.can_perform_action(kwargs):
                # not successful
                return False
            self.incur_attribute_costs(kwargs)

            # Perform original action
            action_function(self)

            return True

        # Add documentation about new attribute costs.
        if not wrapper.__doc__:
            wrapper.__doc__ = ""
        else:
            wrapper.__doc__ += " "
        cost_info = combine_end(
            f"{count} {attr}" for attr, count in kwargs.items()
        )
        cost_attrs_info = combine_end(kwargs, "or")

        wrapper.__doc__ += f"""Costs {cost_info}.

Returns False if could not perform action because of not enough {cost_attrs_info}.
Return True if successful."""

        # Remember which attributes are required for printing later
        wrapper.cost_attrs_info = cost_attrs_info  # type: ignore[attr-defined]

        return wrapper

    return action_decorator


@dataclasses.dataclass(slots=True)
class BaseSurvivor:
    """Base survivor class without a brain."""

    MAX_HEALTH: ClassVar = 100
    MAX_HUNGER: ClassVar = 100
    MAX_THIRST: ClassVar = 100
    MAX_ENERGY: ClassVar = 100

    name: str

    thirst: int = MAX_THIRST
    hunger: int = MAX_HUNGER
    energy: int = MAX_ENERGY
    health: int = MAX_HEALTH
    food_stash: int = 0
    water_stash: int = 0
    shelter: int = 0
    age: int = 0

    @property
    def alive(self) -> bool:
        """Return if health is greater than zero."""
        return self.health > 0

    def can_perform_action(self, costs: dict[str, int]) -> bool:
        """Return if able to perform an action that costs a given amount of an attribute."""
        for attribute, cost in costs.items():
            if getattr(self, attribute) < cost:
                return False
        return True

    def incur_attribute_costs(self, costs: dict[str, int]) -> None:
        """Incur given attribute costs."""
        billable_attributes = set(BaseSurvivor.yield_input_fields())
        for attribute, cost in costs.items():
            assert attribute in billable_attributes, attribute
            new_value = getattr(self, attribute) - cost
            setattr(self, attribute, new_value)

    @costs(food_stash=1)
    def action_eat(self) -> None:
        """Perform eat action."""
        if self.hunger < 90:
            self.hunger += 10
        if self.hunger > 80 and self.health < 95:
            self.health += 2

    @costs(water_stash=1)
    def action_drink(self) -> None:
        """Perform drink action."""
        if self.thirst < 92:
            self.thirst += 8
        if self.thirst > 80 and self.health < 95:
            self.health += 2

    def action_sleep(self) -> None:
        """Perform sleep action."""
        self.energy = min(self.MAX_ENERGY, self.energy + 10)

    @costs(energy=5)
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

    @costs(energy=3)
    def action_scavenge(self) -> None:
        """Perform scavenge action."""
        chance = random.randint(1, 6)  # noqa: S311
        if chance < 5:
            self.food_stash += 1

    @costs(energy=8)
    def action_hunt(self) -> None:
        """Perform hunt action."""
        chance = random.randint(1, 6)  # noqa: S311
        if chance < 3:
            self.food_stash += 3

    @costs(energy=2)
    def action_find_water(self) -> None:
        """Perform find water action."""
        chance = random.randint(1, 6)  # noqa: S311
        if chance < 5:
            self.water_stash += 1
        elif chance < 6:
            self.water_stash += 3

    def decide_action(self) -> str:
        """Return an action to perform."""
        return "relax"

    def advance_time(self, printing: bool = False) -> None:
        """Advance time and perform an action."""
        # get hungrier, get thirstier, lose energy
        self.hunger = max(self.hunger - 3, 0)
        self.thirst = max(self.thirst - 3, 0)
        self.age += 1

        if self.shelter < 20:
            self.energy -= 5
        elif self.shelter < 40:
            self.energy -= 3
        elif self.shelter < 60:
            self.energy -= 1

        self.energy = max(0, self.energy - 2)

        # take damage from poor conditions
        if self.hunger < 20 or self.thirst < 20:
            self.health -= 5
        if self.energy < 20:
            self.health -= 1

        if not self.alive:
            if printing:
                print(f"{self.name} is dead")
            return

        action = self.decide_action()
        success, cost_attr_info = self.perform_action(action)
        if printing:
            if success:
                print(f"{self.name} just did the {action} action")
            else:
                if cost_attr_info is None:
                    cost_attr_info = "of an unknown attribute"
                print(
                    f"{self.name} wanted to do the {action} action but didn't have enough {cost_attr_info}",
                )

    def perform_action(self, action: str) -> tuple[bool, str | None]:
        """Perform the given action. Return if successful.

        Not successful if energy was too low.
        """
        action_title = action.replace(" ", "_")
        perform_action_function = getattr(self, f"action_{action_title}", None)
        if perform_action_function is not None:
            assert callable(perform_action_function)
            result = perform_action_function()
            if result is not None:
                cost_attrs_info = getattr(
                    perform_action_function,
                    "cost_attrs_info",
                    None,
                )
                return bool(result), cost_attrs_info
        return True, None

    def calculate_fitness(self) -> int:
        """Return fitness."""
        return self.age + self.health

    def print_information(self) -> None:
        """Print general status information."""
        print(
            f"{self.name} Hour {self.age}:\tHealth: {self.health}, Hunger: {self.hunger}, Thirst: {self.thirst}, Energy: {self.energy}, Shelter: {self.shelter}\n",
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
    def create_network(cls, hidden_layers: int = 0) -> ActionNetwork[int]:
        """Return a new ActionNetwork with all input fields and actions."""
        input_fields = sorted(cls.yield_input_fields())
        actions = sorted(["relax", *cls.get_action_functions()])
        return ActionNetwork.new_network(input_fields, actions, hidden_layers)

    def get_inputs(self) -> dict[str, int]:
        """Return dictionary of network input fields."""
        input_fields = set(self.yield_input_fields())
        return {
            k: v
            for k, v in dataclasses.asdict(self).items()
            if k in input_fields
        }

    def serialize(self) -> bytes:
        """Return json payload from instance."""
        return orjson.dumps(self)

    @classmethod
    def from_bytes(cls, payload: bytes) -> Self:
        """Return instance from json payload."""
        return cls(**orjson.loads(payload))


# Would have loved to do this all in one class, but not possible to
# define a field with a factory default that uses a class method as it's
# build function.


@dataclasses.dataclass(slots=True)
class Survivor(BaseSurvivor):
    """Survivor class with a brain."""

    network: ActionNetwork[int] = dataclasses.field(
        default_factory=BaseSurvivor.create_network,
    )

    def decide_action(self) -> str:  # noqa: D102
        return self.network.get_action(self.get_inputs())

    def clone_network(self) -> ActionNetwork[int]:
        """Return a copy of the network."""
        return self.network.copy()

    def mutate_network(self) -> None:
        """Mutate network *IN-PLACE*."""
        self.network = self.network.mutate()

    @classmethod
    def from_bytes(cls, payload: bytes) -> Self:
        """Return instance from json payload."""
        data = orjson.loads(payload)
        data["network"] = ActionNetwork.from_dict(data["network"])
        return cls(**data)
