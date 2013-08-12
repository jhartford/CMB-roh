#CMB Autozygosity project

Set of scripts to use in conjunction with plink.

At present there are the following scripts:

- *roh.sh* which runs plink to check for runs of homozygosity with LD-pruning 
- *extract-individuals.sh* which randomly extracts an individual from a given PED file
- *join-individuals.sh* which takes two individual's PED files as input and outputs a random 'child' individual (i.e. it chooses a random base from each individual to combine)