import sys
import population
import person
import synthesize	

'''
Script takes two inputs - the filenames of the two populations from which you want to sythesize
a new person. Currently it only outputs one person but it would be easy to modify it to output many
people....
'''	

############################################################################################
########################	READ PED AND MAP FILES #########################################
############################################################################################

def parse_ped_to_roh(population,filename,rohfile,debug = False):
	'''
	Parse PED files 1 line at a time. PED files tend to have a lot of individuals so unless one needs all the individuals in
	memory, it is preferable to read only those individuals which are required into to population.

	This method overwrites Person objects in the population
	'''
	pedFile = open(filename + ".ped")
	people = []
	count = 0
	line1 = True
	print(pedFile)
	for line in pedFile:
		ped_line = line.split("\t")
		if line1:
			p = person.Person(ped_line[0],ped_line[1],ped_line[2],ped_line[3],ped_line[4],ped_line[5],population)
			p.SNP = ped_line[6:]
			p.SNP[-1] = p.SNP[-1][0:-1]					#remove the \n from the last element
			line1 = False
		else:
			p.FID = ped_line[0]
			p.IID = ped_line[1]
			p.PatID = ped_line[2]
			p.MatID = ped_line[3]
			p.Sex = ped_line[4]
			p.Pheno = ped_line[5]
			p.SNP = ped_line[6:]
			p.SNP[-1] = p.SNP[-1][0:-1]					#remove the \n from the last element
		population.people = [p]
		p.detect_roh(widowsnp = 50, windowthreshold = 0.1, scorethreshold = 0.95)
		p.print_runs_to_file(rohfile)
		if debug:
			print(count)
		count = count+1

	pedFile.close()

filein = sys.argv[1]

print("Parsing file 1")
output_roh = open("roh1.txt","w")
pop1 = population.Population()
pop1.parse_map(str(filein))
#pop1.parse_ped(str(filein))
parse_ped_to_roh(pop1,filein,output_roh, True)
output_roh.close()
#synth = synthesize.Synthesize([pop1.people[0],pop1.people[1]])
#print(len(synth.map))
#synth.breed(True)
#print(synth.children[0].population.map)
'''
pop1.people[0].convert_snp_to_binary()
output_binfile = open("test.ped","w")
pop1.people[0].print_binSNP_to_file(output_binfile)
output_binfile.close()
pop1.people[0].detect_roh()
output_roh = open("roh.txt","w")
pop1.people[0].print_runs_to_file(output_roh)
output_roh.close()
#for run in pop1.people[0].runs:
#	print(run)
#print(pop1.people[0].runs)

#print(pop1.people[0].binSNP)

'''
'''
snp_matches = open("bin.txt","w")
for i in pop1.people[0].binSNP:
	snp_matches.write(str(i))
snp_matches.close()
'''
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

'''
############################################################################################
########################	WRITE PED AND MAP FILES ########################################
############################################################################################
'''
print("Writing files to disk")
filename = "test-out"
output_pedfile = open(filename+".ped","w")
output_mapfile = open(filename+".map","w")
person_to_file(output_pedfile,output_mapfile,child)
output_pedfile.close()
output_mapfile.close()
'''
