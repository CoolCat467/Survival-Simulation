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
from typing import TYPE_CHECKING, Generic, cast

from survival_sim.nodes import InputNode, Node, Number, OutputNode

if TYPE_CHECKING:
    from collections.abc import Sequence

    from typing_extensions import Self


class OldNetwork:
    """Old network."""

    __slots__ = ("input_nodes", "output_nodes")

    def __init__(self) -> None:
        """Initialize network."""
        self.setup_layers()

    def setup_layers(self) -> None:
        """Initialize the layers for this network."""
        self.input_nodes = [
            InputNode("thirst"),
            InputNode("hunger"),
            InputNode("energy"),
            InputNode("shelter"),
            InputNode("food stash"),
            InputNode("water stash"),
        ]
        self.output_nodes = [
            OutputNode("drink"),
            OutputNode("eat"),
            OutputNode("sleep"),
            OutputNode("make shelter"),
            OutputNode("hunt"),
            OutputNode("scavenge"),
            OutputNode("find water"),
            OutputNode("relax"),
        ]
        for i in self.input_nodes:
            for o in self.output_nodes:
                i.outputs.append(o)
                o.inputs.append(i)
                w = random.randint(-10, 10)  # noqa: S311
                i.weights.append(w)
                o.weights.append(w)

    def assign_inputs(
        self,
        thirst: int = 0,
        hunger: int = 0,
        energy: int = 0,
        shelter: int = 0,
        food: int = 0,
        water: int = 0,
    ) -> None:
        """Assign input values to nodes."""
        self.input_nodes[0].value = thirst
        self.input_nodes[1].value = hunger
        self.input_nodes[2].value = energy
        self.input_nodes[3].value = shelter
        self.input_nodes[4].value = food
        self.input_nodes[5].value = water

    def print_information(self) -> None:
        """Print information about this network."""
        # for i in self.input_nodes:
        # print(f"{i.name} node\n\tValue:{i.get_value()}\n\tConnections:")
        # for index in range (len(i.outputs)):
        # print(f"\t\t{i.outputs[index].name}: {i.weights[index]}")
        for i in self.output_nodes:
            print(f"{i.name} node\n\tValue:{i.get_value()}\n\tConnections:")
            for index in range(len(i.inputs)):
                print(f"\t\t{i.inputs[index].name}: {i.weights[index]}")

    def propagate(self) -> None:
        """Propagate inputs through the network."""
        for node in self.output_nodes:
            node.value = 0
            for index in range(len(node.inputs)):
                node.value += (
                    node.inputs[index].get_value() * node.weights[index]
                )
            # print(f"{node.name} now has a value of {node.value}")

    def get_action(self) -> str:
        """Return the action name with the highest value."""
        action_node = max(
            self.output_nodes,
            key=lambda node: node.get_value(),
        )
        return action_node.name

    def copy(self) -> Self:
        """Return a deep copy of this network."""
        new_network = self.__class__()
        for i in range(len(new_network.input_nodes)):
            for j in range(len(new_network.input_nodes[i].weights)):
                new_network.input_nodes[i].weights[j] = self.input_nodes[
                    i
                ].weights[j]
        for i in range(len(new_network.output_nodes)):
            for j in range(len(new_network.output_nodes[i].weights)):
                new_network.output_nodes[i].weights[j] = self.output_nodes[
                    i
                ].weights[j]
        return new_network

    def mutate(self) -> None:
        """Mutate weights randomly *IN-PLACE*."""
        for node in self.output_nodes:
            for index in range(len(node.weights)):
                x = random.randint(1, 10)  # noqa: S311
                if x == 1 or x == 2:
                    # print(f"MUTATION! {best_survivor.name} changed {node.name} from {node.weights[index]} to ", end='')
                    node.weights[index] += 5
                    # print(node.weights[index])
                elif x == 3 or x == 4:
                    # print(f"MUTATION! {best_survivor.name} changed {node.name} from {node.weights[index]} to ", end='')
                    node.weights[index] -= 5
                    # print(node.weights[index])

    def get_hash(self) -> None:
        """Incomplete hash function."""
        for i in range(len(self.input_nodes)):
            for _j in range(len(self.input_nodes[i].weights)):
                raise NotImplementedError()


def test_old() -> None:
    """Run test of old network."""
    n = OldNetwork()
    # n.propagate()
    n.print_information()
    o = OldNetwork()
    o.print_information()
    print("\n\n\n")
    p = o.copy()
    p.print_information()


@dataclass(frozen=True, slots=True)
class Network(Generic[Number]):
    """Base network with feed forward and mutations."""

    layers: list[list[Node[Number]]]

    def feed_forward(self, inputs: list[Number]) -> list[Number]:
        """Return the output layer after feeding inputs through the network."""
        input_ = inputs
        for layer in self.layers:
            output = [node.get_value(input_) for node in layer]
            input_ = output
        return output

    def get_random_mutation_changes(self) -> list[tuple[int, int, int, int]]:
        """Return a random list of (layer, node, weight, weight delta) mutations."""
        # layer, node, weight, weight delta
        changes: list[tuple[int, int, int, int]] = []
        for layer_index, layer in enumerate(self.layers):
            for node_index, node in enumerate(layer):
                for weight_index in range(len(node.weights)):
                    x = random.randint(1, 10)  # noqa: S311
                    delta = 0
                    if x == 1 or x == 2:
                        delta = 5
                    elif x == 3 or x == 4:
                        delta = -5
                    if delta:
                        changes.append(
                            (layer_index, node_index, weight_index, delta),
                        )
        return changes

    def apply_mutations(
        self,
        mutations: list[tuple[int, int, int, int]],
    ) -> None:
        """Apply given mutations *IN PLACE*."""
        for layer_index, node_index, weight_index, delta in mutations:
            self.layers[layer_index][node_index].weights[weight_index] += delta

    def layers_copy(self) -> list[list[Node[Number]]]:
        """Return a deep copy of this network's layers."""
        return [[node.copy() for node in layer] for layer in self.layers]

    def copy(self) -> Self:
        """Return a deep copy of this network."""
        return self.__class__(self.layers_copy())

    def mutate(self) -> Self:
        """Return new version of network after potentially mutating weights.

        Randomly mutate the weights of all nodes in all layers.
        """
        mutations = self.get_random_mutation_changes()
        if not mutations:
            return self
        copy = self.copy()
        copy.apply_mutations(mutations)
        return copy


@dataclass(frozen=True, slots=True, repr=True)
class ActionNetwork(Network[Number], Generic[Number]):
    """Network with named inputs and named action outputs."""

    input_names: tuple[str, ...]
    action_names: tuple[str, ...]

    @staticmethod
    def setup_layers(
        input_names: Sequence[str],
        action_names: Sequence[str],
    ) -> list[list[Node[int]]]:
        """Return a new random simple network layers using action and input names."""
        layers = []
        output_layer = []
        for _action_name in action_names:
            weights = []
            for _input_name in input_names:
                weights.append(random.randint(-100, 100))  # noqa: S311
            node = Node(weights)
            output_layer.append(node)
        layers.append(output_layer)
        return layers

    @classmethod
    def new_network(
        cls,
        input_names: Sequence[str],
        action_names: Sequence[str],
    ) -> ActionNetwork[int]:
        """Initialize action network."""
        class_init = cast("type[ActionNetwork[int]]", cls)  # type: ignore[redundant-cast]
        return class_init(
            cls.setup_layers(input_names, action_names),
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
        return self.__class__(
            self.layers_copy(),
            self.input_names,
            self.action_names,
        )


def test() -> None:
    """Run action network test."""
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
        field_name: random.randint(0, 100)  # noqa: S311
        for field_name in input_fields
    }
    print(f"{input_values = }")
    print(f"{network.get_action_values(input_values) = }")
    print(f"{network.get_action(input_values) = }")


if __name__ == "__main__":
    test()
