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
from dataclasses import dataclass, field

from survival_sim.nodes import SharedNode, sumprod


@dataclass(slots=True)
class Node(SharedNode):
    """Node class."""

    neighbors: list[Node] = field(default_factory=list)

    def add_neighbor(self, node: Node, weight: float) -> None:
        """Add neighbor node."""
        self.neighbors.append(node)
        self.weights.append(weight)

    def update_value(self) -> None:
        """Update value."""
        if len(self.neighbors) == len(self.weights):
            self.set_value(
                sumprod(
                    (neighbor.value for neighbor in self.neighbors),
                    self.weights,
                ),
            )

    def set_value(self, value: float) -> None:  # noqa: D102
        super().set_value(max(-1, min(1, value)))


@dataclass(slots=True)
class HopfieldNetwork:
    """Hopfield network."""

    nodes: list[Node] = field(default_factory=list)

    def add_node(self, n: Node) -> None:
        """Add a new node to the network."""
        self.nodes.append(n)

    def create_connection(
        self,
        from_node: Node,
        to_node: Node,
        weight: float | None = None,
    ) -> None:
        """Create a new connection from node to given node with given weight."""
        if weight is None:
            weight = random.random()  # noqa: S311
        to_node.add_neighbor(from_node, weight)

    def print_information(self) -> None:
        """Print information about nodes."""
        for n in self.nodes:
            print(f"Node {n.name}-current value: {n.value}, connected to...")
            for index in range(len(n.weights)):
                print(
                    f"Neighbor: {n.neighbors[index].name} - Weight: {n.weights[index]}",
                )


def main() -> None:
    """Run hopfield simulation."""
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
        print(f"UPDATING NODE {node.name}")

        node.update_value()
        hopfield.print_information()


if __name__ == "__main__":
    main()
