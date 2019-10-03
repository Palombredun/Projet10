#!/bin/bash

# download the filenames containing the updates to the db
python update/deltas_urls.py

now=$(date +"%Y-%m-%d")

filename="$now.txt"
base_url="https://static.openfoodfacts.org/data/delta/"

# download each csv contained in the text file
cd update/data
while read line; 
do
	echo $url
	url="$base_url$line"
	wget "$url"
done < $filename

gunzip *.gz
cd ../..

# 
python manage.py update_db
rm /home/baptiste/Documents/Openclassrooms/Projets_OC/Projet10/update/data/*.json