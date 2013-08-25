class Person:
	"""Person class contains all info from a line in a PED file and a reference to the population map (which lists all)
	SNPs in that the person has"""
	def __init__(self, FID, IID, PatID, MatID, Sex, Pheno, population):
		self.FID = FID
		self.IID = IID
		self.PatID = PatID
		self.MatID = MatID
		self.Sex = Sex
		self.Pheno = Pheno
		self.SNP = []
		self.population = population
		self.binSNP = []
		self.runs = []

	def inc_array(self,array, start, end):
		'''
		method to increment a subset of an array
		'''
		for i in xrange(start,end):
			array[i] = array[i] + 1
		return(array)

	def detect_roh(self, widowsnp = 50, windowthreshold = 0.1, scorethreshold = 0.95):
		if len(self.binSNP)==0:
			self.convert_snp_to_binary()
		score = [0]*len(self.binSNP)
		#print(self.population.maparray)
		runs_of_homozygosity = []
		distances = []
		for i in xrange(0, len(self.binSNP) - widowsnp):
			window = self.binSNP[i:i+widowsnp]
			if float(sum(window))/len(window) >= (1-windowthreshold):
				score = self.inc_array(score,i,i+widowsnp)
		score = [float(j)/widowsnp for j in score]
	
		run_length_in_snps = 0
		for i in xrange(0,len(score)):
			curr_score = score[i]
			if curr_score>scorethreshold:
				run_length_in_snps = run_length_in_snps+1
				#detect run length
			else:
				if run_length_in_snps!=0:
					runs_of_homozygosity.append([run_length_in_snps,abs(self.population.maparray[i] - self.population.maparray[i-run_length_in_snps])])
				run_length_in_snps = 0
		#print(distances)
		self.runs = runs_of_homozygosity

	def convert_snp_to_binary(self):
		if len(self.binSNP) != len(self.SNP):
			for snp in self.SNP:
				self.binSNP.append(int(snp[0]==snp[2]))

	def print_binSNP_to_file(self,file):
		if len(self.binSNP)==0:
			self.convert_snp_to_binary()
		for i in xrange(0,len(self.binSNP)):
			file.write(str(self.binSNP[i]) + "\t" + str(self.population.maparray[i])) 

	def print_runs_to_file(self,file):
		for i in xrange(0,len(self.runs)):
			file.write(self.FID+"\t"+self.IID+"\t"+str(self.runs[i][0])+"\t"+str(self.runs[i][1])+"\n") 
			