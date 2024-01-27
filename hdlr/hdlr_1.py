from datetime import datetime
from vertexai.language_models import ChatModel, InputOutputTextPair
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject
from config_gemini import ConfigBox

router = Router()

def code_chat_vertex(text_message: str, role: str, temperature: float = 0.2) -> None:
    chat_model = ChatModel.from_pretrained("chat-bison@001")

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }

    chat = chat_model.start_chat(
        context=role,
        examples=[
            InputOutputTextPair(
                input_text="not EXISTS how to use in sqlite3?",
                output_text="""To use the `NOT EXISTS` operator in sqlite3, you can use the following syntax:
```
NOT EXISTS (
  SELECT *
  FROM table_name
  WHERE condition
)""",
            ),
        ],
    )

    response = chat.send_message(
        text_message, **parameters
    )
    print(f"Response from Model: {response.text}")

    return response

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
    
    if flag : await message.answer("Я молчу...")
    else :
        response = code_chat_vertex(message.text, role=True)

        chat_id = str(message.chat.id)
        user_id = message.from_user.id
        use_date = str(datetime.now())

        ConfigBox.update_dialog(chat_id, 'user', message.text)
        params = (chat_id, user_id, use_date, "gemini", message.text, _, 0, 0, 0)
        ConfigBox.dbase.execute('insert into tbl_ya_gpt_log values (?,?,?,?,?,?,?,?,?)', params)
        ConfigBox.dbase.commit()

        ConfigBox.update_dialog(chat_id, 'vertex', response.text)
        params = (chat_id, user_id, use_date, "gemini", response.text, _, 0, 0, 0)
        ConfigBox.dbase.execute('insert into tbl_ya_gpt_log values (?,?,?,?,?,?,?,?,?)', params)
        ConfigBox.dbase.commit()

        await message.answer(response.text)
    
@router.edited_message(F.text)
async def edited_message_with_text(message: Message):
    
    query = message.text.replace('"', '^')

    words = query.split()

    # Make the desired change to the first word
    flag = False
    for _ in words :
        if _[0] == '@' : 
            flag = True
    
    if flag : await message.answer("Я молчу...")
    else :
        await message.answer(f"Message is edited:\n{message.message_id}") 
        
@router.message(F.animation)
async def echo_gif(message: Message):
    await message.reply_animation(message.animation.file_id)

@router.message(F.sticker)
async def message_with_sticker(message: Message):
    await message.answer("Это стикер!")

@router.message(F.photo)
async def message_with_photo(message: Message):
    await message.answer("Это photo!")

@router.message(F.document)
async def message_with_document(message: Message):
    file_id = message.document.file_id
    await message.answer(f"Это document! {file_id}")