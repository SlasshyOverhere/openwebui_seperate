from fastapi import APIRouter, Request
router = APIRouter()

@router.post("/openai/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    # ...existing code to process message...
    # Example response:
    return {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": ai_response_text
                }
            }
        ]
    }