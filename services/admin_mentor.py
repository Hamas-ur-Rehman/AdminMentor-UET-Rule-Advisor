import datetime
import gradio as gr
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

    def interface(self,share:bool=False):
        with gr.Blocks(title="AdminMentor Demo Interface") as demo:
                gr.HTML("""
                <img src="https://github.com/user-attachments/assets/077a48d9-843e-486f-ad63-aebd79164be9" style="display: block; margin: 0 auto; max-width: 100%;">
                <h1 style="text-align: center;">AdminMentor Demo Interface</h1>
                <p><strong>AdminMentor: UET Rule Advisor</strong> is an AI-powered chatbot designed to assist administrators at the University of Engineering and Technology (UET) in navigating and understanding university policies and regulations. The chatbot provides quick, accurate responses to rule-related queries, streamlining administrative tasks and ensuring that UET's guidelines are followed consistently. With a user-friendly interface and seamless access to official documents, AdminMentor serves as a reliable virtual assistant for UET administrators, enhancing efficiency and clarity in rule management.</p>
                """
                )
                
                with gr.Row():
                    gr.HTML("""
                <p><strong>Project Supervisor:</strong></p>
                <ul>
                    <li><strong>Dr. Zakira Enayat</strong></li>
                </ul>
                <br>
                <br>
                <p><strong>Project Members:</strong></p>
                <ul>
                    <li><strong>Murtaza</strong> 20PWBCS0823 </li>
                    <li><strong>Zakarya</strong> 20PWBCS0819 </li>
                    <li><strong>Abdur Rahman</strong> 20PWBCS0794 </li>
                    <li><strong>Sahib Khan</strong> 20PWBCS0827 </li>
                </ul>
                """)
                    with gr.Column(scale=6):
                        chatbot = gr.Chatbot(
                            avatar_images=(
                                "avatar_images\\user_avatar.png",
                                "avatar_images\\uet_avatar.png"
                            )
                        )
                        with gr.Row():    
                            msg = gr.Textbox(scale=9,container=False)
                            btn = gr.Button(value='submit', variant='primary')
                            clear = gr.ClearButton([msg, chatbot])
                    

                def respond(message, history):
                    if message == '':
                        resp_message = "Please Enter a valid question"
                        history = history + [[message,'']]
                    else:
                        history = history + [[message,'']]
                        resp_message = self.ask(message)
                    
                    for i in resp_message:
                        history[-1][1] += i
                        yield "",history

                msg.submit(respond, [msg, chatbot], [msg, chatbot])
                btn.click(respond, [msg, chatbot], [msg, chatbot])
               

        demo.queue()
        _,b,c = demo.launch(
        prevent_thread_lock = True,
        share = share
        
        )
        return b,c

    
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