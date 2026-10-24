"""Nodes."""

# Programmed by CoolCat467

from __future__ import annotations

# Nodes
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

__title__ = "Nodes"
__author__ = "Nathan Roth & CoolCat467"
__license__ = "GNU General Public License Version 3"


import math
import sys
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar, cast

if TYPE_CHECKING:
    from collections.abc import Iterable

    from typing_extensions import Self


Number = TypeVar("Number", int, float)


if sys.version_info < (3, 12):
    import operator

    def sumprod(p: Iterable[Number], q: Iterable[Number]) -> Number:
        """Return the sum of products of values from two iterables p and q."""
        return sum(map(operator.mul, p, q, strict=True))
else:
    sumprod = math.sumprod


@dataclass(slots=True, frozen=True)
class Node(Generic[Number]):
    weights: list[Number]

    def get_value(self, inputs: Iterable[Number]) -> Number:
        """Return value of the sum of input * weight for each pair."""
        return cast("Number", sumprod(inputs, self.weights))  # type: ignore[redundant-cast]

    def copy(self) -> Self:
        """Return a deep copy of this node."""
        return self.__class__(list(self.weights))


class InputNode:
    def __init__(self, name: str, value: int = 0) -> None:
        self.name = name
        self.value = value

        # list of nodes
        self.outputs: list[OutputNode] = []
        # list of weights
        self.weights: list[int] = []

    def set_value(self, v: int) -> None:
        self.value = v

    def get_value(self) -> int:
        return self.value


class OutputNode:
    def __init__(self, name: str, value: int = 0) -> None:
        self.name = name
        self.value = value

        self.inputs: list[InputNode] = []
        self.weights: list[int] = []

    def get_value(self) -> int:
        return self.value


def test() -> None:
    node = Node(weights=[0.25, 0.5])
    print(f"{node = }")
    print(f"{node.get_value((2.0, 4.0)) = }")


if __name__ == "__main__":
    test()
