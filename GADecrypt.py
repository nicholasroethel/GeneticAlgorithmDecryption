import nltk
import sklearn
import random
import numpy as np
from nltk.corpus import words
from random import sample
from Config import get_config, print_usage

import string
import random
def random_string(length):
  return convertToIntArray(''.join(random.choice(string.ascii_letters) for m in range(length)))

def genRandom(crib,n):
	wordlist = words.words()
	randString = ''


	while len(randString) < n: #keeps adding to randstring until its length n
		#print(len(randString))

		if ((len(randString)<1)  or (len(randString) > n-3)): #gets first part or resets to speed up probability of finding proper string length
			randString =  ''
			while(len(randString)<1):
				tmpword = random.choice(wordlist)
				if len(tmpword) < n:
					randString = tmpword

		tmpword = random.choice(wordlist)
		tmplen = len(tmpword)

		if (len(randString) + 1 + tmplen)<=n: #add to the string if possible
			randString = randString + ' ' + tmpword 

	return convertToIntArray(crib + " " + randString)

def evaluate(crib, item1):
  item2 = genRandom(crib,len(item1)-len(crib)-1)
  item3 = random_string(len(item1))

  cribArray = convertToIntArray(crib)

  realcor = sklearn.metrics.matthews_corrcoef(item1,item2)
  fakecor = sklearn.metrics.matthews_corrcoef(item1,item3)

  phiScore = abs(realcor) - abs(fakecor)
  hammingScore = np.sum(np.ones(len(crib))[cribArray==item1[:len(crib)]]) / len(crib)
  
  return phiScore + hammingScore

def crossover(item1,item2):
  crossoverPoint = random.randint(0,len(item1))
  return np.append(item1[:crossoverPoint],item2[crossoverPoint:]), np.append(item2[:crossoverPoint],item1[crossoverPoint:])

def mutate(item):
  randChar = ord(random.choice(string.ascii_letters))
  position = random.randint(0,len(item))
  item[position] = randChar
  
  return item

#I think we should work with Int arrays instead of strings here, makes the correlation calculation easier and probably the encryption
def convertToIntArray(item):
  return np.asarray([ord(c) for c in item])

def convertIntArrayToString(item):
  return ''.join([chr(i) for i in item])

def initPop(config):
  return [random_string(config.message_len) for i in range(config.pop_size)]

def main(config):
  population = initPop(config)
  fitnesses = [evaluate(config.crib, item) for item in population]

  item1 = genRandom("",10)
  item2 = genRandom("",10)
  print(item1,item2)
  print(convertIntArrayToString(item1), convertIntArrayToString(mutate(item1)))
  print(crossover(item1,item2))
  
  
if __name__== "__main__":
  config, unparsed = get_config()
  # If we have unparsed arguments, print usage and exit
  if len(unparsed) > 0:
      print_usage()
      exit(1)
  nltk.download('words')
  main(config)