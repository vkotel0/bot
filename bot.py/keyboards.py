from aiogram.types import \
    KeyboardButton, \
    ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
    
b1 = KeyboardButton("Найти собеседника")
b2 = KeyboardButton("Больше не хочу никого искать")
b3 = KeyboardButton("🙋‍♂️")

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(b1).add(b2).add(b3)

keyboard2 = ReplyKeyboardMarkup()