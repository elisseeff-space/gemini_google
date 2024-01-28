from aiogram import Router, F
from random import randint
from aiogram import types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ParseMode
from config_gemini import ConfigBox, ChatAI_ModelType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
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
    builder = ReplyKeyboardBuilder()
    
    builder.row(types.KeyboardButton(text="The PaLM 2 for Chat (chat-bison)"), types.KeyboardButton(text="Codey for Code Completion (code-gecko)")),
    builder.row(types.KeyboardButton(text="Codey for Code Chat (codechat-bison)"), types.KeyboardButton(text="Codey for Code Generation (code-bison)")),
    builder.add(types.KeyboardButton(text="Show Model in use!"))
    builder.adjust(2)

    keyboard = builder.as_markup(resize_keyboard=True,
                                 input_field_placeholder="Выберите модель нейросети, с которой будем общаться.")

    await message.answer("Здесь можно выбрать модель нейросети, с которой будем общаться.", reply_markup=keyboard)

@router.message(F.text == "The PaLM 2 for Chat (chat-bison)")
async def palm_2_for_chat(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Select the model The PaLM 2 for Chat (chat-bison)",
        callback_data=ChatAI_ModelType.PALM_2_CHAT.value)
    )
    await message.answer(
        "Нажмите на кнопку, чтобы Select the model The PaLM 2 for Chat (chat-bison)",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == ChatAI_ModelType.PALM_2_CHAT.value)
async def set_palm_2_chat_model(callback: types.CallbackQuery):
    await callback.message.answer(f'Model {ChatAI_ModelType.PALM_2_CHAT.value} selected!')
    chat_id = str(callback.message.chat.id)
    ConfigBox.chat_ai_model[chat_id] = ChatAI_ModelType.PALM_2_CHAT
    await callback.answer(
        text=f'Model {ChatAI_ModelType.PALM_2_CHAT.value} selected!',
        show_alert=True
    )

@router.message(F.text == "Codey for Code Chat (codechat-bison)")
async def codey_for_code_chat(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Select the model Codey for Code Chat (codechat-bison)",
        callback_data=ChatAI_ModelType.CODE_CHAT.value)
    )
    await message.answer(
        "Нажмите на кнопку, чтобы Select the model Codey for Code Chat (codechat-bison)",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == ChatAI_ModelType.CODE_CHAT.value)
async def set_codey_for_code_chat_model(callback: types.CallbackQuery):
    await callback.message.answer(f'Model {ChatAI_ModelType.CODE_CHAT.value} selected!')
    chat_id = str(callback.message.chat.id)
    ConfigBox.chat_ai_model[chat_id] = ChatAI_ModelType.CODE_CHAT
    await callback.answer(
        text=f'Model {ChatAI_ModelType.CODE_CHAT.value} selected!',
        show_alert=True
    )

@router.message(F.text == "Codey for Code Completion (code-gecko)")
async def codey_for_chat_completion(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Select the model Codey for Code Completion (code-gecko)",
        callback_data=ChatAI_ModelType.CODE_COMPLETION.value)
    )
    await message.answer(
        "Нажмите на кнопку, чтобы Select the model Codey for Code Completion (code-gecko)",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == ChatAI_ModelType.CODE_COMPLETION.value)
async def set_code_complition_model(callback: types.CallbackQuery):
    await callback.message.answer(f'Model {ChatAI_ModelType.CODE_COMPLETION.value} selected!')
    chat_id = str(callback.message.chat.id)
    ConfigBox.chat_ai_model[chat_id] = ChatAI_ModelType.CODE_COMPLETION
    await callback.answer(
        text=f'Model {ChatAI_ModelType.CODE_COMPLETION.value} selected!',
        show_alert=True
    )

@router.message(F.text == "Codey for Code Generation (code-bison)")
async def codey_for_code_chat_generation(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Select the model Codey for Code Generation (code-bison)",
        callback_data=ChatAI_ModelType.CODE_GENERATION.value)
    )
    await message.answer(
        "Нажмите на кнопку, чтобы Select the model Codey for Code Generation (code-bison)",
        reply_markup=builder.as_markup()
    )

@router.callback_query(F.data == ChatAI_ModelType.CODE_GENERATION.value)
async def set_codey_for_code_chat_generation_model(callback: types.CallbackQuery):
    await callback.message.answer(f'Model {ChatAI_ModelType.CODE_GENERATION.value} selected!')
    chat_id = str(callback.message.chat.id)
    ConfigBox.chat_ai_model[chat_id] = ChatAI_ModelType.CODE_GENERATION
    await callback.answer(
        text=f'Model {ChatAI_ModelType.CODE_GENERATION.value} selected!',
        show_alert=True
    )

@router.message(F.text == "Show Model in use!")
async def show_model_in_use(message: types.Message):
    chat_id = str(message.chat.id)
    if chat_id not in ConfigBox.chat_ai_model.keys() : ConfigBox.create_dialog(chat_id)
    await message.answer(f"Now run: {ConfigBox.chat_ai_model[chat_id].value}!")