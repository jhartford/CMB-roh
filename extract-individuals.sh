#!/bin/bash
# Randomly select bases from two individuals' PED files
# Random number generators here: http://tldp.org/LDP/abs/html/randomvar.html

#RANDOM=1 #set seed of the random number generator 
RANDOM=$$  # Reseed the random number generator using script process ID.

FILE=$RANDOM
RANGE=`wc -l $1 | awk {'print $1'}`   	#get the number of lines in the ped file
FIND=''
REPLACE='\n'

let 'FILE %= RANGE'   					#mod the random number by the number of lines so that the random line is less that range
let 'FILE += 1'							#add 1 so the random number isn't 0
echo 'Extracting individual '$FILE' from '$1
sed -n $FILE'p' $1 > $2'.ped'			#extract line from file

echo 'Individual saved to '$2'.ped'