import vk_api
import random
from bot_functions import sendMessage
from keyboards import in_game_keyboard, keyboard

lobby = []
in_game = []
games = []

def findLobby(user_id):
	global games
	for game in games:
		if user_id in [player["id"] for player in game.players]:
			return game
	print("Нихуя не нашел :(")

class Game21:
	"""
	Игровой класс сессии
	"""
	def __init__(self, user_id1, user_id2):
		global lobby, in_game
		self.player1 = {"id": user_id1, "cards": []}
		self.player2 = {"id": user_id2, "cards": []}
		self.players = (self.player1, self.player2)

		self.active = random.choice([user_id1, user_id2]) 

		self.propusk = 0

		self.cards = [6,7,8,9,10,2,3,4,11] * 4
		random.shuffle(self.cards)

		for player in self.players:
			in_game.append(lobby.pop(lobby.index(player["id"])))
			for i in range(0,2):
				player["cards"].append(self.cards.pop())
			sendMessage(player["id"], "Вы получаете 2 карты", in_game_keyboard)

		self.printCards()
		self.checkWin()
	def getSumm(self, arr):
		summ = 0
		for i in arr:
			summ += i
		return summ
	def printCards(self):
		for player in self.players:

			all_cards_text = "Ваши карты: "
			zapyata = False
			summ = self.getSumm(player["cards"])

			for i in player["cards"]:
				if zapyata:
					all_cards_text += ", "
				all_cards_text += str(i)
				zapyata = True

				#sendMessage(player["id"], player["cards"])

			sendMessage(player["id"], all_cards_text + " - " + str(summ) + " в сумме", in_game_keyboard)

			if(self.active == player["id"]):
				sendMessage(player["id"], "Ваш ход...")
	def disconnectAll(self):
		global in_game, games
		sendMessage(self.players[0]["id"], "У противника было: " + str(self.getSumm(self.players[1]["cards"])))
		sendMessage(self.players[1]["id"], "У противника было: " + str(self.getSumm(self.players[0]["cards"])))
			
		for player in self.players:
			sendMessage(player["id"], "Игра окончена", keyboard)
			in_game.remove(player["id"])
		games.remove(self)
		del self

	def anotherPlayer(self, player):
		player_id = self.players.index(player)
		if player_id == 0:
			return self.players[1]
		elif player_id == 1:
			return self.players[0]

	def findPlayerById(self, user_id):
		for player in self.players:
			if player["id"] == user_id:
				return player

	def action(self, user_id, action):
		#take_card, pass
		if(self.active == user_id):
			enemy_id = self.anotherPlayer(self.findPlayerById(user_id))["id"]
			if action == "take_card":
				new_card = self.cards.pop()
				sendMessage(user_id, "Вы взяли карту " + str(new_card))
				sendMessage(enemy_id, "Игрок взял карту")
				self.findPlayerById(user_id)["cards"].append(new_card)
				self.active = self.anotherPlayer(self.findPlayerById(user_id))["id"]
				self.propusk = 0
			if action == "pass":
				sendMessage(user_id, "Вы пропустили ход")
				sendMessage(enemy_id, "Игрок пропустил ход")

				self.propusk += 1
	
				self.active = self.anotherPlayer(self.findPlayerById(user_id))["id"]
			if action == "leave":
				sendMessage(user_id, "Вы вышли")
				sendMessage(enemy_id, "Противник вышел")
				self.disconnectAll()

			self.printCards()
			self.checkWin()
		else:
			sendMessage(self.findPlayerById(user_id)["id"], "Вы не ходите!")
	def checkWin(self):
		for player in self.players:
			summ = self.getSumm(player["cards"])
			if summ > 21:
				sendMessage(player["id"], "Вы проиграли!")
				sendMessage(self.anotherPlayer(player)["id"], "Вы выйграли!")
				self.disconnectAll()
			if summ == 21:
				sendMessage(player["id"], "Вы выйграли!")
				sendMessage(self.anotherPlayer(player)["id"], "Вы проиграли!")
				self.disconnectAll()
			if self.propusk == 2:
				if self.getSumm(player["cards"]) > self.getSumm(self.anotherPlayer(player["id"])["cards"]):
					sendMessage(player["id"], "Никто не сделал ход. Вы выйграли!")
					sendMessage(self.anotherPlayer(player)["id"], "Никто ни сделал ход. Вы проиграли!")
					self.disconnectAll()
				elif self.getSumm(player["cards"]) == self.getSumm(self.anotherPlayer(player["id"])["cards"]):
					sendMessage(player["id"], "Никто не сделал ход. Ничья!")
					sendMessage(self.anotherPlayer(player)["id"], "Никто ни сделал ход. Ничья!")
					self.disconnectAll()