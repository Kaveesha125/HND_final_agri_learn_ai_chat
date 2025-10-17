# Agri‑Learn AI Chat
>[!NOTE]
> 🧩 This is a **sub-microservice** of the main website for the **HND Final Project**.

FastAPI service for an agriculture chat assistant using [Gemini](https://gemini.google.com/app) and [Supabase](https://supabase.com/)
##  Quick Start
1. **Create virtual environment & install dependencies**
   - Windows (PowerShell)
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     pip install -r requirements.txt
     ```
2. **Configure environment variables**
  
> [!IMPORTANT]
> **You must add these to the `.env` file.**

````
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
GEMINI_API_KEY="your-gemini-api-key"
````

3. **Run the server**
```bash
uvicorn main:app --reload
````
## API Endpoints

> [!NOTE]
> Base URL: `http://localhost:8000`
>
> * **GET `http://localhost:8000/`** - Confirms that the service is running.
>
> * **POST `http://localhost:8000/chat`** - Start a new conversation
>   ```json
>   {
>     "message": "How to improve soil health?",
>     "role": "student"
>   }
>   ```
>
> * **POST `http://localhost:8000/chat`** - Continue an existing conversation by including a `conversation_id`:
>
>   ```json
>   {
>     "message": "What are the best practices for crop rotation?",
>     "role": "student",
>     "conversation_id": "existing-conversation-id"
>   }
>   ```
>
> * **GET `http://localhost:8000/conversations`** — List all past conversations
>
> * **GET `http://localhost:8000/conversations/{conversation_id}`** — Retrieve all messages from a specific conversation
---

> [!TIP]
> Get your api key here - [Gemini](https://aistudio.google.com/app/api-keys) | [Supabase](https://supabase.com/).

> [!NOTE]
> Authentication **not yet implemented**.

---
