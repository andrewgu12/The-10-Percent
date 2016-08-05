import psycopg2
from sqlalchemy import create_engine

import cPickle as pickle
import pandas as pd

#Connect to local postgres
con = psycopg2.connect(dbname='postgres', user='postgres', host='localhost', password='pass123')
engine = create_engine('postgresql://postgres:pass123@localhost/postgres') #postgresql://[user[:password]@][netloc][:port][/dbname][?param1=value1&...]
cur = con.cursor()

df = pd.read_csv('professional_consultancies.csv')
print(df)

df.to_sql('professional_consultancies', engine)