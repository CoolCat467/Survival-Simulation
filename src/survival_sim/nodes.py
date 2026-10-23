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


class inputNode:
    def __init__(self, n):
        self.outputs = []  # list of nodes
        self.weights = []  # list of weights
        self.value = 0
        self.name = n

    def setValue(self, v):
        self.value = v

    def getValue(self):
        return self.value


class outputNode:
    def __init__(self, n):
        self.inputs = []
        self.weights = []
        self.value = 0
        self.name = n

    def getValue(self):
        return self.value
