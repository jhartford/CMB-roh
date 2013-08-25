import copy
import random
import person as p
import population as pop

class Synthesize:
	"""Synthesize class combines multiple people to sythesize individuals"""
	def __init__(self, people):
		self.people = people
		self.map = self.get_common_maps(people)
		self.children = []

	def breed(self, debug = False):
		children = []
		people = self.people
		synthpop = pop.Population()
		for i in xrange(0, len(self.people)/2):
			if (debug):
				print("Making child "+str(i) + " out of person:"+str(2*i) + "  and person:" + str(2*i+1))
			children.append(self.make_child(people[2*i],people[2*i+1],synthpop))
		self.children = children

	def get_common_maps(self, people):
		common = set(people[0].population.map.keys())
		for person in people:
			common = common.intersection(set(person.population.map.keys()))
		return(common)

	def make_child(self,mother,father,synth_population,id="SYNTH"):
		'''
		Takes two Person objects as input and creates a new Person object that is a synthesis of their common SNPs
		For each common SNP, the new base pair is made up of a random selection of one of the bases from the mother 
		and one from the father (sex is irrelavent for this method - mother and father are just used for illustration)
		'''
		common_snps = self.map
		synth_person = p.Person(mother.FID,id,str(father.FID)+"_"+str(father.IID),\
			str(mother.FID)+"_"+str(mother.IID),random.randint(0,1),0,synth_population)
		synth_person.population.map = copy.deepcopy(mother.population.map)
		for snp in common_snps:
			mother_bp_location = mother.population.map[snp][0]
			father_bp_location = father.population.map[snp][0]
			new_basepair = self.sample_base(mother.SNP[mother_bp_location]) +' '+ self.sample_base(father.SNP[father_bp_location])
			#synth_person.population.map[snp] = mother.population.map[snp]
			synth_person.population.map[snp][4] = new_basepair

		return(synth_person)

	def sample_base(self,basepair):
		'''
		Takes a base pair (e.g. 'A T') and returns one of the bases at random
		'''
		if random.randint(0,1) == 1:
			return(basepair[0])
		else:
			return(basepair[2])

	def children_to_file(self,pedfile, mapfile):
		'''
		Takes two open files and a Person object as input and writes the person's data to 
		PED and MAP files.
		'''
		for person in self.children:
			pedfile.write(str(person.FID)+"\t"+str(person.IID)+"\t"+\
				str(person.PatID)+"\t"+str(person.MatID)+"\t"+\
				str(person.Sex)+"\t"+str(person.Pheno))
			for bp in person.population.map:
				pedfile.write("\t"+person.population.map[bp][4])
				mapfile.write(bp+'\t'+'\t'.join(map(str,person.population.map[bp][0:3])) + '\n')
			pedfile.write("\n")