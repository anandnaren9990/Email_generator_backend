from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from resources.llm_prompt import prompt
from resources.llm_resources import model
from services.llm_service import chat_with_llm
from app_log import logger

app = FastAPI()

@app.post("/emailgenerator/")
def generate_email(email_context):
    logger.info("Email generator endpoint is called...")
    try:
        message = [
            {
                "role" : "system",
                "content" : prompt
            },
            {
                "role" : "user",
                "content" : email_context
            }
        ]
        return StreamingResponse(
            chat_with_llm(model=model, messages=message),
            media_type="text/plain"
        )
    except Exception as e:
        print(f"Exception occured: {e}")
