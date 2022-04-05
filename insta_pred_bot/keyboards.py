from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

b1 = KeyboardButton('Предскажи аккаунт')
b2 = KeyboardButton('Инфо')

kb_main = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_main.row(b1, b2)
