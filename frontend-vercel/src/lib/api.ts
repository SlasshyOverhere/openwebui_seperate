```typescript
import { BACKEND_API_URL } from './constants';

export async function sendMessageToBackend(message: string, model: string = "openai/gpt-3.5-turbo") {
    const res = await fetch(`${BACKEND_API_URL}/openai/chat/completions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            model,
            messages: [{ role: "user", content: message }]
        })
    });
    if (!res.ok) throw new Error("Backend error");
    const data = await res.json();
    return data.choices?.[0]?.message?.content || data.message || "";
}
```