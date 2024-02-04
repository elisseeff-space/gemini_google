import json, os
import logging
import sqlite3 as sq
from enum import Enum
from vertexai.language_models import InputOutputTextPair

class ChatAI_ModelType(Enum):
    PALM_2_CHAT = 'Palm_2_Chat' # The PaLM 2 for Chat (chat-bison)
    CODE_CHAT = 'Code_Chat' # Codey for Code Chat (codechat-bison)
    CODE_GENERATION = 'Code_Generation' # Codey for Code Completion (code-gecko)
    CODE_COMPLETION = 'Code_Completion' # Codey for Code Generation (code-bison)"
    GEMINI_PRO = 'Gemini_Pro' # A model size that balances capability and efficiency. https://ai.google.dev/models/gemini?hl=en
    
class gemini_Config():
    logger = logging.getLogger(__name__)
    # настройка обработчика и форматировщика для logger
    if os.name == 'posix': 
        file_name = "/home/pavel/github/gemini_google/log/gemini_google.log"
    elif os.name == 'nt':
        file_name = r'C:\Users\Eliseev\GitHub\gemini_google\log\gemini_google.log'
    else: raise ValueError("Unsupported operating system")

    handler = logging.FileHandler(file_name, mode='w')
    #formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s", datefmt='%Y/%m/%d %I:%M:%S')
    formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s", datefmt='%Y/%m/%d %H:%M:%S')

    PROJECT_ID = "ai-elis-project"
    LOCATION = "us-central1" #e.g. us-central1
    chat_ai_model = {} # Default: ChatAI_ModelType.PALM_2_CHAT
    dialog_messages = {}
    dialog_instructions = {} # role
    dialog_examples = {}
    dialog_chat_gemini_pro = {}
    dialog_chat_palm = {}
    dialog_code_chat = {}
    dialog_code_completion = {}
    dialog_code_generation = {}

    @classmethod
    def __init__(self):
        
        # Set up logger
        # self.logging #.info('Verify successfully init!')
        
        self.logger.setLevel(logging.INFO)
        
        # добавление форматировщика к обработчику
        self.handler.setFormatter(self.formatter)
        # добавление обработчика к логгеру
        self.logger.addHandler(self.handler)

        if os.name == 'posix': filename = "/home/pavel/github/gemini_google/db/gemini_google.db"
        elif os.name == 'nt': filename = str(r'C:\Users\Eliseev\GitHub\gemini_google\db\gemini_google.db')
        else: raise ValueError("Unsupported operating system")
        self.dbase = sq.connect(filename)
        self.cur = self.dbase.cursor()
        

        if os.name == 'posix': in_file = "/home/pavel/cfg/google_config.json"
        elif os.name == 'nt': in_file = str(r'C:\Users\Eliseev\GitHub\cfg\google_config.json')
        else: raise ValueError("Unsupported operating system")
        file = open(in_file, 'r')
        self.config = json.load(file)
    
    @classmethod
    def set_logger_name(self, logger_name: str)->bool:
        self.logger.name = logger_name
    
    @classmethod
    def add_example(self, chat_id: str, example_in: str, example_out: str)->bool:
        self.dialog_examples[chat_id].append(
            InputOutputTextPair(
                    input_text=example_in,
                    output_text=example_out,
            )
        )

    @classmethod
    def create_dialog(self, chat_id: str)->bool:
        self.dialog_messages[chat_id] = [
            {
                "role": "system",
                "text": "Ты профессионал программист на python. В остальное время любишь пофилософствовать."
            }
            ]
        self.dialog_instructions[chat_id] = "Ты профессионал программист на python. В остальное время любишь пофилософствовать."
        self.dialog_examples[chat_id] = [InputOutputTextPair(
                    input_text="Simple question?",
                    output_text="Interesting answer!",
            ),]
        self.chat_ai_model[chat_id] = ChatAI_ModelType.PALM_2_CHAT
    
    @classmethod
    def set_dialog_role(self, chat_id: str, role: str)->bool:
        self.dialog_messages[chat_id] = [
            {
                "role": "system",
                "text": role
            }
            ]
        self.dialog_role[chat_id] = role
        
    @classmethod
    def update_dialog(self, chat_id: str, role: str, message: str)->bool:
        self.dialog_messages[chat_id].append({
                "role": role,
                "text": message
            })
        
        if(len(self.dialog_messages[chat_id])) > 8:
            self.dialog_messages[chat_id].pop(2)
            self.dialog_messages[chat_id].pop(2)
            ConfigBox.logger.info(f"self.dialog_messages[chat_id].pop(2). chat_id = {chat_id}")

        #print('self.dialog_messages[chat_id]: ')
        #print(self.dialog_messages[chat_id])
        #input()
    
    @classmethod
    def set_dialog_instructions(self, chat_id: str, role: str)->bool:
        self.dialog_instructions[chat_id] = role

ConfigBox = gemini_Config()

if __name__ == '__main__':
    print("Hello!")
    
    ConfigBox.logger.warning('New gemini_Config successfully init!')