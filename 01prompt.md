Build a Gradio chat UI in Python on Windows 11 that talks to a local Ollama
model. Environment (verify with `pip show gradio ollama` before writing code):

  - Gradio 6.x  (NOT 5.x)
  - ollama Python library (pydantic-based client)
  - Model: llama3.2, served by `ollama serve` on http://localhost:11434

Hard constraints — do not deviate:

1. Do NOT pass `type=` to `gr.ChatInterface(...)`. Gradio 6 removed that
   parameter entirely. History is ALWAYS the messages format in 6.x.

2. `history` is a list of dicts: [{"role": "user"|"assistant",
   "content": <...>}, ...]. It is NOT a list of (user, assistant) tuples.

3. `content` inside each history dict may be EITHER a plain string OR a
   list of parts like [{"type": "text", "text": "hi"}]. Ollama's Pydantic
   Message model rejects the list form with:
     "Input should be a valid string [type=string_type, input_type=list]"
   So before calling ollama.chat(), collapse content to a plain string
   with a helper like:

     def _flatten_content(c):
         if isinstance(c, str): return c
         if isinstance(c, list):
             return "".join(
                 p if isinstance(p, str)
                 else str(p.get("text", "") if isinstance(p, dict)
                        else getattr(p, "text", ""))
                 for p in c)
         return "" if c is None else str(c)

4. Project every history message down to exactly {"role", "content"} before
   passing to ollama.chat(). Strip any extra Gradio keys (files, metadata,
   id) — they will fail Ollama's validation.

5. `chat_fn(message, history)` must be a GENERATOR that yields growing
   partial strings (accumulate chunk["message"]["content"] and yield the
   running total) so Gradio streams tokens to the browser.

6. Call `ollama.chat(model=MODEL, messages=messages, stream=True)`.

7. If anything about the environment is uncertain (Gradio version, whether
   ChatInterface accepts a kwarg, history shape), INSPECT FIRST — run
   `pip show gradio`, `python -c "import gradio; print(gradio.__version__)"`,
   or `inspect.signature(gr.ChatInterface.__init__)` — before writing code.
   Do not assume behavior from older Gradio versions.

Deliverables:
  - Single runnable file (app_custom.py), ~40 lines.
  - Use a module-level MODEL constant.
  - Do not add features I didn't ask for (no RAG, no file upload, no
    system-prompt UI).
  - After the code, list any assumptions you made about the environment
    so I can verify them.

If you're unsure whether a kwarg exists in the installed Gradio, ask me to
paste the output of `python -c "import inspect, gradio as gr;
print(inspect.signature(gr.ChatInterface.__init__))"` rather than guessing.
