from datetime import datetime
from vertexai.language_models import ChatModel, CodeChatModel, CodeGenerationModel, InputOutputTextPair
from aiogram import Router, F, Bot
from aiogram.types import Message
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from config_gemini import ConfigBox, ChatAI_ModelType

router = Router()

def palm_2_chat_vertex(chat_id:str, text_message: str, role: str, temperature: float = 0.2) -> None:
    chat_model = ChatModel.from_pretrained("chat-bison@001")

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
        "top_p": 0.95,  # Tokens are selected from most probable to least until the sum of their probabilities equals the top_p value.
        "top_k": 40,  # A top_k of 1 means the selected token is the most probable among all tokens.
    }
    #print(role)
    #input()
    #print(ConfigBox.dialog_examples[chat_id])
    #input()
    if chat_id not in ConfigBox.dialog_chat_palm.keys() :
        ConfigBox.dialog_chat_palm[chat_id] = chat_model.start_chat(
            context=role,
            examples=ConfigBox.dialog_examples[chat_id]
        )

    response = ConfigBox.dialog_chat_palm[chat_id].send_message(
        text_message, **parameters
    )
    print(f"palm_2_chat_vertex: {response.text}")

    return response

def code_chat_vertex(chat_id:str, text_message: str, role: str, temperature: float = 0.5) -> object:
    """Example of using Codey for Code Chat Model to write a function."""

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 1024,  # Token limit determines the maximum amount of text output.
    }

    code_chat_model = CodeChatModel.from_pretrained("codechat-bison@001")
    
    if chat_id not in ConfigBox.dialog_code_chat.keys() :
        ConfigBox.dialog_code_chat[chat_id] = code_chat_model.start_chat()

    response = ConfigBox.dialog_code_chat[chat_id].send_message(text_message, **parameters)
    print(f"code_chat_vertex: {response.text}\n")

    return response

def code_completion_vertex(chat_id:str, text_message: str, role: str, temperature: float = 0.2) -> object:

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 64,  # Token limit determines the maximum amount of text output.
    }

    if chat_id not in ConfigBox.dialog_code_completion.keys() :
        ConfigBox.dialog_code_completion[chat_id] = CodeGenerationModel.from_pretrained("code-gecko@001")

    response = ConfigBox.dialog_code_completion[chat_id].predict(prefix=text_message, **parameters)
    print(f"code_completion_vertex: {response.text}")

    return response

def code_generation_vertex(chat_id:str, text_message: str, role: str, temperature: float = 0.5) -> object:

    # TODO developer - override these parameters as needed:
    parameters = {
        "temperature": temperature,  # Temperature controls the degree of randomness in token selection.
        "max_output_tokens": 256,  # Token limit determines the maximum amount of text output.
    }

    if chat_id not in ConfigBox.dialog_code_generation.keys() :
        ConfigBox.dialog_code_generation[chat_id] = CodeGenerationModel.from_pretrained("code-bison@001")

    response = ConfigBox.dialog_code_generation[chat_id].predict(prefix=text_message, **parameters)

    print(f"code_generation_vertex: {response.text}")

    return response
class CreateExample(StatesGroup):
    examplein = State()
    exampleout = State()

@router.message(StateFilter(None), Command("examplein"))
async def cmd_examplein(
            message: Message,
            command: CommandObject,
            state: FSMContext
    ):

    # Если не переданы никакие аргументы, то
    # command.args будет None
    count = 0
    chat_id = str(message.chat.id)
    if chat_id not in ConfigBox.dialog_examples.keys() : ConfigBox.create_dialog(chat_id)
    if command.args is None:
        for _ in ConfigBox.dialog_examples[str(message.chat.id)] :
            count += 1
            await message.answer(f"Example {count}: {_}")
    else :
        await state.update_data(examplein=command.args)
        await state.set_state(CreateExample.examplein)
        await message.answer(f"examplein added!")

@router.message(CreateExample.examplein, Command("exampleout"))
async def cmd_exampleout(
            message: Message,
            command: CommandObject,
            state: FSMContext
    ):

    user_data = await state.get_data()
    chat_id = str(message.chat.id)

    # Если не переданы никакие аргументы, то
    # command.args будет None
    count = 0
    if chat_id not in ConfigBox.dialog_examples.keys() : ConfigBox.create_dialog(chat_id)
    if command.args is None:
        for _ in ConfigBox.dialog_examples[chat_id] :
            count += 1
            await message.answer(f"Example {count}: {_}")
    else :
        ConfigBox.add_example(chat_id=chat_id, example_in=user_data['examplein'], example_out=command.args)
        await message.answer(f"exampleout added! Mission complete!")
        #await state.set_state(CreateExample.exampleout)
        await state.clear()

@router.message(CreateExample.examplein)
async def cmd_exampleout_incorrectly(message: Message):
    await message.answer(
        text="You set examplein. I wait for exampleout.\n\n"
             "Пожалуйста, выберите!"
    )

# Хэндлер на команду /role
@router.message(Command("role"))
async def set_assistant_instructions(
            message: Message,
            command: CommandObject
    ):

    chat_id = str(message.chat.id)

    # Если не переданы никакие аргументы, то
    # command.args будет None
    if command.args is None:
        await message.answer(ConfigBox.dialog_instructions[chat_id])
        return
    # Пробуем разделить аргументы на две части по первому встречному пробелу
    try:
        #open_ai_role_dict[str(message.chat.id)] = command.args
        ConfigBox.set_dialog_instructions(chat_id, command.args)
    # Если получилось меньше двух частей, вылетит ValueError
    except ValueError:
        await message.answer(f"Now the Role set to: {ConfigBox.dialog_instructions[chat_id]}")
        return
    await message.answer(
        "Роль установлена!\n"
        f"Текст: {command.args}"
    )

@router.message(F.text)
async def message_with_text(message: Message):
    
    #query = message.text.replace('"', '^')
    query = message.text.replace('"', '^')

    words = query.split()

    # Make the desired change to the first word
    flag = False
    for _ in words :
        if _[0] == '@' : 
            flag = True
    
    chat_id = str(message.chat.id)
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    user_username = message.from_user.username
    user_name = str(user_id)+'.'+user_username+'.'+user_first_name+'.'+user_last_name
    now = datetime.now()
    formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
    response = None

    if flag : await message.answer("Я молчу...")
    else :
        if chat_id not in ConfigBox.dialog_instructions.keys() : ConfigBox.create_dialog(chat_id)
        #response = palm_2_chat_vertex(chat_id, message.text, role=ConfigBox.dialog_instructions[chat_id])

        match ConfigBox.chat_ai_model[chat_id]:
            case ChatAI_ModelType.PALM_2_CHAT:
                response = palm_2_chat_vertex(chat_id, message.text, role=ConfigBox.dialog_instructions[chat_id])
            case ChatAI_ModelType.CODE_CHAT:
                response = code_chat_vertex(chat_id, message.text, role=ConfigBox.dialog_instructions[chat_id])
            case ChatAI_ModelType.CODE_COMPLETION:
                response = code_completion_vertex(chat_id, message.text, role=ConfigBox.dialog_instructions[chat_id])  
            case ChatAI_ModelType.CODE_GENERATION:
                response = code_generation_vertex(chat_id, message.text, role=ConfigBox.dialog_instructions[chat_id])
            case _:
                response = palm_2_chat_vertex(chat_id, message.text, role=ConfigBox.dialog_instructions[chat_id])

        ConfigBox.update_dialog(chat_id, 'vertex', response.text)
        role_2_db = ConfigBox.chat_ai_model[chat_id].value + ConfigBox.dialog_instructions[chat_id]
        params = (chat_id, user_name, formatted_date, role_2_db, message.text, response.text, 0, 0, 0)
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