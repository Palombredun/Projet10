#!/bin/bash

echo "toto"
python update/deltas_urls.py
echo "titi"

now=$(date +"%Y-%m-%d")

filename="$now.txt"
base_url="https://static.openfoodfacts.org/data/delta/"

# download each file contained in the 
n=1
cd update/data
while read line; 
do
	url="$base_url$line"
	echo "$url"
	wget "$url"
	echo "$n"
	n=$((n+1))
done < $filename

gunzip \*.gz
cd ../..

python manage.py update_db.py
rm update/data/*.csv