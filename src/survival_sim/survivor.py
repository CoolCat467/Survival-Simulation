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
from survival_sim.network import Network


class Survivor:

    MAX_HEALTH = 100
    MAX_HUNGER = 100
    MAX_THIRST = 100
    MAX_SLEEP = 100

    def __init__(self):
        self.thirst = MAX_THIRST
        self.hunger = MAX_HUNGER
        self.sleep = MAX_SLEEP
        self.health = MAX_HEALTH
        self.foodStash = 0
        self.waterStash = 0
        self.shelter = 0
        self.alive = True
        self.name = ""
        self.age = 0
        self.network = Network()

    def eat(self):
        if self.foodStash > 0:
            self.foodStash -= 1
            if self.hunger < 90:
                self.hunger += 10
            if self.hunger > 80 and self.health < 95:
                self.health += 2

    def drink(self):
        if self.waterStash > 0:
            self.waterStash -= 1
            if self.thirst < 92:
                self.thirst += 8
            if self.thirst > 80 and self.health < 95:
                self.health += 2
    
    def goToBed(self):
        self.sleep = min(100, self.sleep + 10)

    def makeShelter(self):
        if self.shelter < 40:
            self.shelter += 15
        elif self.shelter < 80:
            self.shelter += 10
        elif self.shelter < 95:
            self.shelter -= 5
        self.sleep -= 5

    def scavenge(self):
        chance = random.randint(1, 6)
        self.sleep -= 3
        if chance < 5:
            self.foodStash += 1

    def hunt(self):
        chance = random.randint(1, 6)
        self.sleep -= 8
        if chance < 3:
            self.foodStash += 3

    def findWater(self):
        chance = random.randint(1, 6)
        self.sleep -= 2
        if chance < 5:
            self.waterStash += 1
        elif chance < 6:
            self.waterStash += 3

    def advanceTime(self, printing=False):
        #get hungrier, get thirstier, lose energy
        self.hunger = max(self.hunger-3, 0)
        self.thirst = max(self.thirst-3, 0)
        self.age += 1

        if self.shelter < 20:
            self.sleep -= 5
        elif self.shelter < 40:
            self.sleep -= 3
        elif self.shelter < 60:
            self.sleep -= 1

        self.sleep = max(self.sleep-2, 0)
        if self.hunger < 20 or self.thirst < 20 or self.sleep < 20:
            self.health -= 1
        if self.health <= 0:
            self.alive = False
        if not self.alive:
            #print(f"{self.name} just died")
            return
        self.makeDecision(printing)

    def makeDecision(self,printing=False):
        self.network.assignInputs(self.thirst, self.hunger, self.sleep, self.shelter, self.foodStash, self.waterStash)
        self.network.propagate()
        x = self.network.getAction()
        if x == "drink":
            self.drink()
        elif x == "eat":
            self.eat()
        elif x == "sleep":
            self.goToBed()
        elif x == "make shelter":
            self.makeShelter()
        elif x == "hunt":
            self.hunt()
        elif x == "scavenge":
            self.scavenge()
        elif x == "find water":
            self.findWater()
        if printing:
            print(f"{self.name} just did the {x} action")
    def calculateFitness(self):
        return self.age + self.health
    
    def cloneNetwork(self):
        return self.network.copyNetwork()
    
    def printToConsole(self):
        print(f"{self.name} Hour {self.age}:\tHealth: {self.health}, Hunger: {self.hunger}, Thirst: {self.thirst}, Energy: {self.sleep}, Shelter: {self.shelter}\n")

