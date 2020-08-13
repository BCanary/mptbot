from vk_api.keyboard import VkKeyboard, VkKeyboardColor

keyboard = VkKeyboard(one_time=True)
keyboard.add_button('играть в 21', color=VkKeyboardColor.DEFAULT)
keyboard.add_line()
keyboard.add_button('информация', color=VkKeyboardColor.POSITIVE)

err_keyboard = VkKeyboard(one_time=True)
err_keyboard.add_button('играть в 21', color=VkKeyboardColor.DEFAULT)
err_keyboard.add_line()
err_keyboard.add_button('информация', color=VkKeyboardColor.POSITIVE)
err_keyboard.add_line()
err_keyboard.add_button("ошибка", color=VkKeyboardColor.NEGATIVE)

in_game_search_keyboard = VkKeyboard(one_time=True)
in_game_search_keyboard.add_button('Выйти из поиска', color=VkKeyboardColor.NEGATIVE)

in_game_keyboard = VkKeyboard(one_time=True)
in_game_keyboard.add_button('Взять карту', color=VkKeyboardColor.POSITIVE)
in_game_keyboard.add_line()
in_game_keyboard.add_button('Пропустить ход', color=VkKeyboardColor.DEFAULT)
in_game_keyboard.add_line()
in_game_keyboard.add_button('Выйти из игры', color=VkKeyboardColor.NEGATIVE)