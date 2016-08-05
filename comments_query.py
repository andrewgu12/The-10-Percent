import psycopg2
from sqlalchemy import create_engine

import cPickle as pickle
import pandas as pd
from pprint import pprint
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from nltk import tokenize
import sys


import json
import numpy as np


def analyzeSentiment(celex):


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



	# getLobbyistsCommand = "SELECT * FROM eu_comments"
	# cur.execute(getLobbyistsCommand)

	# colnames = [desc[0] for desc in cur.description]

	# df = pd.DataFrame(cur.fetchall(), columns = colnames)
	# df['sentiment'] = 0


	# for index, row in df.iterrows():
	# 	text = row['full_pdf']

	# 	if len(text) <= 0:
	# 		continue

	# 	try:
	# 		lines_list = tokenize.sent_tokenize(text)
	# 	except:
	# 		continue

	# 	sentimentDict = {'positive' : [], 'neutral' : [], 'negative': [], 'compound' : []}

	# 	sid = SentimentIntensityAnalyzer()
	# 	for sentence in lines_list:
	# 		# print(sentence)
	# 		ss = sid.polarity_scores(sentence)

	# 		sentimentDict['positive'].append(ss['pos'])
	# 		sentimentDict['negative'].append(ss['neg'])
	# 		sentimentDict['neutral'].append(ss['neu'])

	# 		sentimentDict['compound'].append(ss['compound'])

	# 	overallSentiment = 0

	
	# 	sentimentDict['positive'] = np.mean(sentimentDict['positive'] )
	# 	sentimentDict['negative'] = np.mean(sentimentDict['negative'] )
	# 	sentimentDict['neutral'] = np.mean(sentimentDict['neutral'] )

	# 	sentimentDict['compound'] = np.mean(sentimentDict['compound'] )


	# 	if sentimentDict['compound'] > 0:#sentimentDict['negative']:
	# 		overallSentiment = 1

	# 	else:
	# 		overallSentiment = -1

		
	# 	df.loc[index, 'sentiment'] = overallSentiment

	# df = df[ df['sentiment'] != 0]
	# pprint(df['county'])

	# df.to_sql('eu_comments_sentiment', engine, if_exists = 'replace')





	getLobbyistsCommand = "SELECT * FROM eu_comments_sentiment"
	cur.execute(getLobbyistsCommand)

	colnames = [desc[0] for desc in cur.description]

	df = pd.DataFrame(cur.fetchall(), columns = colnames)

	df = df.groupby('county').mean()

	df['sentiment'] = (df['sentiment'] + 1) / 2
	df = df['sentiment'].to_frame()

	# print(df)

	rowNames = ['-', '?', '??', 'Czech Republic', 'Belgium', 'Denmark', 'Germany', 'Spain', 'France', 'Croatia', 'Italy', 'Latvia', 'Lituania', 'M', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovenia', 'Slovakia', 'Finland', 'Sweden', 'United Kingdom', 'Austria', 'Ireland']


	df.index = rowNames
	countryDict = df.to_dict(orient = 'index')

	# print(countryDict)
	allCountries = list(countryDict.keys())

	countryJSONNew = []

	for country in allCountries:
		try:
			abbrev = countryCodeLookup[country]

			countryJSONNew.append({ "hc-key": abbrev, 'value' : countryDict[country]['sentiment']})

		except:
			continue

	# pprint(countryJSONNew)

	countryJSONNew = json.dumps(countryJSONNew)
	allInfoJSON = df.to_json()
	pprint(countryJSONNew)

	return countryJSONNew

# analyzeSentiment('')