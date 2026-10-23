from network import Network
import random
MAX_HEALTH = 100
MAX_HUNGER = 100
MAX_THIRST = 100
MAX_SLEEP = 100
class Survivor:

    def __init__(self):
        global MAX_THIRST
        global MAX_HEALTH
        global MAX_SLEEP
        global MAX_HUNGER
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

#s1 = Survivor()
#s2 = Survivor()
#s1.name="Alice"
#s2.name = "Bob"
#s = [s1, s2]
#for t in range(200):
    #for person in s:
        #if person.alive:
            #person.advanceTime()
            #person.printToConsole()
