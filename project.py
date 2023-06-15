
import json
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

from env import TOKEN


bot = Bot(token=TOKEN)


dp = Dispatcher(bot)    

data = []

@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer('Привет! Введите свои данные Имя Фамилия Возраст')

@dp.message_handler(commands=['info']) 
async def get_user_info(message: types.Message):
    user_id = message.from_user.id
    for user in data:
        if user["id"] == user_id:
            response = f"Имя: {user['name']}nФамилия: {user['surname']}nВозра: {user['age']}"
            await message.answer(response)
            return
    await message.answer('Пользователь не найден')


@dp.message_handler(content_types=['text'])
async def add_to_json(message: types.Message):
    name, surname, age = message.text.split()
    user = {"id": message.from_user.id, "name": name, "surname": surname, "age": age}

    data.append(user)

    await message.answer('Данные записаны в файл')

    # with open('data.json', 'w') as json_file:
    #     json.dump(data, json_file)


if __name__ == '__main__':
    # with open('data.json', 'r') as json_file:
    #     data = json.load(json_file)
    executor.start_polling(dp, skip_updates=True)