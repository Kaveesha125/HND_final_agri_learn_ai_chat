# routers/chat.py
from fastapi import APIRouter
from models.chat import ChatRequest
from services.gemini_chat import get_gemini_response
from config import supabase

router = APIRouter()

@router.post("/chat")
def chat_with_agri_learn(request: ChatRequest):
    try:
        if not request.conversation_id:
            convo = supabase.table("conversations").insert({"role": request.role}).execute()
            conversation_id = convo.data[0]["id"]
        else:
            conversation_id = request.conversation_id

        supabase.table("messages").insert({
            "conversation_id": conversation_id,
            "sender": "user",
            "content": request.message
        }).execute()

        reply = get_gemini_response(request.message, request.role)

        supabase.table("messages").insert({
            "conversation_id": conversation_id,
            "sender": "assistant",
            "content": reply
        }).execute()

        return {"reply": reply, "conversation_id": conversation_id}
    except Exception as e:
        return {"error": str(e)}

@router.get("/conversations")
def list_conversations():
    data = supabase.table("conversations").select("*").order("created_at", desc=True).execute()
    return {"conversations": data.data}

@router.get("/conversations/{conversation_id}")
def get_conversation_messages(conversation_id: str):
    data = supabase.table("messages").select("*").eq("conversation_id", conversation_id).order("created_at").execute()
    return {"messages": data.data}