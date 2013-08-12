#!/bin/bash
#Randomly join two individuals

#Function to randomly select one of the two base pairs for each line and return a tempoary file called INPUT2.ped
function randomsub { 
	RANDOM=$$  # Reseed the random number generator using script process ID.
	#RANDOM=1000  #Use this option if you'd rather fix the seed
	cat $1 | tr '\t' '\n' > temp1.ped
	tail -n +7 temp1.ped > temp2.ped
	rm temp1.ped
	cat temp2.ped | awk -v seed=$RANDOM 'BEGIN{srand(seed);}{test = rand(); if (test<0.5) print $1; else print $2; }' > $2'.ped'
}

randomsub $1 sub1
randomsub $2 sub2

paste -d' ' sub1.ped sub2.ped > output-temp.ped 			#join the two columns to a temporary file
echo -e "SIMULATE\nSIM1\n0\n0\n0\n0" > preamble-temp.ped  	#Prepend family and individual ID details onto the PED 'SIMULATE SIM1    0       0       0       0 -'
cat output-temp.ped >> preamble-temp.ped					
rm output-temp.ped
mv preamble-temp.ped output-temp.ped

if [ "$3" = "" ]
then
	cat output-temp.ped | tr '\n' '\t' > output.ped
	echo 'Simulated individual saved to output.ped'
else
	cat output-temp.ped | tr '\n' '\t' > $3			#convert file back to typical ped "wide" file format - 
	echo 'Simulated individual saved to '$3
fi 													#i.e. 1 line per individual (in this case there is only one individual)

rm output-temp.ped
rm sub1.ped
rm sub2.ped