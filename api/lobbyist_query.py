import psycopg2
from sqlalchemy import create_engine
import pandas as pd
import json

def search_issues(q):
	countryCodeLookup = { 'Austria' : 'at',
						'Belgium' :  'be',
						'Croatia': 'hr',
						'Cyprus' : 'cy',
						'Czech Republic' : 'cz',
						'Denmark' : 'dk',
						'Finland' : 'fi',
						'France' : 'fr',
						'Germany' : 'ge',
						'Greece' : 'gr',
						'Hungary' : 'hu',
						'Ireland' : 'ie',
						'Italy' : 'it',
						'Lituania' : 'lt',
						'Luxembourg' : 'lu',
						'Malta' : 'mt',
						'Netherlands' : 'nl',
						'Norway' : 'no',
						'Poland' : 'pl',
						'Portugal' : 'pt',
						'Romania' : 'ro',
						'Russia, Federation Of' : 'ru',
						'Serbia' : 'rs',
						'Slovakia' : 'sk',
						'Slovenia' : 'sl',
						'Spain' : 'es',
						'Sweden' : 'se',
						'Switzerland' : 'ch',
						'Turkey' : 'tr',
						'United Kingdom' : 'uk',
						}
       
	#Connect to local postgres
	con = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='pass123')
	engine = create_engine('postgresql://postgres:pass123@localhost/postgres') #postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
	cur = con.cursor()

	getLobbyistsCommand = '''SELECT * FROM professional_consultancies where "Fields of interest" like \'%''' + str(q) + "%' "
	cur.execute(getLobbyistsCommand)

	colnames = [desc[0] for desc in cur.description]

	df = pd.DataFrame(cur.fetchall(), columns = colnames)

	df.index = df['Identification number:']

	countryDF = df.groupby(u'Head office country').size()

	countryJSON = countryDF.to_dict()

	allCountries = list(countryDF.keys())

	countryJSONNew = []

	for country in allCountries:
		try:
			abbrev = countryCodeLookup[country]
			countryJSONNew.append({ "hc-key": abbrev, 'value' : countryJSON[country]})
			# countryJSONNew[abbrev] = countryJSON[country]
		except:
			continue

	result = json.dumps(countryJSONNew)
	return result



