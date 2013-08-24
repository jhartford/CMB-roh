rohfile = open("dummy.txt")
debug = False
error_rate = 0
source = []
simprun = ""
for line in rohfile:
	simprun = simprun+line[0]
	source.append(int(line[0]))

print("String:"),
print(source)
roh = [-1]*len(source)
part_of_run = [False]*len(source)





def left(runs,error_rate):
	print(runs)
	if (1-float(sum(runs))/len(runs)) <= error_rate:
		return [len(runs)]
	elif len(runs)>1:
		return left(runs[:-1],error_rate) + right(runs[1:],error_rate)
	else:
		return []

def right(runs,error_rate):
	print(runs)
	if (1-float(sum(runs))/len(runs)) <= error_rate:
		return [len(runs)]
	elif len(runs)>1:
		return right(runs[1:],error_rate)
	else:
		return []

def recursiveruns(runs,error_rate):
	out = left(runs[:-1],error_rate) + right(runs[1:],error_rate)
	print("output:"),
	print(out)


def recursion2(runs,error_rate, maxroh):
	for i in range(0, len(runs)-windowsize+1):
		window = runs[i:(windowsize)]
		window_error = 1-float(sum(window))/len(window)
		if window_error <= error_rate:
			recursion2

def windowrun(runs):
	roh = [-1]*len(runs)
	roh_list = []
	for windowsize in range(len(runs), 1, -1):
		#print(windowsize),
		#print(": %.30f" % (sum(map(float,part_of_run))/len(part_of_run)))
		if sum(map(float,part_of_run))/len(part_of_run) == 1:
			break
		#if windowsize%1000 == 0:
		#	print(windowsize)
		for jump in range(0,1+ len(runs)-windowsize):
			if (part_of_run[jump]):
				continue
			window = runs[(jump):(windowsize+jump)]
			window_error = 1-float(sum(window))/len(window)
			if window_error <= error_rate:
				if roh[jump]==-1:
					#print(runs[0:jump])				# only enter the run if there is not already a value there (the value will be larger because the loop runs in reverse)
					#print(runs[(jump):(jump+windowsize)])
					#print(runs[(jump+windowsize+1):])
					#print(len(roh))
					#print(windowsize)
					#print(jump)
					#roh = roh[:(jump-1)] + [windowsize] + roh[(jump+windowsize):]
					#print(roh)
					#roh[jump]= windowsize
					#print("found:"+str(windowsize))
					for i in range(jump,windowsize+jump):
						part_of_run[i] = True
					roh_list.append(windowsize)
			if debug:
				print("window size:"+str(windowsize)),
				print("jump size:"+str(jump)),
				print("error:"+str(window_error)),
				print(str(len(window))+" - "+str(window)+"\n")
		#if windowsize<(len(runs) - 10):
	return(roh_list)
	#		break
#print(map(len,simprun.split("0")))
#print(runs)
#print(roh)
#print(source)
print(windowrun(source))

#recursiveruns(source,0)