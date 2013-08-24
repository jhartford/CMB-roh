'''
Script takes two inputs - the filenames of the two populations from which you want to sythesize
a new person. Currently it only outputs one person but it would be easy to modify it to output many
people....
'''

import random
import copy
import sys

class Population:
	"""Population object to hold the MAP file and the people from the PED file"""
	def __init__(self, maps = {}):
		self.maps = maps
		self.people = []

	def parse_map(self,filename):
		'''
		Create hashtable with SNP id as key and the following value: 
		[snpnum,chromosome,Genetic distance,Base-pair position,base - e.g. 'A C' ]
		'''
		mapFile = open(filename + ".map")
		plink_map = {}
		snp_num = 0
		for line in mapFile:
			map_line = line.split("\t")
			plink_map[map_line[1]] = [snp_num, map_line[0],map_line[2],map_line[3],""] 
			snp_num = snp_num + 1
		self.maps = plink_map
		mapFile.close()
	

	def parse_ped(self,filename,debug = False):
		'''
		Parse PED files
		'''
		pedFile = open(filename + ".ped")
		people = []
		count = 0
		print(pedFile)
		for line in pedFile:
			ped_line = line.split("\t")
			p = Person(ped_line[0],ped_line[1],ped_line[2],ped_line[3],ped_line[4],ped_line[5],self.maps)
			p.SNP = ped_line[6:]
			p.SNP[-1] = p.SNP[-1][0:-1]					#remove the \n from the last element
			people.append(p)
			if debug:
				print(count)
			count = count+1
			if count == 2:
				break
		self.people = people
		pedFile.close()
		
class Person:
	"""Person class contains all info from a line in a PED file and a reference to the population map (which lists all)
	SNPs in that the person has"""
	def __init__(self, FID, IID, PatID, MatID, Sex, Pheno, map):
		self.FID = FID
		self.IID = IID
		self.PatID = PatID
		self.MatID = MatID
		self.Sex = Sex
		self.Pheno = Pheno
		self.SNP = []
		self.map = map
		self.binSNP = []

	def convert_snp_to_binary(self):
		if len(self.binSNP) != len(self.SNP):
			for snp in self.SNP:
				self.binSNP.append(int(snp[0]==snp[2]))
		

def sample_base(basepair):
	'''
	Takes a base pair (e.g. 'A T') and returns one of the bases at random
	'''
	if random.randint(0,1) == 1:
		return(basepair[0])
	else:
		return(basepair[2])

def make_child(mother,father,id="SYNTH"):
	'''
	Takes two Person objects as input and creates a new Person object that is a synthesis of their common SNPs
	For each common SNP, the new base pair is made up of a random selection of one of the bases from the mother 
	and one from the father (sex is irrelavent for this method - mother and father are just used for illustration)
	'''
	mother_snps = set(mother.map.keys())
	father_snps = set(father.map.keys())
	common_snps = mother_snps.intersection(father_snps)
	synth_person = Person(mother.FID,id,str(father.FID)+"_"+str(father.IID),\
		str(mother.FID)+"_"+str(mother.IID),random.randint(0,1),0,{})
	for snp in common_snps:
		mother_bp_location = mother.map[snp][0]
		father_bp_location = father.map[snp][0]
		new_basepair = sample_base(mother.SNP[mother_bp_location]) +' '+ sample_base(father.SNP[father_bp_location])
		synth_person.map[snp] = copy.deepcopy(mother.map[snp])
		synth_person.map[snp][4] = new_basepair

	return(synth_person)

def person_to_file(pedfile, mapfile, person):
	'''
	Takes two open files and a Person object as input and writes the person's data to 
	PED and MAP files.
	'''
	pedfile.write(str(person.FID)+"\t"+str(person.IID)+"\t"+\
		str(person.PatID)+"\t"+str(person.MatID)+"\t"+\
		str(person.Sex)+"\t"+str(person.Pheno))
	for bp in person.map:
		pedfile.write("\t"+person.map[bp][4])
		mapfile.write(bp+'\t'+'\t'.join(map(str,person.map[bp][0:3])) + '\n')
	pedfile.write("\n")

############################################################################################
########################	READ PED AND MAP FILES #########################################
############################################################################################

print("Parsing file 1")
pop1 = Population()
pop1.parse_map(str(sys.argv[1]))
pop1.parse_ped(str(sys.argv[1]))
pop1.people[0].convert_snp_to_binary()

'''
snp_matches = open("bin.txt","w")
for i in pop1.people[0].binSNP:
	snp_matches.write(str(i))
snp_matches.close()
'''

print("Parsing file 2")
pop2 = Population()
pop2.parse_map(str(sys.argv[2]))
pop2.parse_ped(str(sys.argv[2]))

print("Combining files")

person1 = random.randint(0,len(pop1.people)-1)
print(str(len(pop1.people))+" - " + str(person1))
person2 = random.randint(0,len(pop2.people)-1)
print(str(len(pop2.people))+" - " + str(person2))
#Create a child out of one random person from each population:
child = make_child(pop1.people[person1],pop2.people[person2])


############################################################################################
########################	WRITE PED AND MAP FILES ########################################
############################################################################################

print("Writing files to disk")
filename = "test-out"
output_pedfile = open(filename+".ped","w")
output_mapfile = open(filename+".map","w")
person_to_file(output_pedfile,output_mapfile,child)
output_pedfile.close()
output_mapfile.close()