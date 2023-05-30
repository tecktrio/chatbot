import openai
from mybot.settings import OPEN_AI_KEY
openai.organization = "org-1VZK0fl8oXM4HK6zyoHJNi6F"
openai.api_key = OPEN_AI_KEY
messages = []
def getIntelligent(question):
    messages.append({"role": "system", "content":"you are my best friend"})
    while True:
        message = question
        if message:
            messages.append(
            {"role": "user", "content": message},
            )
        chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages,max_tokens=20,
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        return reply