from tkinter import Button
from urllib import request
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from pip import main



# -----Hello menu---- 

btnStudent = KeyboardButton('Студент')
btnTeacher = KeyboardButton('Преподаватель')
student_or_teacher = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnStudent, btnTeacher)


# ----LINKS------

btnLink = KeyboardButton('Ссылка на группу колледжа')


# ----After Hello----

btnGroups = KeyboardButton('Группа 1824')
btnGroups1 = KeyboardButton('1824к')
btnGroups2 = KeyboardButton('1924')
btnGroups3 = KeyboardButton('Не могу найти свою группу')
btnRasp = KeyboardButton('Узнать расписание')
afterhello = ReplyKeyboardMarkup(resize_keyboard=True).add(btnGroups)


Groups =  ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnGroups, btnGroups1, btnGroups2, btnGroups3)


raspkb = InlineKeyboardMarkup(row_width=1)
raspbutton = InlineKeyboardButton(text='Узнать расписание')
noraspbutton2 = InlineKeyboardButton(text='Не узнавать расписание')
raspkb.add(raspbutton, noraspbutton2)









