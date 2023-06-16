
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
from aiogram.types import \
    KeyboardButton, \
    ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, \
    InlineKeyboardMarkup, \
    InlineKeyboardButton

from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from keyboards import *

from aiogram.dispatcher import FSMContext
from env import TOKEN
import os
bot = Bot(token=TOKEN)


dp = Dispatcher(bot, storage=MemoryStorage())    

data = []

inb_callback_data = CallbackData('inb', 'purpose')

@dp.callback_query_handler(inb_callback_data.filter(), state='*')
async def process_callback_button(callback_query: types.CallbackQuery, callback_data: dict, state: FSMContext):
    purpose = callback_data['purpose']
    await bot.answer_callback_query(callback_query.id)
    if purpose == 'up':

        await bot.send_message(chat_id=callback_query.from_user.id, text='хихихаха')

    elif purpose == 'down':

        await bot.send_message(chat_id=callback_query.from_user.id, text='хихи')

@dp.message_handler(commands=['start'], state="*")
async def start_message(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Да", "Нет"]
    keyboard.add(*buttons)
    await message.answer('Привет! Хотите записать свои данные?', reply_markup=keyboard)
    await state.set_state("anwser")
    


@dp.message_handler(state="anwser") 
async def anwser(message: types.Message, state: FSMContext):
    if 'да' in message.text.lower():
        await state.set_state("yes")
        await message.answer('Запишите ФИО тремя словами')
        
    elif 'нет' in message.text.lower():
        await state.set_state('no')
    else:
        await message.reply("Напишите Да или Нет")
    


@dp.message_handler(commands=['info'], state="*") 
async def get_user_info(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    for user in data:
        if user["id"] == user_id:
            response = f"Имя: { user['name']}nФамилия: { user['surname']}nВозрат: { user['age']}"
            await message.answer(response)
            return
    await message.answer('Пользователь не найден')


from keyboards import *

@dp.message_handler(commands=['cknopca'], state="*")
async def cknopca_message(message: types.Message):
    await message.answer('Что вас интересует',
                         reply_markup=keyboard)


@dp.message_handler(content_types=['text'], state="yes")
async def add_to_json(message: types.Message, state: FSMContext):
    pieces = message.text.split()

    if len(pieces) == 3:
        name, surname, age = pieces
        user = {"id": message.from_user.id, "name": name, "surname": surname, "age": age}

        data.append(user)

        await message.answer('Данные записаны в файл')
        await state.set_state('name')
        with open('data.json', 'w') as json_file:
            json.dump(data, json_file)
    else:
        await message.reply('Запишите ФИО тремя словами')

@dp.message_handler(commands="test", state="*")
async def test(message: types.Message):
    await bot.send_message(chat_id=message.from_id, text='поделиться', reply_markup=keyboard)



if __name__ == '__main__':
    if os.path.isfile("data.json"):
        with open('data.json', 'r') as json_file:
            data = json.load(json_file)
    else:
        data = []

    executor.start_polling(dp, skip_updates=True)