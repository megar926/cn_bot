import mysql.connector

def scanBaseCn():
	mydb = mysql.connector.connect(
	  host="server224.hosting.reg.ru",
	  user="u1051830_alexand",
	  password="Megare926",
	  port="3306"
	)
	
	file = open("/home/pi/Documents/myprojects/server/bot/imbase/cn_read.txt", 'w')

	mycursor = mydb.cursor()

	mycursor.execute("SHOW DATABASES")

	for x in mycursor:
	  print(x) # Последовательный вывод информации о базах данных

	mycursor.execute("USE u1051830_cadence_name")

	mycursor.execute("SHOW TABLES")

	for x in mycursor:
	  print(x)

	mycursor.execute("SELECT * FROM cadence_name_query")

	for x in mycursor:
	  print(x)
	  file.write(f"{x[1]};;;{x[2]}\n")

	file.close()

scanBaseCn()
