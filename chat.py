from ollama import chat

def main():
    messages = []
    print("Jarvis v0.1 - type 'quit to exit\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() in ('quit', 'exit'):
            print("Goodbye.")
            break

        if not user_input:
            continue

        messages.append({'role':'user', 'content': user_input})

        print("Jarvis: ", end='', flush=True)

        response = ""

        stream = chat(
            model='llama3.2:latest',
            messages=messages,
            stream=True,
        )

        for chunk in stream:
            content=chunk['message']['content']
            print(content, end='', flush=True)
            response+=content

        print("\n")

        messages.append({'role': 'assistant', 'content': response})

if __name__ == '__main__':
    main()
        