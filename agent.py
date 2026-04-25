from ollama import chat
from tools import tools, handle_tool_call
from memory import init_db, save_message, load_recent, clear_history


def stream_response(messages):
    full_content = ""
    stream = chat(
        model='qwen2.5:7b',
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        full_content += content
    print("\n")
    return full_content


def main():
    init_db()
    messages = load_recent(limit=20)
    print(f"Jarvis v0.4 — type 'quit' to exit, '/clear' to wipe memory")
    print(f"Loaded {len(messages)} messages from history\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ('quit', 'exit'):
            print("Goodbye.")
            break

        if user_input == '/clear':
            clear_history()
            messages = []
            print("Memory wiped.\n")
            continue

        if not user_input:
            continue

        messages.append({'role': 'user', 'content': user_input})
        save_message('user', content=user_input)

        response = chat(
            model='qwen2.5:7b',
            messages=messages,
            tools=tools,
        )

        msg = response['message']
        tool_calls = msg.tool_calls if hasattr(msg, 'tool_calls') else msg.get('tool_calls')

        if tool_calls:
            tc_list = [
                {'function': {'name': tc.function.name if hasattr(tc, 'function') else tc['function']['name'],
                              'arguments': tc.function.arguments if hasattr(tc, 'function') else tc['function'].get('arguments', {})}}
                for tc in tool_calls
            ]
            messages.append(msg)
            save_message('assistant', content='', tool_calls=tc_list)

            for tool_call in tool_calls:
                fn_name = tool_call.function.name if hasattr(tool_call, 'function') else tool_call['function']['name']
                result = handle_tool_call(tool_call)
                messages.append({
                    'role': 'tool',
                    'content': result,
                    'tool_name': fn_name,
                })
                save_message('tool', content=result, tool_name=fn_name)

            print("Jarvis: ", end='', flush=True)
            followup_content = stream_response(messages)
            messages.append({'role': 'assistant', 'content': followup_content})
            save_message('assistant', content=followup_content)
        else:
            print("Jarvis: ", end='', flush=True)
            full_content = stream_response(messages)
            messages.append({'role': 'assistant', 'content': full_content})
            save_message('assistant', content=full_content)


if __name__ == '__main__':
    main()