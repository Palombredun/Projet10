import datetime

import requests

req = requests.get('https://static.openfoodfacts.org/data/delta/index.txt')
dt = datetime.date.today()
file = 'update/data/' + str(dt) + '.txt'

with open(file, 'w') as f:
	f.write(req.text)
