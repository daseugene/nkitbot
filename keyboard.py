from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, InlineKeyboardButton


role_buttons = InlineKeyboardMarkup(row_width=1).row(
    *(
        InlineKeyboardButton(
            "Студент",
            callback_data='student'
        ),
        InlineKeyboardButton(
            "Преподаватель",
            callback_data='teacher'
        ),
        InlineKeyboardButton(
            "Админ",
            callback_data='admin'
        )
    )
)

# help buttons(link)

vk_group_button = InlineKeyboardButton("VK", url='https://vk.com/college89bot')


help_buttons = InlineKeyboardMarkup().add(vk_group_button)
