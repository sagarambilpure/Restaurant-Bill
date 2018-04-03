from mysql.connector import connect
import pandas as pd
from pandas import Series,DataFrame
import numpy as np

def get_data_rest_sql():
	conn=connect(host="localhost",database="restaurant",user="root",password="")
	t=DataFrame(columns=['code','name','price','veg',"type","count"])
	query='select * from details'
	i=1
	cursor=conn.cursor()
	cursor.execute(query)
	row=cursor.fetchone()
	while row is not None:
		t.loc[i]=row
		i+=1
		row=cursor.fetchone()
	cursor.close()
	t1=DataFrame(t[['name','price','veg',"type","count"]],columns=['name','price','veg',"type","count"],index=t["code"])
	return t1