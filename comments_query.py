import psycopg2
from sqlalchemy import create_engine

import cPickle as pickle
import pandas as pd
from pprint import pprint

def analyzeSentiment(celex):
	#Connect to local postgres
	con = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='pass123')
	engine = create_engine('postgresql://postgres:pass123@localhost/postgres') #postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
	cur = con.cursor()

	getLobbyistsCommand = '''SELECT * FROM professional_consultancies where "Fields of interest" like \'%''' + str(q) + "%' "
	cur.execute(getLobbyistsCommand)

	colnames = [desc[0] for desc in cur.description]

	df = pd.DataFrame(cur.fetchall(), columns = colnames)

	df.index = df['Identification number']

	countryDF = df.groupby(u'Head office country').size()

	countryJSON = countryDF.to_json()

	allInfoJSON = df.to_json()
	print(countryJSON)
	pprint(allInfoJSON)

	return countryJSON


