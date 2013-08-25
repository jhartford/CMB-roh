import random
import person

class Population:
	"""Population object to hold the MAP file and the people from the PED file"""
	def __init__(self, map = {}):
		self.map = map
		self.maparray = []
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
			self.maparray.append(int(map_line[3]))
			plink_map[map_line[1]] = [snp_num, map_line[0],map_line[2],map_line[3],""] 
			snp_num = snp_num + 1
		self.map = plink_map
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
			p = person.Person(ped_line[0],ped_line[1],ped_line[2],ped_line[3],ped_line[4],ped_line[5],self)
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