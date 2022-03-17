from aiogram.types import User, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from asgiref.sync import sync_to_async

from database import DBCommands
from keyboards.inline.choice_button import choice
from main import bot, dp
from config import admin_id
from aiogram.dispatcher.filters import Command
from aiogram import types

from aiogram.dispatcher import FSMContext

from quiz.models import Survey
from states.test import Test


async def send_to_admin(*args):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")


@dp.message_handler(Command("start"))
async def enter_start(message: types.Message):
    me = types.User.get_current()
    dbcommands = DBCommands()
    await dbcommands.add_new_user()
    print(User)
    text = f"Привет,  {await message.reply(text='jhgj')}"
    await message.answer(text=text,
                         reply_markup=choice)


@dp.message_handler(Command("test"), state=None)
async def enter_test(message: types.Message):
    #
    await message.answer("Вопрос №1. \n\n"
                         "Вы когда-нибудь пробовали программировать?",
                         reply_markup=choice)
    await Test.Q1.set()
    # Вариант 1 - с помощью функции сет


@dp.message_handler(Command("get_quizzes"), state=None)
async def enter_test(message: types.Message):
    surveys = await sync_to_async(list)(Survey.objects.all())
    choice_quiz = InlineKeyboardMarkup()
    for survey in surveys:
        choice_quiz.add(InlineKeyboardButton(text=survey.title, callback_data="get_quiz:" + str(survey.id)))
    await message.answer("Выберите quiz",
                         reply_markup=choice_quiz)


@dp.callback_query_handler(text_contains="get_quizzes")
async def enter_test(call: CallbackQuery):
    surveys = await sync_to_async(list)(Survey.objects.all())
    choice_quiz = InlineKeyboardMarkup()
    for survey in surveys:
        choice_quiz.add(InlineKeyboardButton(text=survey.title, callback_data="get_quiz:" + str(survey.id)))
    await call.message.answer("Выберите quiz",
                         reply_markup=choice_quiz)


questions = {"Q1": "Вопрос №1. \n\nВы когда-нибудь пробовали программировать?",
             "Q2": "Вопрос №2. \n\nВы получаете удовольствие от программирования?"}


@dp.callback_query_handler(text_contains="answer", state=Test)
async def parse_answer(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=1)
    old_full_state = await state.get_state()
    await call.message.edit_reply_markup(reply_markup=None)
    answer = call.data[7:]
    key = old_full_state[5:]
    await state.update_data(
        {key: answer}
    )
    dbcommands = DBCommands()
    await dbcommands.add_or_update_survey({key: answer})
    await Test.next()
    full_state = await state.get_state()
    if full_state is not None:
        id_question = full_state[5:]
        await call.message.answer(questions.get(id_question, "Данного вопроса не существует"),
                                  reply_markup=choice)
    else:
        await call.message.answer("Вы прошли тест!")

    # await call.message.answer("s")


# @dp.message_handler()
# async def echo(message: types.Message):
#    text = f"Привет, ты написал: {message.text}"
#    await message.reply(text=text)
@dp.callback_query_handler(text_contains="start_quiz:")
async def start_quiz(call: CallbackQuery):
    dbcommands = DBCommands()
    quiz_id = call.data[11:]
    quiz = await dbcommands.get_survey(quiz_id)
    message = "Извините, но такого квиза еще не существует"
    choice_quiz = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Выбрать другой квиз", callback_data="/get_quizzes"),
            ]
        ]
    )
    if quiz is not None:
        message = f"{quiz.title}\n\n{quiz.description}"
        choice_quiz.add(InlineKeyboardButton(text="Начать квиз", callback_data="startq:" + str(quiz.id)))
    await call.message.answer(message, reply_markup=choice_quiz)


@dp.callback_query_handler(text_contains="startq")
async def start_quiz(call: CallbackQuery):
    dbcommands = DBCommands()
    quiz_id = call.data[7:]
    quiz = await dbcommands.get_survey(quiz_id)
    question = await sync_to_async(quiz.questions.all().first)()
    choice_quiz = InlineKeyboardMarkup()
    answers = await sync_to_async(list)(question.answer.all())
    for answer in answers:
        choice_quiz.add(InlineKeyboardButton(text=answer.answer, callback_data=f"answer:{answer.id}"))
    if question.photo.name:

        await call.message.answer_photo(photo=InputFile(question.photo.path), caption=question, reply_markup=choice_quiz)
    elif question.video.name:
        await call.message.answer_video(video=InputFile(question.video.path), caption=question, reply_markup=choice_quiz)
    elif question.sound.name:
        await call.message.answer_audio(audio=InputFile(question.sound.path), caption=question, reply_markup=choice_quiz)
    else:
        await call.message.answer(text=question, reply_markup=choice_quiz)


@dp.callback_query_handler(text_contains="get_quiz:")
async def get_quiz(call: CallbackQuery):
    dbcommands = DBCommands()
    quiz_id = call.data[9:]
    quiz = await dbcommands.get_survey(quiz_id)
    message = "Извините, но такого квиза еще не существует"
    choice_quiz = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Выбрать другой квиз", callback_data="get_quizzes"),
            ]
        ]
    )
    if quiz is not None:
        message = f"{quiz.title}\n\n{quiz.description}"
        choice_quiz.add(InlineKeyboardButton(text="Начать квиз", callback_data="start_quiz:" + str(quiz.id)))
    await call.message.answer(message, reply_markup=choice_quiz)
