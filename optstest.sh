#!/bin/bash

options_found=0
 
while getopts ":a:b:" opt; do
	options_found=1
  	case $opt in
	    a)
	      echo "-a was triggered, Parameter: $OPTARG" >&2
	      ;;
	    b)
	      echo "-b was triggered, Parameter: $OPTARG" >&2
	      ;;	      
	    \?)
	      echo "Invalid option: -$OPTARG" >&2
	      exit 1
	      ;;
	    :)
	      echo "Option -$OPTARG requires an argument." >&2
	      exit 1
	      ;;
  	esac
done

if ((!options_found)); then
  echo "Script run without pruning."
fi