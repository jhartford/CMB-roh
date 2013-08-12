#!/bin/bash
# Randomly select bases from two individuals' PED files
# Random number generators here: http://tldp.org/LDP/abs/html/randomvar.html

RANDOM=1 #set seed of the random number generator 
#RANDOM=$$  # Reseed the random number generator using script process ID.
FILE=$RANDOM
RANGE=`wc -l $1 | awk {'print $1'}`
FIND=''
REPLACE='\n'

let 'FILE %= RANGE'
let 'FILE += 1'
echo 'Extracting individual '$FILE' from '$1
sed -n $FILE'p' $1 | tr '\t' '\n' > temp.ped
tail -n +7 temp.ped > $2'.ped'
rm temp.ped

echo "Done subsetting files"

RANDOM=$$  # Reseed the random number generator using script process ID.

cat test.ped | awk -v seed=$RANDOM 'BEGIN{srand(seed);}{test = rand(); if (test<0.5) print $1; else print $2; }' > subset.ped
