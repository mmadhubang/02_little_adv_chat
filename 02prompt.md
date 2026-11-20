Build a single-file Gradio chat UI (app_custom.py, ~40 lines) on Windows 11
that streams from local Ollama. No RAG, no file upload, no extras.

Environment: Gradio 6.x, ollama (pydantic client), model llama3.2 on
localhost:11434.

Constraints — do not deviate:

1. Do NOT pass `type=` to gr.ChatInterface(). Gradio 6 removed it; history
   is ALWAYS the messages format.

2. history = [{"role": "user"|"assistant", "content": ...}, ...] — dicts,
   NOT (user, assistant) tuples.

3. content may be a str OR a list of parts like [{"type":"text","text":"hi"}].
   Ollama rejects the list with a Pydantic string_type error. Collapse to
   str with a _flatten_content() helper before calling ollama.chat().

4. Project each history message to exactly {"role", "content"} — strip any
   other Gradio keys (files, metadata, id) or Ollama validation fails.

5. chat_fn(message, history) must be a GENERATOR yielding growing partial
   strings (accumulate chunk["message"]["content"], yield running total)
   so Gradio streams to the browser.

6. Call ollama.chat(model=MODEL, messages=messages, stream=True).

7. Do not assume API shapes from memory. Before writing code, verify with:
     pip show gradio
     python -c "import inspect, gradio as gr; print(inspect.signature(gr.ChatInterface.__init__))"
   If unsure, ask me to paste the output rather than guess.

After the code, list any environment assumptions so I can verify them.
