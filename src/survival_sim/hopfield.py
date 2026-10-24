"""Hopfield."""

# Programmed by CoolCat467

from __future__ import annotations

# Hopfield
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

__title__ = "Hopfield"
__author__ = "Nathan Roth & CoolCat467"
__license__ = "GNU General Public License Version 3"

import random


class Node:
    def __init__(self, id_: str) -> None:
        self.value = 0.0
        self.neighbors: list[Node] = []
        self.weights: list[float] = []
        self.id = id_

    def add_neighbor(self, node: Node, weight: float) -> None:
        self.neighbors.append(node)
        self.weights.append(weight)

    def update_value(self) -> None:
        if len(self.neighbors) == len(self.weights):
            self.value = 0
            for weight, neighbor in zip(
                self.weights,
                self.neighbors,
                strict=True,
            ):
                self.value += neighbor.value * weight
            self.value = max(-1, min(1, self.value))


class HopfieldNetwork:
    def __init__(self, nodes: list[Node] | None = None) -> None:
        if nodes is None:
            self.nodes = []
        else:
            self.nodes = nodes

    def add_node(self, n: Node) -> None:
        self.nodes.append(n)

    def create_connection(
        self,
        from_node: Node,
        to_node: Node,
        weight: float | None = None,
    ) -> None:
        if weight is None:
            weight = random.random()  # noqa: S311
        to_node.add_neighbor(from_node, weight)

    def print_information(self) -> None:
        for n in self.nodes:
            print(f"Node {n.id}-current value: {n.value}, connected to...")
            for index in range(len(n.weights)):
                print(
                    f"Neighbor: {n.neighbors[index].id} - Weight: {n.weights[index]}",
                )


def main() -> None:
    hopfield = HopfieldNetwork()
    n1 = Node("a")
    n2 = Node("b")
    n3 = Node("c")
    hopfield.add_node(n1)
    hopfield.add_node(n2)
    hopfield.add_node(n3)
    n1.add_neighbor(n2, 0.5)
    n2.add_neighbor(n3, 1.9)
    n3.add_neighbor(n1, 2.2)
    n1.add_neighbor(n3, -0.8)
    n2.add_neighbor(n1, 1.2)
    n3.add_neighbor(n2, 0.2)

    n1.value = 1
    n2.value = -1
    n3.value = -1
    hopfield.print_information()

    for i in range(400):
        print(f"\n\n*******\nIteration {i}\n*******")
        x = random.randint(0, 2)  # noqa: S311
        node = hopfield.nodes[x]
        print(f"UPDATING NODE {node.id}")

        node.update_value()
        hopfield.print_information()


if __name__ == "__main__":
    main()
