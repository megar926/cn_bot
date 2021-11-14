import mysql.connector
import datetime
import pandas as pd

mydb = mysql.connector.connect(
	host="server224.hosting.reg.ru",
 	user="u1051830_alexand",
 	password="Megare926",
 	port="3306",
 	db = "u1051830_cadence_name")
            
mycursor = mydb.cursor()
#mycursor.execute(f"INSERT INTO cadence_name_query VALUES ('{datetime.datetime.now()}', 'name', 'cadence')")
#mydb.commit()

# mycursor.execute(f"SELECT name FROM cadence_name_query WHERE cadence_name = 'cadence'")
# select_data = []
# for x in mycursor:
# 	select_data.append(x[0])

# if len(select_data)>0:
# 	print(select_data[0])

mycursor.execute("DROP TABLE IF EXISTS intermech_base")
mycursor.execute("CREATE TABLE intermech_base (name varchar(64), cadence_name varchar(64), var varchar(64), firm varchar(64), class varchar(64), func varchar(64))")

base = pd.read_excel("/home/pi/Documents/myprojects/server/bot/imbase/base.xlsx")

for x in range(base.shape[0]):
	mycursor.execute(f"INSERT INTO intermech_base VALUES ('{base.iloc[x][base.columns[0]]}', '{base.iloc[x][base.columns[1]]}', '{base.iloc[x][base.columns[2]]}', '{base.iloc[x][base.columns[3]]}', '{base.iloc[x][base.columns[4]]}', '{base.iloc[x][base.columns[5]]}')")
	if(x%10000 == 0):
		print(x)
mydb.commit()

base = pd.read_excel("/home/pi/Documents/myprojects/server/bot/imbase/Соединители.xlsx")

for x in range(base.shape[0]):
	mycursor.execute(f"INSERT INTO intermech_base VALUES ('{base.iloc[x][base.columns[0]]}', '{base.iloc[x][base.columns[1]]}', '{base.iloc[x][base.columns[2]]}', '{base.iloc[x][base.columns[3]]}', '{base.iloc[x][base.columns[4]]}', '{base.iloc[x][base.columns[5]]}')")
mydb.commit()
