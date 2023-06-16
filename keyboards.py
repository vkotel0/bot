from aiogram.types import \
    KeyboardButton, \
    ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, \
    InlineKeyboardMarkup, \
    InlineKeyboardButton



from aiogram.utils.callback_data import CallbackData

inb_callback_data = CallbackData('inb', 'purpose')
       
i1 = InlineKeyboardButton('👍', callback_data=inb_callback_data.new('up'))
i2 = InlineKeyboardButton('👎', callback_data=inb_callback_data.new('down'))        

inlineKeyboard = InlineKeyboardMarkup().insert(i1).insert(i2)       
        
b1 = KeyboardButton("Поделиться местом", request_location=True)
b2 = KeyboardButton("поделиться номером", request_contact=True)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(b1).add(b2)


#keyboard2 = ReplyKeyboardMarkup(one_time_keyboard=True)
#keyboard2.insert(b1).insert(b2).insert(b3)



