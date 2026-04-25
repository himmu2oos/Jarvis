from ollama import chat
from tools import tools, handle_tool_call


def stream_response(messages, use_tools=False):
    full_content = ""
    kwargs = {
        'model': 'qwen2.5:7b',
        'messages': messages,
        'stream': True,
    }
    if use_tools:
        kwargs['tools'] = tools

    stream = chat(**kwargs)
    for chunk in stream:
        content = chunk['message']['content']
        print(content, end='', flush=True)
        full_content += content
    print("\n")
    return full_content


def main():
    messages = []
    print("Jarvis v0.3 — type 'quit' to exit\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ('quit', 'exit'):
            print("Goodbye.")
            break

        if not user_input:
            continue

        messages.append({'role': 'user', 'content': user_input})

        response = chat(
            model='qwen2.5:7b',
            messages=messages,
            tools=tools,
        )

        msg = response['message']
        tool_calls = msg.tool_calls if hasattr(msg, 'tool_calls') else msg.get('tool_calls')

        if tool_calls:
            messages.append(msg)
            for tool_call in tool_calls:
                fn_name = tool_call.function.name if hasattr(tool_call, 'function') else tool_call['function']['name']
                result = handle_tool_call(tool_call)
                messages.append({
                    'role': 'tool',
                    'content': result,
                    'tool_name': fn_name,
                })

            print("Jarvis: ", end='', flush=True)
            followup_content = stream_response(messages)
            messages.append({'role': 'assistant', 'content': followup_content})
        else:
            print("Jarvis: ", end='', flush=True)
            full_content = stream_response(messages)
            messages.append({'role': 'assistant', 'content': full_content})


if __name__ == '__main__':
    main()