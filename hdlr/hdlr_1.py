from datetime import datetime
import openai
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject
from PIL import Image
import io
from config_gemini import ConfigBox
#from assistants_request import assistant_run
#from openai import AsyncOpenAI

router = Router()

# Хэндлер на команду /test1
@router.message(Command("role"))
async def set_assistant_instructions(
            message: Message,
            command: CommandObject
    ):

    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer(
            "Ошибка: не переданы аргументы"
        )
        return
    # Пробуем разделить аргументы на две части по первому встречному пробелу
    try:
        #open_ai_role_dict[str(message.chat.id)] = command.args
        ConfigBox.set_dialog_instructions(str(message.chat.id), command.args)
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(
            "Ошибка: неправильный формат команды. Пример:\n"
            "/role <Описание роли>"
        )
        return
    await message.answer(
        "Роль установлена!\n"
        f"Текст: {command.args}"
    )

@router.message(F.text)
async def message_with_text(message: Message, bot: Bot):
    
    #query = message.text.replace('"', '^')
    query = message.text.replace('"', '^')

    words = query.split()

    # Make the desired change to the first word
    flag = False
    for _ in words :
        if _[0] == '@' : 
            flag = True
    
    if flag is False :

        response = ConfigBox.model.generate_content(message.text, stream=True)

        final_response = ''
        for _ in response:
            final_response += _.text
        chat_id = str(message.chat.id)
        user_id = message.from_user.id
        use_date = str(datetime.now())

        ConfigBox.update_dialog(chat_id, message.text)
        params = (chat_id, user_id, use_date, "gemini", message.text, _, 0, 0, 0)
        ConfigBox.dbase.execute('insert into tbl_ya_gpt_log values (?,?,?,?,?,?,?,?,?)', params)
        ConfigBox.dbase.commit()

        await message.answer(final_response)
    else : 
        await message.answer("Я молчу...")
    
@router.edited_message(F.text)
async def edited_message_with_text(message: Message):
    
    query = message.text.replace('"', '^')

    words = query.split()

    # Make the desired change to the first word
    flag = False
    for _ in words :
        if _[0] == '@' : 
            flag = True
    
    if flag is False :

        response = ConfigBox.client.images.generate(
        model="dall-e-3",
        prompt=message.text,
        size="1024x1024",
        quality="standard",
        n=1,
        )

        image_url = response.data[0].url
        chat_id = str(message.chat.id)
        user_id = message.from_user.id
        use_date = str(datetime.now())

        ConfigBox.update_dialog(chat_id, message.text)
        params = (chat_id, user_id, use_date, "imagination", message.text, _, 0, 0, 0)
        ConfigBox.dbase.execute('insert into tbl_ya_gpt_log values (?,?,?,?,?,?,?,?,?)', params)
        ConfigBox.dbase.commit()

        await message.answer(f"Картинка сгенерирована:\n{image_url}")
    else : 
        await message.answer("Я молчу...")

@router.edited_message(F.text)
async def edited_message_with_text(message: Message):
    
    await message.answer("Message is edited...")

@router.message(F.animation)
async def echo_gif(message: Message):
    await message.reply_animation(message.animation.file_id)

@router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer("Это стикер!")

@router.message(F.photo)
async def message_with_photo(message: Message):

    # Read the image file from disk and resize it
    #image = Image.open("image.png")
    photo_bytes_io = io.BytesIO()

    await message.bot.download(file=message.photo[-1].file_id, destination=photo_bytes_io)

    # Download the photo in bytes format
    
    #await photo.download(destination=photo_bytes_io)
    #photo_bytes_io.seek(0)

    image = Image.open(photo_bytes_io)
    #image = Image(photo)
    width, height = 1024, 1024
    image = image.resize((width, height))

    # Convert the image to a BytesIO object
    byte_stream = io.BytesIO()
    image.save(byte_stream, format='PNG')
    byte_array = byte_stream.getvalue()

    try: 
        response = ConfigBox.client.images.create_variation(
            image=byte_array,
            n=1,
            model="dall-e-2",
            size="1024x1024"
            )

        image_url = response.data[0].url
        chat_id = str(message.chat.id)
        user_id = message.from_user.id
        use_date = str(datetime.now())

        ConfigBox.update_dialog(chat_id, message.text)
        params = (chat_id, user_id, use_date, "imagination", "variation", "variation", 0, 0, 0)
        ConfigBox.dbase.execute('insert into tbl_ya_gpt_log values (?,?,?,?,?,?,?,?,?)', params)
        ConfigBox.dbase.commit()

        await message.answer(f"Картинка сгенерирована:\n{image_url}")
    except openai.OpenAIError as e:
        ConfigBox.logger.error(e)

@router.message(F.document)
async def message_with_document(message: Message):
    file_id = message.document.file_id
    await message.answer(f"Это document! {file_id}")