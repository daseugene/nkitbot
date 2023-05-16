from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, InlineKeyboardButton


role_buttons = InlineKeyboardMarkup(row_width=1).row(
    *(
        InlineKeyboardButton(
            "Студент",
            callback_data='student'
        ),
        # InlineKeyboardButton(
        #     "Преподаватель",
        #     callback_data='teacher'
        # ),
        InlineKeyboardButton(
            "Админ",
            callback_data='admin'
        )
    )
)


student_buttons = InlineKeyboardMarkup(row_width=1).row(
    *(
        InlineKeyboardButton(
            "Расписание", 
            callback_data='student_schedule'
        ),
        InlineKeyboardButton(
            "Группа ВК",
            callback_data='attention'
        ),
        InlineKeyboardButton(
            "Погода",
            callback_data='weather'
        )
    )
)

teacher_buttons = InlineKeyboardMarkup(row_width=1).row(
    *(
        InlineKeyboardButton(
            "Посмотреть расписание", callback_data='schedule'
        ),
        InlineKeyboardButton(
            "Объявление",
            callback_data='attention'
        ),
        InlineKeyboardButton(
            "Погода",
            callback_data='weather'
        )
    )
)

admin_buttons = InlineKeyboardMarkup(row_width=1).row(
    *(
        InlineKeyboardButton(
            "Обновить расписание", callback_data='upload_new_rasp'
        ),
        InlineKeyboardButton(
            "Объявление",
            callback_data='attention'
        ),
        InlineKeyboardButton(
            "Погода",
            callback_data='weather'
        )
    )
)


# help buttons(link)

vk_group_button = InlineKeyboardButton("VK", url='https://vk.com/college89bot')


help_buttons = InlineKeyboardMarkup().add(vk_group_button)
