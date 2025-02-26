import logging
from fastapi import FastAPI
from pydantic import BaseModel
import openai

#Setup Logging (to debug issues)
logging.basicConfig(level=logging.DEBUG)

#Replace this with your actual OpenAI API key
openai.api_key = "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"  # Replace with your real key

#Create FastAPI App
app = FastAPI()

#Request Body Model
class ChatRequest(BaseModel):
    message: str

#Chatbot API Endpoint
@app.post("/chat")
async def chatbot(request: ChatRequest):
    try:
        logging.debug(f"Received message: {request.message}")

        #Call OpenAI GPT API (New Syntax for openai>=1.0.0)
        client = openai.OpenAI(api_key="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")  # ✅ Create an OpenAI client
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Eyedra, a mental health AI assistant."},
                {"role": "user", "content": request.message}
            ],
            max_tokens=150
        )

        chatbot_response = response.choices[0].message.content.strip()
        logging.debug(f"Chatbot response: {chatbot_response}")

        return {"response": chatbot_response}

    except openai.OpenAIError as e:  #Fix AttributeError
        logging.error(f"OpenAI API Error: {e}")
        return {"response": f"OpenAI API error: {str(e)}"}

    except Exception as e:
        logging.error(f"General Error: {e}")
        return {"response": f"Error: {str(e)}"}
