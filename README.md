## AdminMentor: UET Rule Advisor
**AdminMentor: UET Rule Advisor** is an AI-powered chatbot designed to assist administrators at the University of Engineering and Technology (UET) in navigating and understanding university policies and regulations. The chatbot provides quick, accurate responses to rule-related queries, streamlining administrative tasks and ensuring that UET's guidelines are followed consistently. With a user-friendly interface and seamless access to official documents, AdminMentor serves as a reliable virtual assistant for UET administrators, enhancing efficiency and clarity in rule management.

## Features
- **Rule Querying**: Users can ask questions about UET's rules and regulations, receiving instant responses from the chatbot.
- **Document Retrieval**: AdminMentor can provide links to official documents and resources related to specific rules and policies.
- **User-Friendly Interface**: AdminMentor is designed with a simple, intuitive interface that makes it easy for administrators to interact with the chatbot and access information quickly.

## Technologies Used
- Python
- Langchain
- FastAPI
- Gradio
- Uvicorn
- Chroma Vector Databse
- MongoDB
- OpenAI

## Requirements
- Make sure you have python installed on your computer. If not, you can download it from [Download Python version 3.10.8](https://www.python.org/ftp/python/3.10.8/python-3.10.8-amd64.exe).
- Download Mongo community server [Download by clicking me](https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-7.0.14-signed.msi) and install it.
- Download MongoDB Compass [Download by clicking me](https://downloads.mongodb.com/compass/mongodb-compass-1.43.6-win32-x64.exe) and install it.
- Download and install the latest version of [Download by clicking me](https://github.com/git-for-windows/git/releases/download/v2.46.0.windows.1/Git-2.46.0-64-bit.exe).

## Important step
create a file named `.env` in the root directory of the project and add the following lines to it.
    ```env
    OPENAI_API_KEY=paste-your-api-key-here
    MONGODB=mongodb://localhost:27017/
    ```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Hamas-ur-Rehman/AdminMentor-UET-Rule-Advisor
   ```

2. Install the required dependencies:
   ```bash
    pip install -r requirements.txt
    ```
3. Run the application:
    ```bash
    uvicorn main:app --reload
    ```
4. Open the browser and go to the following URL:
    ```bash
    http://127.0.0.1:8000/docs
    ```
    ![image](https://github.com/user-attachments/assets/5b86fd6f-b653-4b49-8ba9-bcb1d19d1f24)


5. You can now interact with the chatbot through the Swagger UI. This is you API endpoint. I have created a demo UI and an API if you want to make your own UI as well.
     ![image](https://github.com/user-attachments/assets/91318b76-901c-425d-9ccd-a64c9a97d9b1)

6. To run the API, run the following command: follow the image below (This is needed if you want to make your own UI)
   ![image](https://github.com/user-attachments/assets/3a201513-7659-4a7a-84e3-54b835394162)
   ![image](https://github.com/user-attachments/assets/e46db2ad-50b7-4c02-9653-994b077e0389)
   ![image](https://github.com/user-attachments/assets/7e93ac58-a6a1-4db6-86fc-0cdbdf7492f7)
   ![image](https://github.com/user-attachments/assets/483ebebd-73e5-42c7-a798-0ba859af5b16)

8. To run the UI, run the following command: follow the image below
   ![image](https://github.com/user-attachments/assets/acde4055-79c3-4e31-bd9a-a0cc0c56c723)
   ![image](https://github.com/user-attachments/assets/c9b0e582-2cbc-49aa-9f24-f96c214772d1)
   ![image](https://github.com/user-attachments/assets/15ddc205-4825-45b7-b649-53569f3586f6)
   ![image](https://github.com/user-attachments/assets/1e3680b5-70ae-4d96-8ae0-54e4692e2626)

## Final UI
![image](https://github.com/user-attachments/assets/3a7d4e96-64db-4d60-93bf-0ff5fa9aea85)




