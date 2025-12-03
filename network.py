from nodes import inputNode
from nodes import outputNode
import random
class Network:
    def __init__(self):
        tNode = inputNode("thirst")
        hNode = inputNode("hunger")
        eNode = inputNode("energy")
        sNode = inputNode("shelter")
        fNode = inputNode("food stash")
        wNode = inputNode("water stash")
        drinkNode = outputNode("drink")
        eatNode = outputNode("eat")
        sleepNode = outputNode("sleep")
        shelterNode = outputNode("make shelter")
        nothingNode = outputNode("relax")
        huntNode = outputNode("hunt")
        scavengeNode = outputNode("scavenge")
        findWaterNode = outputNode("find water")
        self.inputNodes = [tNode,hNode,eNode,sNode,fNode,wNode]
        self.outputNodes = [drinkNode,eatNode,sleepNode,shelterNode,huntNode,scavengeNode,findWaterNode,nothingNode]
        for i in self.inputNodes:
            i.value = random.randint(0, 100)
            for o in self.outputNodes:
                i.outputs.append(o)
                o.inputs.append(i)
                w = random.randint(-10, 10)
                i.weights.append(w)
                o.weights.append(w)


    def assignInputs(self, thirst=0,hunger=0,energy=0,shelter=0,food=0,water=0):
        self.inputNodes[0].value = thirst
        self.inputNodes[1].value = hunger
        self.inputNodes[2].value = energy
        self.inputNodes[3].value = shelter
        self.inputNodes[4].value = food
        self.inputNodes[5].value = water

    def printToConsole(self):
        #for i in self.inputNodes:
            #print(f"{i.name} node\n\tValue:{i.getValue()}\n\tConnections:")
            #for index in range (len(i.outputs)):
                #print(f"\t\t{i.outputs[index].name}: {i.weights[index]}")
        for i in self.outputNodes:
            print(f"{i.name} node\n\tValue:{i.getValue()}\n\tConnections:")
            for index in range (len(i.inputs)):
                print(f"\t\t{i.inputs[index].name}: {i.weights[index]}")

    def propagate(self):
        for node in self.outputNodes:
            node.value = 0
            for index in range(len(node.inputs)):
                node.value += node.inputs[index].getValue() * node.weights[index]
            #print(f"{node.name} now has a value of {node.value}")

    def getAction(self):
        highestValue = -1000000
        action = ""
        for outputNode in self.outputNodes:
            if outputNode.getValue() > highestValue:
                highestValue = outputNode.getValue()
                action = outputNode.name
        return action

    def copyNetwork(self):
        newNetwork = Network()
        for i in range(len(newNetwork.inputNodes)):
            for j in range(len(newNetwork.inputNodes[i].weights)):
                newNetwork.inputNodes[i].weights[j] = self.inputNodes[i].weights[j]
        for i in range(len(newNetwork.outputNodes)):
            for j in range(len(newNetwork.outputNodes[i].weights)):
                newNetwork.outputNodes[i].weights[j] = self.outputNodes[i].weights[j]
        return newNetwork

    def mutate(self):
        pass

    def getHash(self):
        num = 0
        pow = 0
        for i in range(len(self.inputNodes)):
            for j in range(len(self.inputNodes[i].weights)):
                pass

if __name__=="__main__":    
    n = Network()
    #n.propagate()
    n.printToConsole()
    o = Network()
    o.printToConsole()
    print("\n\n\n")
    p = o.copyNetwork()
    p.printToConsole()