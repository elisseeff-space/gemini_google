import json, os
import logging
import sqlite3 as sq
from enum import Enum
import vertexai

class ChatModeType(Enum):
    CODE_CHAT = 'Code_Chat'
    CODE_GENERATION = 'Code_Generation'
    CODE_COMPLETION = 'Code_Completion'
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
    chat_mode = {}#ChatModeType.CODE_CHAT
    dialog_messages = {}
    dialog_role = {}

    """
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    from vertexai.preview.generative_models import (
        GenerationConfig,
        GenerativeModel,
    )
    
    from vertexai.preview.generative_models import (
        Content,
        FunctionDeclaration,
        GenerativeModel,
        Part,
        Tool,
    )
    """

    #model = GenerativeModel("gemini-pro")
    
    dialog_messages = {}

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
        

        if os.name == 'posix': in_file = "/home/pavel/cfg/config.json"
        elif os.name == 'nt': in_file = str(r'C:\Users\Eliseev\GitHub\cfg\config.json')
        else: raise ValueError("Unsupported operating system")
        file = open(in_file, 'r')
        self.config = json.load(file)

        # create OpenAI connection

        #self.client = OpenAI(api_key = self.config['openai'])

    @classmethod
    
    @classmethod
    def set_logger_name(self, logger_name: str)->bool:
        self.logger.name = logger_name
    
    @classmethod
    def create_dialog(self, chat_id: str)->bool:
        self.dialog_messages[chat_id] = [
            {
                "role": "system",
                "text": "Ты профессионал программист на python. В остальное время любишь пофилософствовать."
            }
            ]
        self.dialog_role[chat_id] = "Ты профессионал программист на python. В остальное время любишь пофилософствовать."
    
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

ConfigBox = gemini_Config()

if __name__ == '__main__':
    print("Hello!")
    
    ConfigBox.logger.warning('New gemini_Config successfully init!')