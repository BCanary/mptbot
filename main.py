# import the requests library
import requests
import xlrd
import telebot
from telebot import types
from bs4 import BeautifulSoup

"""
ОСТОРОЖНО ЗДЕСЬ И ДАЛЕЕ ГОВНОКОД НАПИСАННЫЙ ПОД СТРЕССОМ! Я ВАС ПРЕДУПРЕДИЛ!
"""

markup = types.ReplyKeyboardMarkup()
itembtn1 = types.KeyboardButton('информация')
markup.add(itembtn1)

token = "1364150425:AAErYiwGtWHTM11dL82aY6uL4rte6IwhqiM"

bot = telebot.TeleBot(token)

#XLSX_URL = "https://6c869467-a-7da13995-s-sites.googlegroups.com/a/mpt.ru/priemnaa-komissia-2020/home/090207%20%20%20%D0%91%D0%AE%D0%94%D0%96%D0%95%D0%A2%20.xlsx?attachauth=ANoY7coOmUFB5Ramu3cJrEdrMzRqXq0HTbQgyRTUsY6cc-4ryf5yMUOiLqyNTpBCi_qSygzWeaXNStBDBnpzgpUEejaajauLUfKA1-WBOUse91A5CO7lx1lQ17_3HVpDbcLte1zps7i6hwSAwtd0rdnju4Z4pX7INVjAKnoEEF_yTpCL99L2owONfUNV3-oA_EaqByXfp9VsC-HmmsTOnDQ5gcFtJf5rkppU-UZmA4fQSDIXsz6rkN8wi_ZlVbXkrEvc9oyu8UCEon0tqbBDHVCuGWYnCtOdsg%3D%3D&attredirects=0&d=1"
excel_file = xlrd.open_workbook('temp.xlsx')

#выбираем активный лист
sheet = excel_file.sheet_by_index(0)

def getExcelTable(tr):
	global excel_file, sheet
	
	r = requests.get("https://sites.google.com/a/mpt.ru/priemnaa-komissia-2020/")
	
	print(r.status_code)
	
	b = BeautifulSoup(r.content, "lxml")
	#						tr 5 (Инф безопасность)
	#table 3 (специальности) tr 2 (Инф системы и прог) td 1 (350 мест)
	r = requests.get(b.find_all("table")[3].find_all("tr")[tr].find_all("td")[1].find("a")["href"])
	
	text_start = r.text.find("http://sites.google.com/a/mpt.ru/priemnaa-komissia-2020/home/")
	
	text_end = text_start
	while True:
		text_end += 1
		if r.text[text_end] == "\"":
			break 
	
	xls_url = r.text[text_start:text_end]
	
	# download the file contents in binary format
	r = requests.get(xls_url)
	 
	# open method to open a file on your system and write the contents
	with open("temp.xlsx", "wb") as code:
		code.write(r.content)
	
	
	excel_file = xlrd.open_workbook('temp.xlsx')
	#выбираем активный лист
	sheet = excel_file.sheet_by_index(0)
	print("Loaded!")

def getExcelPosition(tr):
	global excel_file
	
	start = 3
	same_score_position = -1
	position = -1
	uvedomleni = 0
	vsego = 0
	summ_ball = 0
	status = "Error"
	last_uvedomlenie_ball = -1
	
	#[1021.0, 'Максяшев Андрей Сергеевич', 3.1053, 9.0, 'Да'] 
	
	sheet = excel_file.sheet_by_index(0)

	if tr == 2:
		mest = 350
	elif tr == 5:
		mest = 45

	check = 0
	for i in range(start, 30+start): 
		val = sheet.row_values(i)
		if val[4] == "Да":
			print(val)
			check += 1
	if check < 29:
		print("NO")
		sheet = excel_file.sheet_by_index(1)
	try:
		for i in range(start, 30000):
			if i <= 3:
				continue
			val = sheet.row_values(i)
			#print(val)
			if val[1] == "Коняшин Владислав Владимирович":
				position = i-start
				status = val[4]
			if val[4] == "Да":
				if val[2] >= 4.48 and val[2] <= 4.5:
					same_score_position = i-start
				if i-start == mest:
					last_uvedomlenie_ball = val[2]
				uvedomleni += 1
			vsego = val[0]
			summ_ball += val[2]


	except IndexError:
		return {
			"same_score_position": str(same_score_position),
			"last_uvedomlenie_ball": str(last_uvedomlenie_ball),
			"position": str(position),
			"uvedomleni": str(uvedomleni),
			"vsego": str(vsego),
			"sredni": str(summ_ball/vsego),
			"status": status
		}
		
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global getExcelTable
	if (message.text == "/start"):
		bot.send_message(message.from_user.id, "Жми кнопку", reply_markup=markup)
	if (message.text) == "информация":
		bot.send_message(message.from_user.id, "Отправил запрос на удаленный сервер... Жду файла xlsx")
		for tr in [2,5]:
			if tr == 2:
				profa = "Программирование"
			elif tr == 5:
				profa = "Безопасность"

			getExcelTable(tr)
			response = getExcelPosition(tr)
			bot.send_message(message.from_user.id, profa + ": Ты на: " + response["position"] + " месте\nПозиция со схожим баллом в уведомления:" + response["same_score_position"] + "\nСтатус твоего уведомления:" + response["status"] + "\nВсего подано уведомлений: " + response["uvedomleni"] + "\nПоследний балл на уведомлениях: " + response["last_uvedomlenie_ball"] + "\nВсего подано заявлений:" + response["vsego"] + "\nОбщий средний балл:" + response["sredni"], reply_markup=markup)

#print(getExcelPosition()["sredni"])
bot.polling(none_stop=True, interval=0)