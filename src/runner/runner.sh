#!/bin/bash
if [ $# -lt 1 ]
then
    echo "please specify number of iterations"
    exit -1
fi
trap 'kill $(jobs -p)' EXIT
i=0
echo $1
while [ $i -lt $1 ]
do
	python ../communication/simpleAgent.py 8000 &
	python runner.py 
	let "i=$i+1"
	echo $i
done
kill $!

