#!/bin/bash
# Randomly select bases from two individuals' PED files
# Random number generators here: http://tldp.org/LDP/abs/html/randomvar.html

#RANDOM=1 #set seed of the random number generator 
RANDOM=$$  # Reseed the random number generator using script process ID.
FILE=$RANDOM
RANGE=`wc -l $1 | awk {'print $1'}`
FIND=''
REPLACE='\n'

let 'FILE %= RANGE'
let 'FILE += 1'
echo 'Extracting individual '$FILE' from '$1
sed -n $FILE'p' $1 > $2'.ped'

echo 'Individual saved to '$2'.ped'