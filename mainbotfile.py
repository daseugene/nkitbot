from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio
from aiogram.types import Message, ContentType
from aiogram.dispatcher import FSMContext
import os

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
    await StudentStates.stud_ready_to_study.set()
    await message.answer("Теперь мы узнали из какой ты группы. Чтобы продолжить работу в системе, отправьте любое сообщение в чат.")



@dp.message_handler(state=StudentStates.stud_ready_to_study)
async def stud_wyd(message: types.Message):
    await message.answer("Что будем делать?", reply_markup=keyboard.student_buttons)

@dp.callback_query_handler(text='student_schedule')
async def get_sche(query: types.CallbackQuery):
    await query.message.reply(
        "Введите интересующий день недели, на который хотите узнать расписание"
    )
    await StudentStates.get_sch_state.set()

@dp.message_handler(state=StudentStates.get_sch_state)
async def get_schedule(message: types.Message):
    reply = await StudentService.get_schedule(message.text)
    await message.reply(reply)
    await StudentStates.stud_ready_to_study.set()
    await message.reply("Что будем делать?", reply_markup=keyboard.student_buttons)


###----- TEACHER -------

# @dp.callback_query_handler(text='teacher')
# async def teacher_authorized(query: types.CallbackQuery):
#     await query.message.reply(
#         "Была выбрана роль ПРЕПОДАВАТЕЛЬ. Введите ключ авторизации!"    
#     )
#     await TeacherStates.awaiting_key.set()


# @dp.message_handler(state=TeacherStates.awaiting_key)
# async def teacher_authorized(message: types.Message):
#     success = await TeacherService.check_code(
#                                           message.text, )
#     if not success:
#         await message.reply(
#             "Код недействителен"
#         )
#     else:
#         await message.answer(
#                 "Добро пожаловать, " + message.from_user.full_name +
#                 " Если Вы согласны продолжать работу в системе НКИТ-БОТ, отправьте код повторно.",
#                 await TeacherStates.ready_to_work.set())      
#         await TeacherService.init_teacher(
#                                 message.from_user.id, message.text)
                                             
    

# @dp.message_handler(state=TeacherStates.ready_to_work)
# async def t_wyd(message: types.Message):
#     await TeacherService.finish_auth(
#                                 message.from_user.id)
#     await message.answer(
#         "Что будем делать?",
#         reply_markup=keyboard.teacher_buttons
        
        
#     )
#     # await TeacherStates.ready_to_work.set()



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
    await query.message.reply("Отправьте документ с расписанием в чат.")

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@dp.callback_query_handler(text='attention')
async def ready_for_attention(query: types.CallbackQuery):
    await query.message.reply(
        "Введите ваше объявление"
    )
    await AdminStates.ready_to_create_attention.set()

@dp.message_handler(state=AdminStates.ready_to_create_attention)
async def create_attention(message: types.Message):
    await AdminService.delete_old_attention()
    await AdminService.create_attention(message.from_user.id, message.text)
    await message.reply(
            "Сообщение было создано, кому его отправим?", reply_markup=keyboard.admin_attention_buttons 
        )   

@dp.callback_query_handler(text='all_users')
async def send_attention_to_all(query: types.CallbackQuery):
    list = await AdminService.send_attention_to_all()
    print(list)
    message_to_users = await AdminService.get_last_attention()

    pre_attention = "ОБЪЯВЛЕНИЕ ОТ АДМИНИСТРАЦИИ: "
    attention = pre_attention + message_to_users
    for user_id in list:
        message = types.Message(text=attention, chat=user_id)
        await bot.send_message(chat_id=user_id, text=attention)


#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

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


if __name__ == '__main__':
    print('Starting bot...')
    newfuture = asyncio.new_event_loop()
    asyncio.set_event_loop(newfuture)
    newfuture = asyncio.get_event_loop().run_until_complete(
        db_manager.first_time_init()
    )

    print('Testing database connection...')
    executor.start_polling(dp, skip_updates=True)
