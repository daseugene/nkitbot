from tkinter import Button
from urllib import request
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from pip import main


btnGroups = KeyboardButton('������ 1824')
btnGroups1 = KeyboardButton('1824�')
btnGroups2 = KeyboardButton('1924')
btnGroups3 = KeyboardButton('�� ���� ����� ���� ������')
btnRasp = KeyboardButton('������ ����������')
afterhello = ReplyKeyboardMarkup(resize_keyboard=True).add(btnGroups)


Groups =  ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnGroups, btnGroups1, btnGroups2, btnGroups3)


raspkb = InlineKeyboardMarkup(row_width=3,
                             inline_keyboard= [
                                  [
                                      InlineKeyboardButton(text='������?', callback_data='Message'),
                                      InlineKeyboardButton(text='�� ������?', callback_data='No message')
                                      ]

                                  ])
raspbutton = InlineKeyboardButton(text="HAHAHA")
noraspbutton2 = InlineKeyboardButton(text="HAHAHA")
raspkb.add(raspbutton, noraspbutton2)