import vk_api
from config import bot
from random import randint

def sendMessage(user_id, message, keyboard=None):
	if keyboard == None:
		bot.method("messages.send", {"user_id": user_id, "message":message, 
			"random_id": randint(0,1024*1024)})
	else:
		bot.method("messages.send", {"user_id": user_id, "message":message, 
					"random_id": randint(0,1024*1024), "keyboard": keyboard.get_keyboard()})