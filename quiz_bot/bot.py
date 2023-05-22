import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.wsgi import get_wsgi_application
from quiz.models import Question
from quiz_bot import settings
import django
# Инициализация Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_bot.settings')

# Инициализация Django
django.setup()
application = get_wsgi_application()

# Инициализация бота и диспетчера
bot = Bot(token=settings.TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
# Определение состояний
class QuizState(StatesGroup):
    waiting_for_answer = State()


# Обработчик команды /start
@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Добро пожаловать в квиз!")
    await QuizState.waiting_for_answer.set()
    await message.answer("Ответьте на первый вопрос:")
@dp.message_handler(state=QuizState.waiting_for_answer)
async def process_answer(message: types.Message, state: FSMContext):
    user_answer = message.text.lower()
    
    # Проверка ответа
    try:
        question = Question.objects.get(answer=user_answer)
        await message.answer("Правильный ответ!")
    except ObjectDoesNotExist:
        await message.answer("Неправильный ответ!")
    
    # Переход к следующему вопросу
    await state.finish()
    await QuizState.waiting_for_answer.set()
    await message.answer("Ответьте на следующий вопрос:")