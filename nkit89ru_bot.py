from ast import Lambda
from email import message_from_string
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.utils.markdown import text
from aiogram.dispatcher import Dispatcher
import keyboard as kb
import logging
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


bot = Bot(token="5674127673:AAGiSaquLQYIfptAxU3fdrX2mxAOxIDtJ64")
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

async def on_startup():
    print("Онлайн")


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    await message.reply("Привет! Вы студент или преподаватель?", reply_markup=kb.student_or_teacher)



@dp.message_handler()
async def bot_message(message: types.Message):
   try: 
       if message.text == "Студент":
           await message.reply("В какой группе Вы учитесь?", reply_markup=kb.Groups)
           if message.text =="Группа 1824":
               await message.reply("НАКОНЕЦ-ТО", reply_markup="kb.raspkb")
           else:
               print('jopa')
       elif message.text == "Преподаватель":
           await message.reply("На данный момент программная часть для преподавателей находится в разработке")
   except:
        print("aaaaaa")


@dp.message_handler()
async def botgroup(message: types.Message):
    
    print("Start?")
    

#@dp.message_handler()
#async def botgroup(message: types.Message):
    
 #   if message.text == "1824":
  #      await message.reply("Вы успешно зарегистрированы в системе", reply_markup=kb.raspkb)
      #  dp.register_callback_query_handler(bot_helper)
 #   elif message.text == "1924" or "Не могу найти свою группу":
    #    await message.reply("Возможно, Ваша группа пока не добавлена в систему. Повторите попытку позже.")
   #     dp.register_callback_query_handler(bot_helper)          
   # else:
        


@dp.message_handler(content_types = ["text", "numbers"])
async def bot_helper(message: types.Message):
    await message.reply('Чем могу помочь?', reply_markup=kb.Navigation)
    dp.register_callback_query_handler(bot_mainhelper)


@dp.message_handler()
async def bot_mainhelper(message: types.Message):
    await message.answer("В какой группе Вы учитесь?", reply_markup=kb.Groups)
    if message.text == "Узнать расписание":
        await message.reply('   ')
        dp.register_callback_query_handler()














help_message = text(
    "Это урок по клавиатурам.",
    "Доступные команды:\n",
    "/start - приветствие",
    sep="\n"
)




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
