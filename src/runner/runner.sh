#!/bin/bash
trap 'kill $(jobs -p)' EXIT
python ../communication/simpleAgent.py 8000 &
python runner.py 
kill $!

