import psycopg2
from sqlalchemy import create_engine

import cPickle as pickle
import pandas as pd

#Connect to local postgres
con = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='pass123')
engine = create_engine('postgresql://postgres:pass123@localhost/postgres') #postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
cur = con.cursor()

df = pd.read_json('eu_comment_data.json')

# df = df.astype(str)
print(df)

# df = df.rename(columns = {u'(Organisation) name' : 'Organisation name', u'Full time equivalent (FTE)' : 'Full time equivalent', u'Estimate of costs (absolute amount)' : u'Estimate of costs - absolute amount' , u'Estimate of costs (as a range)' : u'Estimate of costs - as a range', u'Turnover (absolute amount)' : u'Turnover - absolute amount', u'Turnover (as a range)' : u'Turnover - as a range'})

print(df.columns)

df.to_sql('eu_comments', engine, if_exists = 'replace')