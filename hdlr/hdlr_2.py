from aiogram import Router, F
from random import randint
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from config_gemini import ConfigBox
from aiogram.utils.formatting import (
    Bold, as_list, as_marked_section, as_key_value, HashTag
)

router = Router()

# Хэндлер на команду /help
@router.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = "\n "
    help_text += ""
    help_text += "\n"
    help_text += ""
    content = as_list(
        as_marked_section(
            Bold("Иструкция по применению!"),
            as_key_value("Всего три правила использования бота", 3),
            marker="  ",
        ),
        as_marked_section(
            Bold("1. Пишете в сообщении описание того, что надо нарисовать и я нарисую."),
            "Например, нарисуй котика на полянке, играющего с мячиком.",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("2. Если бот добавлен в группу, и нужно чтобы он проигнорировал сообщение, то есть НЕ отвечал на него, надо добавить символ @ в сообщение."),
            "Например, адресно обратиться к одному из участников.\n Тогда бот не будет мешать своими ответами.",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("3. Если отправить боту картинку, то он перерисует её."),
            "Например, если хотите увидеть что-то новое в старом изображении.",
            marker="✅ ",
        ),
        HashTag("#OpenAI Imagination"),
        sep="\n\n",
    )
    await message.reply(**content.as_kwargs())

@router.message(Command("control"))
async def cmd_control(message: types.Message):
    for _ in ConfigBox.dialog_messages.keys() :
        await message.answer(f"In chat {_}: {len(ConfigBox.dialog_messages[_])} messages.\n")
        