from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage


class AuthStates(StatesGroup):
    choosing_role = State()
    authorization = State()


class TeacherStates(StatesGroup):
    awaiting_key = State()


class AdminStates(StatesGroup):
    awaiting_key = State()
    choosing_user_for_add = State()
    choosing_user_for_delete = State()

    