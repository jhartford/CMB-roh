#!/bin/bash
# plink script to test for homozygosity. The parameters are those recommended by Howrigan, Simonson and Keller (2011)
# Usage: run with file name and "no-prune" as a parameter to not use LD pruning (default is to prune)

if [ "$2" = "no-prune" ]
then
	plink --noweb --bfile "$1" --out roh --homozyg --homozyg-snp 45 --homozyg-window-het 1 --homozyg-window-missing 5 --homozyg-window-threshold 0.05
else
	echo "Pruning..."
    if [ ! -f "$1-pruned.prune.out" ]
	then
		plink --noweb --bfile "$1" --out "$1-pruned" --indep 50 5 2
	fi
	plink --noweb --bfile "$1" --out "$1-roh" --exclude "$1-pruned.prune.out" --homozyg --homozyg-snp 45 --homozyg-window-het 1 --homozyg-window-missing 5 --homozyg-window-threshold 0.05  	
fi