import vk_api
from vk_api.longpoll import VkLongPoll

token = "f729e0d0d654a503b745610253ae910aef4af57b473998d7e0811326abdb107fe1535a825ea9a699ec002"
bot = vk_api.VkApi(token=token)
longpoll = VkLongPoll(bot)