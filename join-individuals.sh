#!/bin/bash
#Join two individuals

function randomsub {
	RANDOM=$$  # Reseed the random number generator using script process ID.
	cat $1 | tr '\t' '\n' > temp1.ped
	tail -n +7 temp1.ped > temp2.ped
	rm temp1.ped
	cat temp2.ped | awk -v seed=$RANDOM 'BEGIN{srand(seed);}{test = rand(); if (test<0.5) print $1; else print $2; }' > $2'.ped'
}

randomsub $1 sub1
randomsub $2 sub2

paste -d' ' sub1.ped sub2.ped > output-temp.ped
echo -e "SIMULATE\nSIM1\n0\n0\n0\n0" > preamble-temp.txt
cat output-temp.ped >> preamble-temp.txt
rm output-temp.ped
mv preamble-temp.txt output-temp.ped
cat output-temp.ped | tr '\n' '\t' > output.ped

#'SIMULATE SIM1    0       0       1       -9'

rm output-temp.ped
rm sub1.ped
rm sub2.ped