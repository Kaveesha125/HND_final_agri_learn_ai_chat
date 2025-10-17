from fastapi import FastAPI
from pydantic import BaseModel
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from gemini_chat import get_gemini_response

# this loads the .env file variables (your keys)
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    role: str
    conversation_id: str | None = None


@app.post("/chat")
def chat_with_agri_learn(request: ChatRequest):
    try:
        # if no conversation id new conversation
        if not request.conversation_id:
            convo = supabase.table("conversations").insert({"role": request.role}).execute()
            conversation_id = convo.data[0]["id"]
        # if have id continue existing conversation
        else:
            conversation_id = request.conversation_id

        # Save user message
        supabase.table("messages").insert({
            "conversation_id": conversation_id,
            "sender": "user",
            "content": request.message
        }).execute()

        # Get AI reply
        reply = get_gemini_response(request.message, request.role)

        # Save AI reply
        supabase.table("messages").insert({
            "conversation_id": conversation_id,
            "sender": "assistant",
            "content": reply
        }).execute()

        return {"reply": reply, "conversation_id": conversation_id}
    except Exception as e:
        return {"error": str(e)}

#  Get all conversation summaries
@app.get("/conversations")
def list_conversations():
    data = supabase.table("conversations").select("*").order("created_at", desc=True).execute()
    return {"conversations": data.data}

#  Get all messages in one conversation
@app.get("/conversations/{conversation_id}")
def get_conversation_messages(conversation_id: str):
    data = supabase.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at").execute()
    return {"messages": data.data}

@app.get("/")
def read_root():
    return {"status": "site is up and running"}
