import asyncio
from env import TOKEN

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import Message

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from keyboards import keyboard

bot = Bot(token=TOKEN) 
dp = Dispatcher(bot, storage=MemoryStorage())

connected_users = []

@dp.message_handler(commands=['start', 'help'], state='*')
async def send_welcome(message: types.Message, state: FSMContext):
    await message.answer("привет!\nя эхо бот!\nкпак тебя зовут")
    await state.set_state("q1")


@dp.message_handler(state = "q1")
async def process_name(message: types.Message, state: FSMContext):
    name = message.text
    await state.update_data({"name" : name})
    await state.set_state("q2")
    await message.answer("Say your age")
    
@dp.message_handler(state = "q2")
async def process_age(message: types.Message, state: FSMContext):
    age = message.text
    if age.isdigit():
        await state.update_data({"age" : int(age)})
        await state.set_state("echo")
        await message.answer("Now I am echo-bot!")
    elif age.isdigit() and int(age) < 18:
        await message.answer("Пошел отсюда")
        connected_users.append(message.from_user.id)
        await bot.send_chat_action(message.from_user.id, types.ChatActions.TYPING)
        connected_users.append(message.from_user.id)
    else:
        data = await state.get_data()
        await message.answer(f"This is not a number, try another time {data['name']}")


@dp.message_handler(state='echo')
async def cho(message: types.Message):
    for user in connected_users:
        if message.from_user.id == user:
            continue 
        await bot.semd_message(user, message.text)



@dp.message_handler(state = "echo")
async def echo(message: Message):
    tasks = []
    for user in connected_users:
        if message.from_user.id == user:
            continue
        tasks.append(
            bot.send_message(user, f'@{message.from_user.username} : {message.text}')
            )
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)