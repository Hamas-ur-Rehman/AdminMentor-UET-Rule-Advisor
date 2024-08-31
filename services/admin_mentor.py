import datetime
from utils.custom_logger import log

from prompt import PROMPT

from .mongodb_service import MongoDBService
from .openai_service import OpenAIService
from .chroma_service import ChromaService

class AdminMentor:
    def __init__(self,userid:str):
        self.mongo = MongoDBService()
        self.openai = OpenAIService()
        self.chroma = ChromaService()
        self.userid = userid

    def ask(self,question:str):
        log.info("Adding Chats into MongoDB -- User")
        self.mongo.insert_chat(
            userid=self.userid,
            role="user",
            msg=question,
            created_at=datetime.datetime.now()
        )
        
        
        messages = self.__build_messages(question)

        response = self.openai.askai(messages)
        log.info("Adding Chats into MongoDB -- AI")
        self.mongo.insert_chat(
            userid=self.userid,
            role="assistant",
            msg=response,
            message=messages,
            created_at=datetime.datetime.now()
        )
        return response

    
    def __build_messages(self,question:str):
        log.info("Retriving Data From Database")
        docs = self.chroma.retriver(question)
        DOC_PROMPT = 'This is from where you can possibly get information about the user question'
        for doc in docs:
            DOC_PROMPT += "\n" + doc
        messages = [
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "system",
                "content": DOC_PROMPT
            },
        ]

        try:
            log.info("Fetching Chats from MongoDB")
            chats = self.mongo.fetch_chats(self.userid)
            for chat in chats:
                    messages.append(
                    {
                        "role":chat['role'],
                        "content":chat["msg"]
                    }
                    )
        except Exception as e:
            log.error(f"Error in fetching chats: {e}", exc_info=True)
        

        messages.append({"role":"user","content":question})
        return messages