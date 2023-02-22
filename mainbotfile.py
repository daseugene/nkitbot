from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio

from services import StudentService, db_manager, TeacherService, AdminService
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

### ---- STUDENT ----
@dp.callback_query_handler(text='student')
async def student_authorized(query: types.CallbackQuery):
    await query.message.answer(
        "Выбрана роль СТУДЕНТ. Напиши номер своей группы!",
        
    )
    await query.message.delete()
    await StudentStates.student_authorization.set()

@dp.message_handler(state=StudentStates.student_authorization)
async def student_choosing_group(message: types.Message):
    await message.delete()
    print(message.text, message.from_user.id)
    await StudentService.init_student(message.text, message.from_user.id)
    await message.answer("Теперь нам известно, что ты студент группы " + message.text)
    await StudentStates.stud_ready_to_study.set()
    await message.answer("Чтобы продолжить работу в системе, отправьте любое сообщение в чат.")
    



@dp.message_handler(state=StudentStates.stud_ready_to_study)
async def stud_wyd(message: types.Message):
    await message.answer("Что будем делать?", reply_markup=keyboard.student_buttons)

@dp.callback_query_handler(state=StudentStates.stud_ready_to_study, text = 'student_schedule')
async def stud_schedule(query: types.CallbackQuery):
    await query.message.answer("Обрабатываем Ваш запрос...")
    await StudentStates.awaiting_schedule.set()

@dp.message_handler(state=StudentStates.awaiting_schedule)
async def get_schedule(message: types.Message):
    await StudentService.student_schedule(message.from_user.id)

    await StudentStates.stud_ready_to_study.set()


###----- TEACHER -------

@dp.callback_query_handler(text='teacher')
async def teacher_authorized(query: types.CallbackQuery):
    await query.message.reply(
        "Была выбрана роль ПРЕПОДАВАТЕЛЬ. Введите ключ авторизации!"    
    )
    await TeacherStates.awaiting_key.set()


@dp.message_handler(state=TeacherStates.awaiting_key)
async def teacher_authorized(message: types.Message):
    success = await TeacherService.check_code(
                                          message.text, )
    if not success:
        await message.reply(
            "Код недействителен"
        )
    else:
        await message.answer(
                "Добро пожаловать, " + message.from_user.full_name +
                " Если Вы согласны продолжать работу в системе НКИТ-БОТ, отправьте код повторно.",
                await TeacherStates.ready_to_work.set())      
        await TeacherService.init_teacher(
                                message.from_user.id, message.text)
                                             
    

@dp.message_handler(state=TeacherStates.ready_to_work)
async def t_wyd(message: types.Message):
    # await TeacherService.init_teacher(
    #                             message.from_user.id, message.text)
    await message.answer(
        "Что будем делать?",
        reply_markup=keyboard.teacher_buttons
        
        
    )



### ----- ADMIN -----
@dp.message_handler(state=AdminStates.awaiting_key)
async def admin_authorization(message: types.Message):
    success = await AdminService.check_admin_code(
                                          message.text
                                          )

    if success:
        await message.reply(
            "Добро пожаловать в систему, " + message.from_user.full_name
        )
    else:
        await message.reply("Код недействителен. ")

@dp.callback_query_handler(text='admin')
async def admin(query: types.CallbackQuery):
    await query.message.answer("""
                                Чтобы убедиться в том, что Вы АДМИН, введите код авторизации в чат.
                                """)
    await query.message.delete()

    await AdminStates.awaiting_key.set()


### ----- SYSTEM AND HELP BUTTONS ----


@dp.message_handler(commands=['about'])
async def process_about_command(message: types.Message):
    # РЕДАКТИРОВАТЬ
    await message.answer(
        ("Этот бот упростит твою учёбу."
         "Следить за обновлениями можно по ссылке: "),
        reply_markup=keyboard.help_buttons)

if __name__ == '__main__':
    print('Starting bot...')
    newfuture = asyncio.new_event_loop()
    asyncio.set_event_loop(newfuture)
    newfuture = asyncio.get_event_loop().run_until_complete(
        db_manager.first_time_init()
    )

    print('Testing database connection...')
    executor.start_polling(dp, skip_updates=True)
