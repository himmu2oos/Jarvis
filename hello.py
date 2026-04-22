from ollama import chat

response = chat(
    model='llama3.2:latest',
    messages=[
        {
            'role':'user',
            'content':'Tell me about Arsenal F.C in under 50 words'
        }
    ],
    stream=True,
)

for chunk in response:
    print(chunk['message']['content'], end='', flush=True)

print()
