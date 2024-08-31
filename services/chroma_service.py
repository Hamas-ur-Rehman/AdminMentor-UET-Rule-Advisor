import os
import time
import shutil
from tqdm import tqdm
from dotenv import load_dotenv
from utils.custom_logger import log
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
import threading
load_dotenv()


class ChromaService:
    def __init__(self):
        self.db_name = "./chromadb"
        self.text_splitter = RecursiveCharacterTextSplitter(
                        # Set a really small chunk size, just to show.
                        chunk_size=5000,
                        chunk_overlap=1000,
                        length_function=len,
                        is_separator_regex=False,
                    )

    def loader(self):
        try:
            start_time = time.time()
            # Initialize the embeddings function from OpenAI
            embeddings = OpenAIEmbeddings()

            # Initialize the Chroma vector store
            log.info("Initializing Chroma vector store")
            if os.path.exists(self.db_name):
                log.info("Removing existing Chroma vector store")
                shutil.rmtree(self.db_name)

            vectorstore = Chroma(
                persist_directory=self.db_name,
                embedding_function=embeddings,
                collection_name="uet"
            )

            root_path = './extracted'
            items = os.listdir(root_path)
            for i in tqdm(items):
                with open(f"{root_path}/{i}",'r', encoding='utf-8') as f:
                    texts = self.text_splitter.create_documents([f.read()])
                    if isinstance(texts, str):
                        texts = [texts]
                    Chroma.add_documents(vectorstore, texts)
            log.warning(f"Time taken to load data: {round(time.time() - start_time, 2)} seconds")
        except Exception as e:
            log.error(f"Error in loader: {e}", exc_info=True)


    def retriver(self, question, k=4):
        try:
            start_time = time.time()
            # Initialize the embeddings function from OpenAI
            embeddings = OpenAIEmbeddings()
            vectorstore = Chroma(
                persist_directory=self.db_name,
                embedding_function=embeddings,
                collection_name="uet"
                )
            log.info("Retrieving documents from Chroma vector store")
            DOCS = []
            for i in vectorstore.similarity_search(question, k=k):
                DOCS.append(i.page_content)
            if len(DOCS) == 0:
                DOCS.append("Sorry, I couldn't find any relevant documents")
            log.warning(f"Time taken to retrieve documents: {round(time.time() - start_time,2)} seconds")
            return DOCS
        except Exception as e:
            log.error(f"Error in retriver: {e}", exc_info=True)
            return ["Sorry, I couldn't find any relevant documents"]