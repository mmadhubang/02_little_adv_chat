import gradio as gr
import ollama

MODEL = "llama3.2"

def _flatten_content(content) -> str:
    """Collapse Gradio 6's structured content (str or list of parts) into plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for part in content:
            if isinstance(part, str):
                parts.append(part)
            elif isinstance(part, dict):
                parts.append(str(part.get("text") or part.get("value") or ""))
            else:
                parts.append(str(getattr(part, "text", "") or ""))
        return "".join(parts)
    return "" if content is None else str(content)


def chat_fn(message, history):
    # Build Ollama-compatible messages by flattening Gradio's content parts.
    messages = [
        {
            "role": m["role"],
            "content": _flatten_content(m["content"]),
        }
        for m in history
    ]
    messages.append({"role": "user", "content": message})

    stream = ollama.chat(model=MODEL, messages=messages, stream=True)
    response_text = ""
    for chunk in stream:
        response_text += chunk["message"]["content"]
        yield response_text


demo = gr.ChatInterface(
    fn=chat_fn,
    title="Ollama Chat (llama3.2)",
    description="Local chatbot powered by Ollama + Gradio.",
)

if __name__ == "__main__":
    demo.launch()
