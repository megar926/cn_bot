import telebot
import config
import pandas as pd
import mysql.connector
import subprocess
import configparser
#pip3 install PyTelegramBotAPI
#import pickle

config_ini = configparser.ConfigParser()
config_ini.read("/home/alex/Документы/myprojects/cn_bot/config_linux.ini")
path_eri = config_ini["BASE_PATH"]["eri_base"]
path_con = config_ini["BASE_PATH"]["connector_base"]
path_upload_folder = config_ini["PROJECT_PATH"]["file_upload_folder"]

bot = telebot.TeleBot(config.TOKEN)

def scanBaseCn(text):
	df = pd.DataFrame()
	bomConverterData = text.replace('[', '').replace(']', '')
	bomConverterData = bomConverterData.split("'")
	list_d = []
	for x in bomConverterData:
		list_d.append(x.lstrip().lstrip().replace("\n", ''))
	bomConverterData = list_d
	print(bomConverterData)
	
	file = open("/home/pi/Documents/myprojects/server/bot/imbase/cn_read.txt", 'r')
	file = file.readlines()
	query_list_rus = []
	query_list_cn = []
	return_list = []
	rusDf = []
	cnDf = []
	for x in file:
		data = x.split(";;;")
		print(data)
		query_list_rus.append(data[0].replace("\n", ""))
		query_list_cn.append(data[1].replace("\n", ""))
	for x in bomConverterData:
		if x in query_list_cn:
			print(x)
			for y, z in zip(query_list_rus, query_list_cn):
				if (x == z) & (len(x) > 5):
					return_list.append(f"{x} {y}")
					rusDf.append(y)
					cnDf.append(x)
	df['PN'] = rusDf
	df['CN'] = cnDf
	print(return_list)
	return return_list, df

@bot.message_handler(commands=['start'])
def welcome(message):
	sti = open('static/sticker.webp', 'rb')
	bot.send_sticker(message.chat.id, sti)
	bot.send_message(message.chat.id, message.from_user)
	bot.send_message(message.chat.id, message.chat.id)

@bot.message_handler(content_types=['text'])
def lalala(message):
	#bot.send_message(message.chat.id, message.text)
	if (message.text[0] == "[") & (message.text[-1] == "]"):
		bot.send_message(message.chat.id, "Find component started, please wait")
		try:
			findedComponents, df = scanBaseCn(message.text)
			for x in findedComponents:
				bot.send_message(message.chat.id, x)
			df.to_excel('/home/pi/Documents/myprojects/server/bot/imbase/data.xlsx')
			file = open('/home/pi/Documents/myprojects/server/bot/imbase/data.xlsx', "rb")
			bot.send_document(message.chat.id, file)
			file.close()
		except:
			bot.send_message(message.chat.id, "ERROR")	
		
	if (message.text == 'upload'):
		bot.send_message(message.chat.id, f'Обновляем базу!!!')
		try:
			mydb = mysql.connector.connect(
				host="server224.hosting.reg.ru",
				user="u1051830_alexand",
				password="Megare926",
				port="3306",
				db = "u1051830_cadence_name")
			bot.send_message(message.chat.id, f'Успешное подключение к серверу!!!')
			mycursor = mydb.cursor()
			mycursor.execute("DROP TABLE IF EXISTS intermech_base")
			mycursor.execute("CREATE TABLE intermech_base (name varchar(64), cadence_name varchar(64), var varchar(64), firm varchar(64), class varchar(64), func varchar(64))")
			base = pd.read_excel("/home/pi/Documents/myprojects/server/bot/imbase/base.xlsx")
			bot.send_message(message.chat.id, f'{base.columns}')
			for x in range(base.shape[0]):
				mycursor.execute(f"INSERT INTO intermech_base VALUES ('{base.iloc[x][base.columns[0]]}', '{base.iloc[x][base.columns[1]]}', '{base.iloc[x][base.columns[2]]}', '{base.iloc[x][base.columns[3]]}', '{base.iloc[x][base.columns[4]]}', '{base.iloc[x][base.columns[5]]}')")
			mydb.commit()

			base = pd.read_excel("/home/pi/Documents/myprojects/server/bot/imbase/Соединители.xlsx")
			bot.send_message(message.chat.id, f'{base.columns}')
			for x in range(base.shape[0]):
				mycursor.execute(f"INSERT INTO intermech_base VALUES ('{base.iloc[x][base.columns[0]]}', '{base.iloc[x][base.columns[1]]}', '{base.iloc[x][base.columns[2]]}', '{base.iloc[x][base.columns[3]]}', '{base.iloc[x][base.columns[4]]}', '{base.iloc[x][base.columns[5]]}')")
			mydb.commit()

			bot.send_message(message.chat.id, f'База на reg.ru обновлена!!!')
		except:
			bot.send_message(message.chat.id, f'ОШИБКА!!! База на reg.ru не обновлена!!!')
	elif (message.text == 'temp'):
		temp = subprocess.check_output(['vcgencmd', 'measure_temp'])
		bot.send_message(message.chat.id, f'{temp}')
	elif (message.text == 'reboot'):
		temp = subprocess.check_output(['sudo','reboot', 'now'])
		bot.send_message(message.chat.id, f'REBOOT!!!')

@bot.message_handler(content_types=['document'])
def upload_files(message):
	file_name = message.document.file_name
	file_id = message.document.file_name
	file_id_info = bot.get_file(message.document.file_id)
	downloaded_file = bot.download_file(file_id_info.file_path)
	tab = pd.read_excel(downloaded_file)
	tab.to_excel(f'{path_upload_folder}+{message.document.file_name}', index = False)
	bot.send_message(message.chat.id, f'{message.document.file_name} сохранен!')
	#pickle.dump(tab, f'/home/pi/Documents/myprojects/server/bot/imbase/{message.document.file_name.split(".")[0]}')
	#bot.send_message(message.chat.id, f'{message.document.file_name.split(".")[0]} сохранен!')

bot.polling(none_stop=True)
