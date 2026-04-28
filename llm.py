from ollama import chat as ollama_chat
from config import MODEL


class LLMError(Exception):
    pass


def stream_with_tools(messages, tools):
    """
    Single streaming call with tool detection.
    Returns (content_str, tool_calls_or_None).
    Prints content live as it streams (suppressed if tool_calls detected).
    """
    full_content = ""
    final_tool_calls = None
    printed_prefix = False

    try:
        stream = ollama_chat(
            model=MODEL,
            messages=messages,
            tools=tools,
            stream=True,
        )

        for chunk in stream:
            msg = chunk.get('message') if isinstance(chunk, dict) else chunk.message
            content = msg.get('content', '') if isinstance(msg, dict) else (msg.content or '')
            tool_calls = msg.get('tool_calls') if isinstance(msg, dict) else getattr(msg, 'tool_calls', None)

            if tool_calls:
                final_tool_calls = tool_calls

            if content and not final_tool_calls:
                if not printed_prefix:
                    print("Jarvis: ", end='', flush=True)
                    printed_prefix = True
                print(content, end='', flush=True)
                full_content += content

        if printed_prefix:
            print("\n")

        return full_content, final_tool_calls

    except Exception as e:
        raise LLMError(f"stream failed: {e}")


def stream_followup(messages):
    """Stream final reply after tool results. No tools passed."""
    full_content = ""
    print("Jarvis: ", end='', flush=True)
    try:
        stream = ollama_chat(model=MODEL, messages=messages, stream=True)
        for chunk in stream:
            msg = chunk.get('message') if isinstance(chunk, dict) else chunk.message
            content = msg.get('content', '') if isinstance(msg, dict) else (msg.content or '')
            print(content, end='', flush=True)
            full_content += content
        print("\n")
        return full_content
    except Exception as e:
        print(f"\n[stream error: {e}]\n")
        return full_content