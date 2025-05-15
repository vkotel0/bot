import logging
import os
import sqlite3
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.client.default import DefaultBotProperties

# Настройка логов
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token="7831741062:AAHrSmy8O4Wa3jVem1qrMRihd_Ex0V5YhRQ", default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
dp = Dispatcher(storage=MemoryStorage())


# ========== БАЗА ДАННЫХ ==========
def init_db():
    """Инициализация базы данных SQLite"""
    with sqlite3.connect('english_test.db') as conn:
        cursor = conn.cursor()

        # Таблица пользователей
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            tests_completed INTEGER DEFAULT 0,
            highest_level TEXT DEFAULT 'A1'
        )
        ''')

        # Таблица результатов тестов
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            total_questions INTEGER,
            level TEXT,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')

        # Таблица достижений
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            name TEXT,
            description TEXT,
            unlocked BOOLEAN DEFAULT FALSE,
            date_unlocked TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        ''')
        conn.commit()


def add_user(user_id: int, username: str, first_name: str, last_name: str):
    """Добавление нового пользователя"""
    with sqlite3.connect('english_test.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
        VALUES (?, ?, ?, ?)
        ''', (user_id, username, first_name, last_name))
        conn.commit()


# ========== ВОПРОСЫ ТЕСТА ==========
QUESTIONS = [
    # Уровень A1 (10 вопросов)
    {
        "question": "I ___ a student.",
        "options": ["am", "is", "are", "be"],
        "correct_answer": "am",
        "level": "A1"
    },
    {
        "question": "She ___ to the gym every day.",
        "options": ["go", "goes", "going", "gone"],
        "correct_answer": "goes",
        "level": "A1"
    },
    {
        "question": "This is ___ book.",
        "options": ["a", "an", "the", "-"],
        "correct_answer": "a",
        "level": "A1"
    },
    {
        "question": "They ___ from Spain.",
        "options": ["is", "are", "am", "be"],
        "correct_answer": "are",
        "level": "A1"
    },
    {
        "question": "___ you like ice cream?",
        "options": ["Do", "Does", "Are", "Is"],
        "correct_answer": "Do",
        "level": "A1"
    },
    {
        "question": "My brother ___ TV every evening.",
        "options": ["watch", "watches", "watching", "watched"],
        "correct_answer": "watches",
        "level": "A1"
    },
    {
        "question": "We ___ to the park yesterday.",
        "options": ["go", "goed", "went", "gone"],
        "correct_answer": "went",
        "level": "A1"
    },
    {
        "question": "There ___ many people here.",
        "options": ["is", "are", "am", "be"],
        "correct_answer": "are",
        "level": "A1"
    },
    {
        "question": "___ is your name?",
        "options": ["What", "How", "Where", "When"],
        "correct_answer": "What",
        "level": "A1"
    },
    {
        "question": "I can ___ a bike.",
        "options": ["ride", "riding", "rode", "rides"],
        "correct_answer": "ride",
        "level": "A1"
    },

    # Уровень A2 (10 вопросов)
    {
        "question": "If it rains, we ___ cancel the trip.",
        "options": ["will", "would", "should", "might"],
        "correct_answer": "will",
        "level": "A2"
    },
    {
        "question": "She has ___ finished her homework.",
        "options": ["yet", "just", "already", "still"],
        "correct_answer": "just",
        "level": "A2"
    },
    {
        "question": "This is the ___ movie I've ever seen!",
        "options": ["best", "good", "better", "well"],
        "correct_answer": "best",
        "level": "A2"
    },
    {
        "question": "He ___ his keys yesterday.",
        "options": ["loses", "lost", "has lost", "losing"],
        "correct_answer": "lost",
        "level": "A2"
    },
    {
        "question": "Would you like ___ tea?",
        "options": ["some", "any", "many", "few"],
        "correct_answer": "some",
        "level": "A2"
    },
    {
        "question": "She is ___ than her sister.",
        "options": ["tall", "taller", "tallest", "more tall"],
        "correct_answer": "taller",
        "level": "A2"
    },
    {
        "question": "I ___ my phone at home this morning.",
        "options": ["forget", "forgot", "forgotten", "forgetting"],
        "correct_answer": "forgot",
        "level": "A2"
    },
    {
        "question": "They have been friends ___ childhood.",
        "options": ["for", "since", "from", "during"],
        "correct_answer": "since",
        "level": "A2"
    },
    {
        "question": "You ___ eat so much sugar. It's unhealthy!",
        "options": ["should", "shouldn't", "must", "can"],
        "correct_answer": "shouldn't",
        "level": "A2"
    },
    {
        "question": "I'm not used to ___ early.",
        "options": ["wake", "waking", "woke", "woken"],
        "correct_answer": "waking",
        "level": "A2"
    },

    # Уровень B1 (10 вопросов)
    {
        "question": "By next year, I ___ here for 5 years.",
        "options": ["will work", "will have worked", "work", "am working"],
        "correct_answer": "will have worked",
        "level": "B1"
    },
    {
        "question": "If I ___ you, I would apologize.",
        "options": ["am", "was", "were", "have been"],
        "correct_answer": "were",
        "level": "B1"
    },
    {
        "question": "The report ___ by the manager yesterday.",
        "options": ["signs", "signed", "was signed", "has signed"],
        "correct_answer": "was signed",
        "level": "B1"
    },
    {
        "question": "She suggested ___ to the cinema.",
        "options": ["to go", "going", "go", "went"],
        "correct_answer": "going",
        "level": "B1"
    },
    {
        "question": "He's the man ___ car was stolen.",
        "options": ["who", "whose", "whom", "which"],
        "correct_answer": "whose",
        "level": "B1"
    },
    {
        "question": "I wish I ___ how to swim.",
        "options": ["know", "knew", "have known", "would know"],
        "correct_answer": "knew",
        "level": "B1"
    },
    {
        "question": "They ___ each other since 2010.",
        "options": ["know", "knew", "have known", "had known"],
        "correct_answer": "have known",
        "level": "B1"
    },
    {
        "question": "It's high time you ___ a job.",
        "options": ["find", "found", "will find", "have found"],
        "correct_answer": "found",
        "level": "B1"
    },
    {
        "question": "The more you practice, ___ you become.",
        "options": ["better", "the better", "the best", "good"],
        "correct_answer": "the better",
        "level": "B1"
    },
    {
        "question": "She ___ be at home. Her car isn't here.",
        "options": ["mustn't", "can't", "might not", "shouldn't"],
        "correct_answer": "can't",
        "level": "B1"
    }
]

# ========== СИСТЕМА ДОСТИЖЕНИЙ ==========
ACHIEVEMENTS = [
    {
        "name": "Новичок",
        "description": "Пройдите первый тест!",
        "condition": lambda stats: stats["tests_completed"] >= 1
    },
    {
        "name": "Ученик (A2)",
        "description": "Достигните уровня A2",
        "condition": lambda stats: stats["highest_level"] == "A2"
    },
    {
        "name": "Опытный тестируемый",
        "description": "Пройдите 5 тестов",
        "condition": lambda stats: stats["tests_completed"] >= 5
    }
]


def update_test_result(user_id: int, score: int, total: int, level: str):
    """Обновление результатов теста"""
    with sqlite3.connect('english_test.db') as conn:
        cursor = conn.cursor()

        # Обновляем статистику пользователя
        cursor.execute('''
        UPDATE users 
        SET tests_completed = tests_completed + 1,
            highest_level = CASE 
                WHEN highest_level = 'A1' AND ? IN ('A2', 'B1', 'B2', 'C1', 'C2') THEN ?
                WHEN highest_level = 'A2' AND ? IN ('B1', 'B2', 'C1', 'C2') THEN ?
                WHEN highest_level = 'B1' AND ? IN ('B2', 'C1', 'C2') THEN ?
                WHEN highest_level = 'B2' AND ? IN ('C1', 'C2') THEN ?
                WHEN highest_level = 'C1' AND ? = 'C2' THEN ?
                ELSE highest_level
            END
        WHERE user_id = ?
        ''', (level, level, level, level, level, level, level, level, user_id))

        # Добавляем результат теста
        cursor.execute('''
        INSERT INTO test_results (user_id, score, total_questions, level)
        VALUES (?, ?, ?, ?)
        ''', (user_id, score, total, level))

        conn.commit()


def get_user_stats(user_id: int) -> dict:
    """Получение статистики пользователя"""
    with sqlite3.connect('english_test.db') as conn:
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
        user = cursor.fetchone()

        if not user:
            return None

        cursor.execute('''
        SELECT name, description, unlocked 
        FROM achievements 
        WHERE user_id = ?
        ''', (user_id,))
        achievements = cursor.fetchall()

        return {
            "user_id": user[0],
            "username": user[1],
            "tests_completed": user[4],
            "highest_level": user[5],
            "achievements": achievements
        }


def unlock_achievement(user_id: int, name: str, description: str):
    """Разблокировка достижения"""
    with sqlite3.connect('english_test.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        INSERT OR IGNORE INTO achievements (user_id, name, description, unlocked, date_unlocked)
        VALUES (?, ?, ?, TRUE, ?)
        ''', (user_id, name, description, datetime.now()))
        conn.commit()


def check_achievements(user_id: int):
    """Проверка и разблокировка достижений"""
    stats = get_user_stats(user_id)
    if not stats:
        return

    for achievement in ACHIEVEMENTS:
        if achievement["condition"](stats):
            unlock_achievement(
                user_id,
                achievement["name"],
                achievement["description"]
            )


# ========== FSM СОСТОЯНИЯ ==========
class TestStates(StatesGroup):
    IN_TEST = State()


# ========== ОБРАБОТЧИКИ КОМАНД ==========
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    add_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )
    await message.answer(
        "🇬🇧 *English Level Test Bot*\n\n"
        "🔹 /test – Начать тест (10 случайных вопросов)\n"
        "🔹 /profile – Мой прогресс\n"
        "🔹 /top – Топ игроков"
    )


@dp.message(Command("test"))
async def cmd_test(message: types.Message, state: FSMContext):
    """Обработчик команды /test"""
    await state.set_state(TestStates.IN_TEST)
    await state.update_data(
        questions=random.sample(QUESTIONS, 10),
        current_question=0,
        score=0
    )
    await send_question(message, state)


async def send_question(message: types.Message, state: FSMContext):
    """Отправка вопроса пользователю"""
    data = await state.get_data()
    question = data["questions"][data["current_question"]]

    keyboard = ReplyKeyboardMarkup(
        keyboard=[[option] for option in question["options"]],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer(
        f"❓ *Вопрос {data['current_question'] + 1}/10*\n\n"
        f"{question['question']}",
        reply_markup=keyboard
    )


@dp.message(TestStates.IN_TEST)
async def process_answer(message: types.Message, state: FSMContext):
    """Обработка ответа пользователя"""
    data = await state.get_data()
    question = data["questions"][data["current_question"]]

    if message.text == question["correct_answer"]:
        await message.answer("✅ Верно!")
        await state.update_data(score=data["score"] + 1)
    else:
        await message.answer(f"❌ Неверно! Правильно: {question['correct_answer']}")

    if data["current_question"] + 1 >= 10:
        await finish_test(message, state)
    else:
        await state.update_data(current_question=data["current_question"] + 1)
        await send_question(message, state)


async def finish_test(message: types.Message, state: FSMContext):
    """Завершение теста и вывод результатов"""
    data = await state.get_data()
    score = data["score"]
    level = calculate_level(score)

    update_test_result(message.from_user.id, score, 10, level)
    check_achievements(message.from_user.id)

    await message.answer(
        f"🎉 *Тест завершен!*\n\n"
        f"🔹 Правильных ответов: *{score}/10*\n"
        f"🔹 Ваш уровень: *{level}*\n\n"
        f"📊 Посмотреть профиль: /profile",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.clear()


def calculate_level(score: int) -> str:
    """Определение уровня по количеству баллов"""
    if score < 4:
        return "A1"
    elif 4 <= score < 7:
        return "A2"
    elif 7 <= score < 9:
        return "B1"
    else:
        return "B2"


@dp.message(Command("profile"))
async def cmd_profile(message: types.Message):
    """Обработчик команды /profile"""
    stats = get_user_stats(message.from_user.id)
    if not stats:
        await message.answer("Сначала пройдите тест: /test")
        return

    achievements_text = "\n".join(
        f"{'✅' if ach[2] else '❌'} {ach[0]} - {ach[1]}"
        for ach in stats["achievements"]
    ) if stats["achievements"] else "Пока нет достижений"

    await message.answer(
        f"📊 *Ваш профиль*\n\n"
        f"🔹 Тестов пройдено: *{stats['tests_completed']}*\n"
        f"🔹 Макс. уровень: *{stats['highest_level']}*\n\n"
        f"🏆 *Достижения:*\n{achievements_text}"
    )


@dp.message(Command("top"))
async def cmd_top(message: types.Message):
    """Обработчик команды /top"""
    with sqlite3.connect('english_test.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
        SELECT username, highest_level, tests_completed
        FROM users
        ORDER BY 
            CASE highest_level
                WHEN 'C2' THEN 6
                WHEN 'C1' THEN 5
                WHEN 'B2' THEN 4
                WHEN 'B1' THEN 3
                WHEN 'A2' THEN 2
                WHEN 'A1' THEN 1
                ELSE 0
            END DESC,
            tests_completed DESC
        LIMIT 10
        ''')
        top_users = cursor.fetchall()

    response = "🏆 *Топ-10 игроков*\n\n"
    for i, (username, level, tests) in enumerate(top_users, 1):
        response += f"{i}. {username or 'Аноним'} - {level} ({tests} тестов)\n"

    await message.answer(response)


# ========== ЗАПУСК БОТА ==========
async def main():
    """Основная функция запуска бота"""
    init_db()  # Инициализация базы данных
    await dp.start_polling(bot)


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())