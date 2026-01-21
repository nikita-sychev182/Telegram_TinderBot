
# Утилитарные функции для работы с Telegram Bot API и форматирования сообщений
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    BotCommand,
    MenuButtonCommands,
    BotCommandScopeChat,
    MenuButtonDefault,
    Update
)
# Импорты из библиотеки python-telegram-bot для работы с Telegram Bot API
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


# Преобразует информацию о пользователе диалога в строку
def dialog_user_info_to_str(user) -> str:
    result = ""
    map = {
        "name": "Имя",
        "sex": "Пол",
        "age": "Возраст",
        "city": "Город",
        "occupation": "Профессия",
        "hobby": "Хобби",
        "goals": "Цели знакомства",
        "handsome": "Красота, привлекательность в баллах (максимум 10 баллов)",
        "wealth": "Доход, богатство",
        "annoys": "В людях раздражает",
    }
    # Строка, а не к примеру json, чтобы проще было вставлять в промпт
    for key, name in map.items():
        if key in user:
            result += name + ": " + user[key] + "\n"
    return result


# Отправляет в чат текстовое сообщение с разметкой markdown
# предназначение данной функции - корректная отправка символов вне BMP (эмодзи и др.)
async def send_text(
    update: Update, context: ContextTypes.DEFAULT_TYPE, text: str
) -> Message:
    # Проверка на корректность markdown (четное число символов "_")
    if text.count("_") % 2 != 0:
        message = f"Строка '{text}' является невалидной с точки зрения markdown. Воспользуйтесь методом send_html()"
        print(message)
        return await update.message.reply_text(message)
    
    # кодировка для корректного отображения символов вне BMP
    text = text.encode("utf16", errors="surrogatepass").decode("utf16")
    
    # отправка сообщения с указанием parse_mode=MARKDOWN
    return await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.MARKDOWN
    )


# Отправляет в чат HTML сообщение
# предназначение данной функции - корректная отправка текста с HTML разметкой и символов вне BMP (эмодзи и др.)
async def send_html(
    update: Update, context: ContextTypes.DEFAULT_TYPE, text: str
) -> Message:
    text = text.encode("utf16", errors="surrogatepass").decode("utf16")
    return await context.bot.send_message(
        chat_id=update.effective_chat.id, text=text, parse_mode=ParseMode.HTML
    )


# Отправляет в чат текстовое сообщение с кнопками
# Кнопки реализованы с помощью InlineKeyboardMarkup и InlineKeyboardButton библиотеки python-telegram-bot
async def send_text_buttons(
    update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, buttons: dict
) -> Message:
    text = text.encode("utf16", errors="surrogatepass").decode("utf16")
    keyboard = []
    for key, value in buttons.items():
        button = InlineKeyboardButton(str(value), callback_data=str(key))
        keyboard.append([button])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return await update.message.reply_text(
        text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN
    )


#  Отправляет в чат фото из папки /resources/images/
# Предназначение данной функции - централизовать путь к ресурсам
async def send_photo(
    update: Update, context: ContextTypes.DEFAULT_TYPE, name: str
) -> Message:
    with open("resources/images/" + name + ".jpg", "rb") as photo:
        return await context.bot.send_photo(
            chat_id=update.effective_chat.id, photo=photo
        )


# Реализация меню бота с командами в левом нижнем углу чата
# Реализованы с помощью BotCommand, BotCommandScopeChat и MenuButtonCommands библиотеки python-telegram-bot
async def show_main_menu(
    update: Update, context: ContextTypes.DEFAULT_TYPE, commands: dict
):
    command_list = [BotCommand(key, value) for key, value in commands.items()]
    await context.bot.set_my_commands(
        command_list, scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
    )
    await context.bot.set_chat_menu_button(
        menu_button=MenuButtonCommands(), chat_id=update.effective_chat.id
    )


# Скрывает меню бота в левом нижнем углу чата
# В основной логике бота меню не используется, сделана на случай если понадобится
async def hide_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.delete_my_commands(
        scope=BotCommandScopeChat(chat_id=update.effective_chat.id)
    )
    await context.bot.set_chat_menu_button(
        menu_button=MenuButtonDefault(), chat_id=update.effective_chat.id
    )


# Загружает сообщение из папки  /resources/messages/
def load_message(name):
    with open("resources/messages/" + name + ".txt", "r", encoding="utf8") as file:
        return file.read()


# Загружает промпт из папки /resources/prompts/
def load_prompt(name):
    with open("resources/prompts/" + name + ".txt", "r", encoding="utf8") as file:
        return file.read()

# Определение класса Dialog для использования в bot.py
class Dialog:
    pass
