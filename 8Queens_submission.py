import numpy as np
import sys




class BoardPosition:
	def __init__(self):
		self.sequence = None
		self.score = None
		self.survival = None
	def setSequence(self, val):
		self.sequence = val
	def setScore(self, score):
		self.score = score
	def setSurvival(self, val):
		self.survival = val
	nQueens = 8
	STOP_CTR = 28
	MUTATE = 0.000001
	MUTATE_FLAG = True
	MAX_ITER = 100000
	POPULATION = None
		
def score(chromosome = None):
	clashes = 0;
	row_col_clashes = abs(len(chromosome) - len(np.unique(chromosome)))
	clashes += row_col_clashes

	# calculate diagonal clashes
	for i in range(len(chromosome)):
		for j in range(len(chromosome)):
			if ( i != j):
				dx = abs(i-j)
				dy = abs(chromosome[i] - chromosome[j])
				if(dx == dy):
					clashes += 1


	return 28 - clashes	


def generate_child():
	# randomly generates a sequence of board states.
	#global nQueens
	init_distribution = np.arange(BoardPosition.nQueens)
	np.random.shuffle(init_distribution)
	return init_distribution

def generate_intial_population(population_size = 100):
	global POPULATION

	POPULATION = population_size

	population = [BoardPosition() for i in range(population_size)]
	for i in range(population_size):
		population[i].setSequence(generate_child())
		population[i].setScore(score(population[i].sequence))

	return population


def get_parent():
	globals()	
	parent1, parent2 = None, None
	# parent is decided by random probability of survival.
	# since the fitness of each board position is an integer >0, 
	# we need to normaliza the fitness in order to find the solution
	
	summation_fitness = np.sum([x.score for x in population])
	for each in population:
		each.survival = each.score/(summation_fitness*1.0)

	while True:
		parent1_random = np.random.rand()
		parent1_rn = [x for x in population if x.survival <= parent1_random]
		try:
			parent1 = parent1_rn[0]
			break
		except:
			pass

	while True:
		parent2_random = np.random.rand()
		parent2_rn = [x for x in population if x.survival <= parent2_random]
		try:
			t = np.random.randint(len(parent2_rn))
			parent2 = parent2_rn[t]
			if parent2 != parent1:
				break
			else:
				continue
		except:
			continue

	if parent1 is not None and parent2 is not None:
		return parent1, parent2
	else:
		sys.exit(-1)

def reproduce_crossover(parent1, parent2):
	globals()
	n = len(parent1.sequence)
	c = np.random.randint(n, size=1)
	child = BoardPosition()
	child.sequence = []
	child.sequence.extend(parent1.sequence[0:c])
	child.sequence.extend(parent2.sequence[c:])
	child.setScore(score(child.sequence))
	return child


def mutate(child):
	if child.survival < BoardPosition.MUTATE:
		c = np.random.randint(8)
		child.sequence[c] = np.random.randint(8)
	return child

def GA(iteration):
	globals()
	newpopulation = []
	for i in range(len(population)):
		parent1, parent2 = get_parent()
		# print "Parents generated : ", parent1, parent2

		child = reproduce_crossover(parent1, parent2)

		if(BoardPosition.MUTATE_FLAG):
			child = mutate(child)

		newpopulation.append(child)
	return newpopulation


def stop():
	globals()
	fitnessvals = [pos.score for pos in population]
	if BoardPosition.STOP_CTR in fitnessvals:
		return True
	if BoardPosition.MAX_ITER == iteration:
		return True
	return False



def right_sequence():
        population = generate_intial_population(1000)                
        iteration = 0;
        while not stop():
        	# keep iteratin till  you find the best position
        	population = GA(iteration)
        	iteration +=1   
        generatedseq = []
        for each in population:
        	if each.score == 28:
        		generatedseq.append(each)
        if len(generatedseq) > 0:
            print(f"Generated Sequence Of Queens:",str(generatedseq[0].sequence).replace("[","").replace("]",""))
            #print(f"Generated score for the sequence:",generatedseq[0].score)

right_sequence()