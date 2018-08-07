"""
        Password genetic algorithm development
        Made by: Tiago Antunes
"""
import random


print("How it works:")
print("Time goes by using generations. Each generation has 1000 elements and they're the base for the next generation")
print("Only 50 of a generation survive. The bigger the score, the more chances they have to survive. Populations have a size of 1000")
print("Each Citizen that is breed has some random mutations to avoid staying at a local minimum and not evolving")
print("Each element is a text that is similar to DNA. You type in a lowercase text which is the objective")
print("Generation 0 is totally random!")
password = input("To start, type in the target: ") #this is the target password that the program must adapt to


class Citizen:
    """ Citizen class of our evolution  """
    def __init__(self, generation, content):
        self.generation = generation
        self.content = content
        self.score = 0
        self.survival = 0

    def __repr__(self):
        return self.content


def createGeneration(n, generation):
    """ Creates the a population of size n """
    pop = []
    i = 0
    while i < n:
        t = ''
        for j in range(len(password)):
            t += chr(96 + random.randint(1,26))
        pop.append(Citizen(generation, t))
        i+=1
    return pop

def getScore(citizen):
    """ Gets the score of an individual citizen """
    score = 0
    for l in range(len(password)):
        if citizen.content[l] == password[l]:
            score += 1
    return int(score * 100 / len(password))



def updateScores(population):
    """ Updates all the scores of the population """
    for cit in population:
        cit.score = getScore(cit)


def breed(mom, dad, gen):
    """ Generates a new Citizen, as a combination of his parents"""
    content = ''
    for l in range(len(mom.content)):
        text = (mom.content[l] if random.random() > 0.5 else dad.content[l]) if random.random() * (mom.score + dad.score)/200 < 0.7 else chr(96 + random.randint(1,26))
        content += text
    return Citizen(gen, content)



def getSurvivors(pop, k):
    """ Selects the population that will survive for the next gen """
    for l in pop:
        l.survival = l.score * random.random() #the bigger the score, the bigger the survival
    
    return sorted(pop, key=lambda x: x.survival)[-k:]


def newGeneration(population, gen, k, n):
    """ Creates the new generation of the race """
    newPopulation = getSurvivors(population, k)
    i = k
    while i < n:
        a,b = random.randint(0,k-1), random.randint(0,k-1)
        if a == b:
            continue
        newPopulation.append(breed(newPopulation[a], newPopulation[b], gen))
        i += 1
    return newPopulation

def perfection(pop):
    """ Goes through the population to find if there is a Citizen that reached the objective """
    for i in pop[::-1]:
        if i.content == password:
            print(pop)
            print('Found it! Generation:', i.generation)
            return True
    return False


def main():
    population = createGeneration(1000,0) #creates first generation
    generation = 0
    while not perfection(population): #until target not reached
        generation += 1
        population = newGeneration(population, generation, 50, 1000) #only survive 50, target population is 1000
        updateScores(population) #attribute scores to each element
        population.sort(key=lambda x: x.score) 
        print('Currently in generation',generation, 'and best score is', population[-1].score, 'with word', population[-1].content)


main()