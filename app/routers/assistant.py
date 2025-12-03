from fastapi import APIRouter, HTTPException
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")
client = OpenAI(api_key=OPENAI_API_KEY)

@router.post("/ask")
async def ask_ai(query: str):

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are KrishiMitra, an AI assistant for farmers. Answer simply and in Hindi if farmer asks in Hindi."},
                {"role": "user", "content": query}
            ],
            temperature=0.6,
            max_tokens=200
        )

        answer = response.choices[0].message.content
        return {"query": query, "answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
