"""Network."""

# Programmed by CoolCat467

from __future__ import annotations

# Network
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

__title__ = "Network"
__author__ = "Nathan Roth & CoolCat467"
__license__ = "GNU General Public License Version 3"

import random
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic

from survival_sim.nodes import InputNode, Node, Number, OutputNode

if TYPE_CHECKING:
    from collections.abc import Sequence

    from typing_extensions import Self


class OldNetwork:
    def __init__(self) -> None:
        self.setup_network()

    def setup_network(self) -> None:
        tNode = InputNode("thirst")
        hNode = InputNode("hunger")
        eNode = InputNode("energy")
        sNode = InputNode("shelter")
        fNode = InputNode("food stash")
        wNode = InputNode("water stash")
        drinkNode = OutputNode("drink")
        eatNode = OutputNode("eat")
        sleepNode = OutputNode("sleep")
        shelterNode = OutputNode("make shelter")
        nothingNode = OutputNode("relax")
        huntNode = OutputNode("hunt")
        scavengeNode = OutputNode("scavenge")
        findWaterNode = OutputNode("find water")
        self.inputNodes = [tNode, hNode, eNode, sNode, fNode, wNode]
        self.outputNodes = [
            drinkNode,
            eatNode,
            sleepNode,
            shelterNode,
            huntNode,
            scavengeNode,
            findWaterNode,
            nothingNode,
        ]
        for i in self.inputNodes:
            i.value = random.randint(0, 100)
            for o in self.outputNodes:
                i.outputs.append(o)
                o.inputs.append(i)
                w = random.randint(-10, 10)
                i.weights.append(w)
                o.weights.append(w)

    def assignInputs(
        self,
        thirst: int = 0,
        hunger: int = 0,
        energy: int = 0,
        shelter: int = 0,
        food: int = 0,
        water: int = 0,
    ) -> None:
        self.inputNodes[0].value = thirst
        self.inputNodes[1].value = hunger
        self.inputNodes[2].value = energy
        self.inputNodes[3].value = shelter
        self.inputNodes[4].value = food
        self.inputNodes[5].value = water

    def printToConsole(self) -> None:
        # for i in self.inputNodes:
        # print(f"{i.name} node\n\tValue:{i.getValue()}\n\tConnections:")
        # for index in range (len(i.outputs)):
        # print(f"\t\t{i.outputs[index].name}: {i.weights[index]}")
        for i in self.outputNodes:
            print(f"{i.name} node\n\tValue:{i.getValue()}\n\tConnections:")
            for index in range(len(i.inputs)):
                print(f"\t\t{i.inputs[index].name}: {i.weights[index]}")

    def propagate(self) -> None:
        for node in self.outputNodes:
            node.value = 0
            for index in range(len(node.inputs)):
                node.value += (
                    node.inputs[index].getValue() * node.weights[index]
                )
            # print(f"{node.name} now has a value of {node.value}")

    def getAction(self) -> str:
        highestValue = float("-inf")
        action = ""
        for OutputNode in self.outputNodes:
            if OutputNode.getValue() > highestValue:
                highestValue = OutputNode.getValue()
                action = OutputNode.name
        return action

    def copyNetwork(self) -> Self:
        newNetwork = self.__class__()
        for i in range(len(newNetwork.inputNodes)):
            for j in range(len(newNetwork.inputNodes[i].weights)):
                newNetwork.inputNodes[i].weights[j] = self.inputNodes[
                    i
                ].weights[j]
        for i in range(len(newNetwork.outputNodes)):
            for j in range(len(newNetwork.outputNodes[i].weights)):
                newNetwork.outputNodes[i].weights[j] = self.outputNodes[
                    i
                ].weights[j]
        return newNetwork

    def mutate(self) -> None:
        pass

    def getHash(self) -> None:
        for i in range(len(self.inputNodes)):
            for _j in range(len(self.inputNodes[i].weights)):
                pass


def test_old() -> None:
    n = OldNetwork()
    # n.propagate()
    n.printToConsole()
    o = OldNetwork()
    o.printToConsole()
    print("\n\n\n")
    p = o.copyNetwork()
    p.printToConsole()


@dataclass(frozen=True, slots=True)
class Network(Generic[Number]):
    layers: list[list[Node[Number]]]

    def feed_forward(self, inputs: list[Number]) -> list[Number]:
        """Return the output layer after feeding inputs through the network."""
        input_ = inputs
        for layer in self.layers:
            output = [node.get_value(input_) for node in layer]
            input_ = output
        return output


@dataclass(frozen=True, slots=True)
class ActionNetwork(Network[Number], Generic[Number]):
    input_names: tuple[str, ...]
    action_names: tuple[str, ...]

    @staticmethod
    def setup_network(
        input_names: Sequence[str],
        action_names: Sequence[str],
    ) -> list[list[Node[int]]]:
        """Return a new random simple network layers using action and input names."""
        layers = []
        output_layer = []
        for _action_name in action_names:
            weights = []
            for _input_name in input_names:
                weights.append(random.randint(-100, 100))
            node = Node(weights)
            output_layer.append(node)
        layers.append(output_layer)
        return layers

    @classmethod
    def new_network(
        cls,
        input_names: Sequence[str],
        action_names: Sequence[str],
    ) -> Self[int]:
        """Initialize action network."""
        return cls(
            cls.setup_network(input_names, action_names),
            tuple(input_names),
            tuple(action_names),
        )

    def get_action_values(
        self,
        input_values: dict[str, Number],
    ) -> dict[str, Number]:
        """Return a dictionary of action names to values given a dict of input names to values."""
        inputs = [input_values[key] for key in self.input_names]
        output = self.feed_forward(inputs)
        return dict(zip(self.action_names, output, strict=True))

    def get_action(self, input_values: dict[str, Number]) -> str:
        """Return the action to perform given a dict of input names to values."""
        action_results = self.get_action_values(input_values)
        action = max(
            action_results.items(),
            key=lambda action_result: action_result[1],
        )
        return action[0]

    def copy(self) -> Self:
        """Return a deep copy of this network."""
        layers = [[node.copy() for node in layer] for layer in self.layers]
        return self.__class__(
            layers,
            self.input_names,
            self.action_names,
        )


def test() -> None:
    input_fields = (
        "thirst",
        "hunger",
        "energy",
        "shelter",
        "food stash",
        "water stash",
    )
    actions = (
        "drink",
        "eat",
        "sleep",
        "make shelter",
        "hunt",
        "scavenge",
        "find water",
        "rest",
    )
    network = ActionNetwork.new_network(input_fields, actions)
    print(f"{network = }")
    input_values = {
        field_name: random.randint(0, 100) for field_name in input_fields
    }
    print(f"{input_values = }")
    print(f"{network.get_action_values(input_values) = }")
    print(f"{network.get_action(input_values) = }")


if __name__ == "__main__":
    test()
# types: syntax error: Expected dedent, found end of file
