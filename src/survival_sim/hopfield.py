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
    def __init__(self, i):
        self.value = 0
        self.neighbors = []
        self.weights = []
        self.id = i

    def addNeighbor(self, n: Node, w: float):
        self.neighbors.append(n)
        self.weights.append(w)

    def updateValue(self):
        if len(self.neighbors) == len(self.weights):
            self.value = 0
            for index in range(len(self.neighbors)):
                self.value += self.neighbors[index].value * self.weights[index]
            if self.value < 0:
                self.value = -1
            else:
                self.value = 1


class HopfieldNetwork:
    def __init__(self):
        self.nodes = []

    def addNode(self, n: Node):
        self.nodes.append(n)

    def createConnection(self, nFrom: Node, nTo: Node, w=random.random()):
        nTo.addNeighbor(nFrom, w)

    def printToConsole(self):
        for n in self.nodes:
            print(f"Node {n.id}-current value: {n.value}, connected to...")
            for index in range(len(n.weights)):
                print(
                    f"Neighbor: {n.neighbors[index].id} - Weight: {n.weights[index]}",
                )


def main():
    h = HopfieldNetwork()
    n1 = Node("a")
    n2 = Node("b")
    n3 = Node("c")
    h.addNode(n1)
    h.addNode(n2)
    h.addNode(n3)
    n1.addNeighbor(n2, 0.5)
    n2.addNeighbor(n3, 1.9)
    n3.addNeighbor(n1, 2.2)
    n1.addNeighbor(n3, -0.8)
    n2.addNeighbor(n1, 1.2)
    n3.addNeighbor(n2, 0.2)

    n1.value = 1
    n2.value = -1
    n3.value = -1
    h.printToConsole()
    print("hi")

    for i in range(400):
        print(f"\n\n*******\nIteration {i}\n*******")
        x = random.randint(0, 2)
        print("UPDATING NODE " + str(h.nodes[x].id))
        myNode = h.nodes[x]
        myNode.updateValue()
        h.printToConsole()


if __name__ == "__main__":
    main()
