from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio

from services import StudentService, db_manager, TeacherService
import keyboard
from utils import TeacherStates, AdminStates, StudentStates


bot = Bot(token='5674127673:AAGiSaquLQYIfptAxU3fdrX2mxAOxIDtJ64')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'], state=None)
async def command_start(message: types.Message):

    await message.reply(
        "Привет. Выбери свою роль: ",
        reply_markup=keyboard.role_buttons
    )


@dp.callback_query_handler(text='student')
async def student_authorized(query: types.CallbackQuery):
    await query.message.answer(
        "Напиши номер своей группы!"
    )
    await StudentStates.student_authorization.set()
 

@dp.message_handler(state=StudentStates.student_authorization)
async def student_choosing_group(message: types.Message):
    print(message.text, message.from_user.id)
    await StudentService.init_student(message.text, message.from_user.id)




# @dp.message_handler(state='student_authorization')
# async def studentis(message: types.Message):
    


@dp.callback_query_handler(text='teacher')
async def teacher_authorized(query: types.CallbackQuery):
    await query.message.reply(
        "Введите ключ авторизации!"
    )
    teacher_id = query.from_user.id
    teacher_name = query.from_user.full_name

    print("Выбрал(а) роль преподавателя: ", teacher_name, "ID: ", teacher_id)
    await TeacherStates.awaiting_key.set()


@dp.message_handler(state=TeacherStates.awaiting_key)
async def teacher_authorized(message: types.Message):
    success = await TeacherService.init_teacher(
                                          message.from_user.id,
                                          message.text)
    key = message.text 
    print(message.from_user.full_name, "input", key)
    if success:
        await message.reply(
            "Авторизация прошла успешно"
        )
    else:
        await message.reply(
            "Код недействителен"
        )
    


# @dp.message_handler(state=AdminStates.awaiting_key)
# async def admin_authorization(message: types.Message):
#     success = await UserService.init_user('admin',
#                                           message.from_user.id,
#                                           message.text
#                                           )

#     if success:
#         await message.reply(
#             "Добро пожаловать в систему, ", message.from_user.full_name
#         )
#     else:
#         await message.reply("Код недействителен. ")


@dp.message_handler(commands=['about'])
async def process_about_command(message: types.Message):
    # РЕДАКТИРОВАТЬ
    await message.answer(
        ("Этот бот упростит твою учёбу."
         "Следить за обновлениями можно по ссылке: "),
        reply_markup=keyboard.help_buttons)

# @dp.message_handler()
# async def after_autorization(message: types.Message):
 #   await message.reply("Напиши номер своей группы, студент!")


if __name__ == '__main__':
    print('Starting bot...')
    newfuture = asyncio.new_event_loop()
    asyncio.set_event_loop(newfuture)
    newfuture = asyncio.get_event_loop().run_until_complete(
        db_manager.first_time_init()
    )

    print('Testing database connection...')
    executor.start_polling(dp, skip_updates=True)
