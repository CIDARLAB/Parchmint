#!/bin/sh

#java -Xmx5000m  -jar runFluigi.jar ../devices/chthesis/64.uf -i fluigi.ini -o eps
#java -Xmx5000m  -jar runFluigi.jar ../devices_ali/xgrid_128.uf -i fluigi.ini -o eps

echo "Running pin annotator"

for f in ./*.json ;

do 
	echo "Running File $f";
	python pin_annotate.py $f
done