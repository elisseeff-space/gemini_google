from aiogram import Router
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
    help_text = "Инструкция по применению!\n"
    help_text += "Всего три правила использования бота\n\n"
    help_text += "1. The PaLM 2 for Chat (chat-bison) foundation model is a large language model (LLM) that excels at language understanding, language generation, and conversations. This chat model is fine-tuned to conduct natural multi-turn conversations, and is ideal for text tasks about code that require back-and-forth interactions.\n\n"
    help_text += "2. Command /role - Context shapes how the model responds throughout the conversation. For example, you can use context to specify words the model can or cannot use, topics to focus on or avoid, or the response format or style.\n\n"
    help_text += "3. Боту можно зхадать примеры вопроса и ответа\nCommand /example - Examples for the model to learn how to respond to the conversation.\n\n3.1/examplein [Text of question]\n\n3.2/exampleout [Text of answer]\n"
    help_text += "#Google #Gemini"
    await message.answer(help_text)

@router.message(Command("control"))
async def cmd_control(message: types.Message):
    for _ in ConfigBox.dialog_messages.keys() :
        await message.answer(f"In chat {_}: {len(ConfigBox.dialog_messages[_])} messages.\n")

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="С пюрешкой")],
        [types.KeyboardButton(text="Без пюрешки")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)
