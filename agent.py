from datetime import datetime
from ollama import chat


def get_current_time():
    return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")


tools = [
    {
        'type': 'function',
        'function': {
            'name': 'get_current_time',
            'description': 'Get the current date and time',
            'parameters': {
                'type': 'object',
                'properties': {},
                'required': [],
            },
        },
    },
]


def handle_tool_call(tool_call):
    fn_name = tool_call['function']['name']

    if fn_name == 'get_current_time':
        return get_current_time()

    return f"Unknown tool: {fn_name}"


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
    messages = []
    print("Jarvis v0.2 — type 'quit' to exit\n")

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
        print("DEBUG msg:", msg)
        messages.append(msg)

        if msg.get('tool_calls'):
            for tool_call in msg['tool_calls']:
                result = handle_tool_call(tool_call)
                messages.append({
                    'role': 'tool',
                    'content': result,
                })

            print("Jarvis: ", end='', flush=True)
            followup_content = stream_response(messages)
            messages.append({'role': 'assistant', 'content': followup_content})
        else:
            print("Jarvis:", msg['content'], "\n")


if __name__ == '__main__':
    main()