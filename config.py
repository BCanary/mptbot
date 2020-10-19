import vk_api
from vk_api.longpoll import VkLongPoll

token = ""
bot = vk_api.VkApi(token=token)
longpoll = VkLongPoll(bot)
