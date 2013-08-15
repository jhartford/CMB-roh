import random

class Population:
	"""Population object to hold the MAP file and the people from the PED file"""
	def __init__(self, maps):
		self.maps = maps
		self.people = []
		

class Person:
	"""Person class contains all info from a line in a PED file"""
	def __init__(self, FID, IID, PatID, MatID, Sex, Pheno, map):
		self.FID = FID
		self.IID = IID
		self.PatID = PatID
		self.MatID = MatID
		self.Sex = Sex
		self.Pheno = Pheno
		self.SNP = []
		self.map = map

def parse_map(mapFile):
	'''
	Create hashtable with SNP id as key and the following value: 
	[snpnum,chromosome,Genetic distance,Base-pair position,base - e.g. 'A C' ]
	'''
	plink_map = {}
	snp_num = 0
	for line in mapFile:
		map_line = line.split("\t")
		plink_map[map_line[1]] = [snp_num, map_line[0],map_line[2],map_line[3],""] 
		snp_num = snp_num + 1
	return plink_map


def parse_ped(pedFile, map = {},debug = False):
	'''
	Parse PED files
	'''
	people = []
	count = 0
	for line in pedFile:
		ped_line = line.split("\t")
		p = Person(ped_line[0],ped_line[1],ped_line[2],ped_line[3],ped_line[4],ped_line[5],map)
		p.SNP = ped_line[6:]
		p.SNP[-1] = p.SNP[-1][0:-1]					#remove the \n from the last element
		people.append(p)
		if debug:
			print(count)
		count = count+1
		if count == 2:
			break
	return people

def sample_base(basepair):
		if random.randint(0,1) == 1:
			return(basepair[0])
		else:
			return(basepair[3])


def make_child(mother,father,id="SYNTH"):
	mother_snps = set(mother.map.keys())
	father_snps = set(father.map.keys())
	common_snps = mother_snps.intersection(father_snps)
	synth_person = Person(mother.FID,id,father.IID,mother.IID,random.randint(0,1),0,{})
	for snp in common_snps:
		mother_snp_map = mother.map[snp]
		father_snp_map = father.map[snp]


	return(synth_person)

p = open("khoisan_clean_ped.ped")
m = open("khoisan_clean_ped.map")
b = open("bray.map")

m_map = parse_map(m)
b_map = parse_map(b)
pop1 = Population(m_map)
pop1.people = parse_ped(p,pop1.maps)

child = make_child(pop1.people[0],pop1.people[1])
#print(child.map['rs7987820'])

com = list(set(m_map.keys()).intersection(set(b_map.keys())))
print(m_map[com[1]])
print(b_map[com[1]])

m.close()
p.close()
b.close()


test = {"t":1,"a":2,"f":3}
test2 = {"t":1,"a":2,"f":3,"d":"Dasdf","fds":"hello"}
inter = set(test2.keys()).intersection(set(test.keys()))