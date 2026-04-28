from config import SYSTEM_PROMPT, HISTORY_LIMIT, MAX_TOOL_CALLS_PER_TURN
from llm import stream_with_tools, stream_followup, LLMError
from memory import init_db, save_message, load_recent
from tools import tools, handle_tool_call
from commands import handle_command


def build_messages(history):
    """Prepend system prompt to history."""
    return [{'role': 'system', 'content': SYSTEM_PROMPT}] + history


def run_turn(history):
    """One full turn. Single streaming call. Tool path adds second stream call."""
    content, tool_calls = stream_with_tools(build_messages(history), tools)

    if not tool_calls:
        history.append({'role': 'assistant', 'content': content})
        save_message('assistant', content=content)
        return history

    # Tool path
    if len(tool_calls) > MAX_TOOL_CALLS_PER_TURN:
        print(f"[truncating: {len(tool_calls)} tool calls > limit {MAX_TOOL_CALLS_PER_TURN}]")
        tool_calls = tool_calls[:MAX_TOOL_CALLS_PER_TURN]

    tc_serialized = [
        {'function': {
            'name': tc.function.name if hasattr(tc, 'function') else tc['function']['name'],
            'arguments': tc.function.arguments if hasattr(tc, 'function') else tc['function'].get('arguments', {}),
        }} for tc in tool_calls
    ]

    history.append({
        'role': 'assistant',
        'content': content,
        'tool_calls': tc_serialized,
    })
    save_message('assistant', content=content, tool_calls=tc_serialized)

    for tool_call in tool_calls:
        fn_name = tool_call.function.name if hasattr(tool_call, 'function') else tool_call['function']['name']
        result = handle_tool_call(tool_call)
        history.append({'role': 'tool', 'content': result, 'tool_name': fn_name})
        save_message('tool', content=result, tool_name=fn_name)

    followup = stream_followup(build_messages(history))
    history.append({'role': 'assistant', 'content': followup})
    save_message('assistant', content=followup)
    return history


def main():
    init_db()
    history = load_recent(limit=HISTORY_LIMIT)
    print(f"Jarvis v0.6 — type /help for commands")
    print(f"Loaded {len(history)} messages from history\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye.")
            break

        if not user_input:
            continue

        if user_input.lower() in ('quit', 'exit'):
            print("Goodbye.")
            break

        if user_input.startswith('/'):
            handled, history = handle_command(user_input, history)
            if handled:
                continue

        history.append({'role': 'user', 'content': user_input})
        save_message('user', content=user_input)

        try:
            history = run_turn(history)
        except LLMError as e:
            print(f"[error: {e}. try again or /clear]\n")
        except Exception as e:
            print(f"[unexpected error: {e}]\n")


if __name__ == '__main__':
    main()