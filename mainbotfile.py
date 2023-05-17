from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio
from aiogram.types import Message, ContentType
from aiogram.dispatcher import FSMContext
import os

from services import StudentService, db_manager, TeacherService, AdminService, GetResult
import keyboard
from utils import TeacherStates, AdminStates, StudentStates



bot = Bot(token='5674127673:AAGiSaquLQYIfptAxU3fdrX2mxAOxIDtJ64')
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())
reply = GetResult.gett_result()



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
  #
    await StudentService.init_student(message.text, message.from_user.id)
    await message.answer("Теперь нам известно, что ты студент группы " + message.text)
    await StudentStates.stud_ready_to_study.set()
    await message.answer("Чтобы продолжить работу в системе, отправьте любое сообщение в чат.")
   # await get_schedule(group)
    



@dp.message_handler(state=StudentStates.stud_ready_to_study)
async def stud_wyd(message: types.Message):
    await message.answer("Что будем делать?", reply_markup=keyboard.student_buttons)

@dp.callback_query_handler(state=StudentStates.stud_ready_to_study, text='students_schedule')
async def stud_schedule(query: types.CallbackQuery):
    await query.message.answer("Обрабатываем Ваш запрос...")
    await StudentStates.awaiting_schedule.set()

@dp.message_handler(state=StudentStates.awaiting_schedule)
async def get_schedule(message: types.Message):
    await StudentService.student_schedule(message.from_user.id)

    await StudentStates.stud_ready_to_study.set()

@dp.callback_query_handler(text='student_schedule')
async def get_sche(query: types.CallbackQuery):
    await query.message.reply(
        "Введите интересующий день недели, на который хотите узнать расписание"
    )
    await StudentStates.get_sch_state.set()

@dp.message_handler(state=StudentStates.get_sch_state)
async def get_schedule(message: types.Message):
    success = await StudentService.get_schedule(message.text)
    if success:
        await message.reply(
            "Best",
           reply_markup=keyboard.student_buttons
        )
        await StudentStates.stud_ready_to_study.set()     
    else:
        await message.reply(reply)


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
    await TeacherService.finish_auth(
                                message.from_user.id)
    await message.answer(
        "Что будем делать?",
        reply_markup=keyboard.teacher_buttons
        
        
    )
    # await TeacherStates.ready_to_work.set()



### ----- ADMIN -----
@dp.callback_query_handler(text='admin')
async def teacher_authorized(query: types.CallbackQuery):
    await query.message.reply(
        "Была выбрана роль АДМИНИСТРАТОР. Введите ключ авторизации!"    
    )
    await AdminStates.awaiting_key.set()

@dp.message_handler(state=AdminStates.awaiting_key)
async def admin_authorization(message: types.Message):
    success = await AdminService.check_admin_code(
                                          message.text
                                          )
    if success:
        await message.reply(
            "Добро пожаловать в систему, " + message.from_user.full_name, reply_markup=keyboard.admin_buttons
        )
        await AdminStates.ready_to_work_admin.set()      
        
        await AdminService.final_auth(
                                message.from_user.id)
    else:
        await message.reply("Код недействителен. ")


SAVE_DIR = "pdf/files/"

@dp.callback_query_handler(text='upload_new_rasp')
async def transition_to_uploading(query: types.CallbackQuery):
    await AdminStates.waiting_for_file.set()
    await query.message.reply("Отправьте любое сообщение в чат.")



@dp.message_handler(content_types=ContentType.DOCUMENT, state=AdminStates.waiting_for_file)
async def handle_pdf(message: types.Message):
    if message.document.mime_type == "application/pdf":
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
            file_path = f"{SAVE_DIR}{message.document.file_name}"
            await message.document.download(file_path)

            await message.answer(f"Файл {message.document.file_name} сохранен в {SAVE_DIR}")
            await AdminStates.ready_to_work_admin.set()


@dp.message_handler(commands=['parse_pdf'])
async def send_pdf_content(message: types.Message):
    # Открываем файл и создаем объект pdfReader
    pdfFileObj = open('grps.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # Получаем количество страниц в документе
    num_pages = pdfReader.numPages

    # Читаем содержимое каждой страницы и добавляем в переменную text
    text = ""
    for page in range(num_pages):
        pageObj = pdfReader.getPage(page)
        text += pageObj.extractText()

    # Закрываем файл
    pdfFileObj.close()

    # Отправляем содержимое в сообщении пользователю
    await bot.send_message(message.chat.id, text)





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
