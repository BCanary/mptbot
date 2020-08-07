# import the requests library
import requests
import xlrd
import telebot
from telebot import types

markup = types.ReplyKeyboardMarkup()
itembtn1 = types.KeyboardButton('информация')
markup.add(itembtn1)

token = "1364150425:AAErYiwGtWHTM11dL82aY6uL4rte6IwhqiM"

bot = telebot.TeleBot(token)

XLSX_URL = "https://6c869467-a-7da13995-s-sites.googlegroups.com/a/mpt.ru/priemnaa-komissia-2020/home/090207%20%20%20%D0%91%D0%AE%D0%94%D0%96%D0%95%D0%A2%20.xlsx?attachauth=ANoY7coOmUFB5Ramu3cJrEdrMzRqXq0HTbQgyRTUsY6cc-4ryf5yMUOiLqyNTpBCi_qSygzWeaXNStBDBnpzgpUEejaajauLUfKA1-WBOUse91A5CO7lx1lQ17_3HVpDbcLte1zps7i6hwSAwtd0rdnju4Z4pX7INVjAKnoEEF_yTpCL99L2owONfUNV3-oA_EaqByXfp9VsC-HmmsTOnDQ5gcFtJf5rkppU-UZmA4fQSDIXsz6rkN8wi_ZlVbXkrEvc9oyu8UCEon0tqbBDHVCuGWYnCtOdsg%3D%3D&attredirects=0&d=1"
excel_file = xlrd.open_workbook('temp.xlsx')

#выбираем активный лист
sheet = excel_file.sheet_by_index(0)

def getExcelTable():
	global XLSX_URL, excel_file, sheet
	# download the file contents in binary format
	r = requests.get(XLSX_URL)
	 
	# open method to open a file on your system and write the contents
	with open("temp.xlsx", "wb") as code:
		code.write(r.content)
	
	
	excel_file = xlrd.open_workbook('temp.xlsx')
	#выбираем активный лист
	sheet = excel_file.sheet_by_index(0)
	print("Loaded!")

def getExcelPosition():
	global excel_file
	
	start = 3
	
	position = -1
	uvedomleni = 0
	vsego = 0
	summ_ball = 0
	
	#[1021.0, 'Максяшев Андрей Сергеевич', 3.1053, 9.0, 'Да'] 
	
	try:
		for i in range(start, 30000):
			if i == 3:
				continue
			val = sheet.row_values(i)
			#print(val)
			if val[1] == "Коняшин Владислав Владимирович":
				position = i-start
			if val[4] == "Да":
				uvedomleni += 1
			vsego = val[0]
			summ_ball += val[2]
	except IndexError:
		return {
			"position": str(position),
			"uvedomleni": str(uvedomleni),
			"vsego": str(vsego),
			"sredni": str(summ_ball/vsego)
		}
		
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
	global getExcelTable
	if (message.text == "/start"):
		bot.send_message(message.from_user.id, "Жми кнопку ЖМИ КНОПКУ!!!", reply_markup=markup)
	if (message.text) == "информация":
		bot.send_message(message.from_user.id, "Отправил запрос на удаленный сервер... Жду файла xlsx")
		getExcelTable()
		response = getExcelPosition()
		bot.send_message(message.from_user.id, "Ты на: " + response["position"] + " месте\nВсего подано уведомлений: " + response["uvedomleni"] + "\n" + "Всего подано заявлений:" + response["vsego"] + "\nОбщий средний балл:" + response["sredni"], reply_markup=markup)


#print(getExcelPosition()["sredni"])
bot.polling(none_stop=True, interval=0)