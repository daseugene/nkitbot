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


class AfterAuth_Student:
    @staticmethod
    def student_authorized():
        pass
