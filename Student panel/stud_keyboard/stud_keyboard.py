from tkinter import Button
from urllib import request
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from pip import main


btnGroups = KeyboardButton('Группа 1824')
btnGroups1 = KeyboardButton('1824к')
btnGroups2 = KeyboardButton('1924')
btnGroups3 = KeyboardButton('Не могу найти свою группу')
btnRasp = KeyboardButton('Узнать расписание')
afterhello = ReplyKeyboardMarkup(resize_keyboard=True).add(btnGroups)


Groups =  ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnGroups, btnGroups1, btnGroups2, btnGroups3)


raspkb = InlineKeyboardMarkup(row_width=3,
                             inline_keyboard= [
                                  [
                                      InlineKeyboardButton(text='Хочешь?', callback_data='Message'),
                                      InlineKeyboardButton(text='Не хочешь?', callback_data='No message')
                                      ]

                                  ])
raspbutton = InlineKeyboardButton(text="HAHAHA")
noraspbutton2 = InlineKeyboardButton(text="HAHAHA")
raspkb.add(raspbutton, noraspbutton2)