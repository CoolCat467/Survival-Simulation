from survivor import Survivor
import random
def pickBest(people: list, fraction):
    sortedList = sorted(people, key=lambda person: person.calculateFitness(),reverse=True)
    returnList = []
    for i in range(len(sortedList) // fraction):
        for j in range(fraction):
            copyPerson = sortedList[i]
            child = Survivor()
            child.name = copyPerson.name
            child.network = copyPerson.cloneNetwork()
            returnList.append(child)
    return returnList

#INEFFICIENT...JUST USE PICK BEST
def generateNewPopulation(people):
    newPeople = pickBest(people, 2)
    return newPeople

def survivalTrial(people, maxTime):
    for t in range(maxTime):
        for person in people:
            if person.alive:
                person.advanceTime()

def mutate(p: Survivor):
    for node in p.network.outputNodes:
        for index in range(len(node.weights)):
            x = random.randint(1, 10)
            if x == 1 or x == 2:
                #print(f"MUTATION! {p.name} changed {node.name} from {node.weights[index]} to ", end='')
                node.weights[index] += 5
                #print(node.weights[index])
            elif x == 3 or x == 4:
                #print(f"MUTATION! {p.name} changed {node.name} from {node.weights[index]} to ", end='')
                node.weights[index] -= 5
                #print(node.weights[index])
def initializePopulation():
    numPeople = 100
    people = []
    for i in range(numPeople):
        s = Survivor()
        s.name = "Subject " + str(i)
        people.append(s)    
    return people

def printCurrentResults(people):
    for p in people:
        print(f"{p.name}: {p.calculateFitness()} - alive for {p.age} and current health of {p.health}")

def printCurrentBest(people, num):
    tempList = sorted(people, key=lambda person: person.calculateFitness(), reverse=True)
    for p in range(num):
        print(f"{tempList[p].name}: {tempList[p].calculateFitness()} - alive for {tempList[p].age} and current health of {tempList[p].health}")

def getCurrentHigh(people):
    high = 0
    person = None
    for p in people:
        if p.calculateFitness() > high:
            high = p.calculateFitness()
            person = p
    return high, person

def geneticAlgorithm():
    maxGenerations = 1000
    #randomly initialize population
    #determine fitness of population
    #repeat
        #select parents from population
        #generate new population
        #perform mutation on new population
        #calculate fitness on new population

    #randomly initialize population
    survivorList = initializePopulation()
    highScore = 0
    for generation in range(maxGenerations):
        #print(f"**********\nGENERATION {generation}\n**********\n")
        survivalTrial(survivorList, 200)
        #printCurrentResults(survivorList)
        #printCurrentBest(survivorList, 3)
        h,p = getCurrentHigh(survivorList)
        
        if h > highScore:
            print(f"New high value of {h} in generation {generation}")
            highScore = h
        else:
            pass
            #print(f"Current high: {getCurrentHigh(survivorList)[0]}, generation: {generation}")
        survivorList = generateNewPopulation(survivorList)
        for person in survivorList:
            mutate(person)
    return p

stud=geneticAlgorithm()


subject = Survivor()
subject.name = stud.name
subject.network = stud.cloneNetwork()
for t in range(200):
    if subject.alive:
        subject.advanceTime(True)
        subject.printToConsole()   #person.advanceTime()
            #person.printToConsole()