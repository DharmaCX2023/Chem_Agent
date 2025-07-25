import openai

openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxx"

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "hello"}
    ],
    temperature=0,
    timeout=10
)

print(response["choices"][0]["message"]["content"])