import os
from django.http import HttpResponse
from django.shortcuts import render
from twilio.rest import Client
from .chatbot_keywords import chatbot_keywords
account_sid = 'ACb44b91cc79bde5f60515ac29b4a6da71'
auth_token = '67450e31eef2339776b92603b996af5d'
client = Client(account_sid, auth_token)
from django.views.decorators.csrf import csrf_exempt
import openai
# Create your views here.
def mybot(request):
    openai.organization = "org-zmd9VBXgOdzNW5zgZ8ci8RzG"
    openai.api_key = "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"
    # messages = 
    
# import openai

    chat  = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Who won the world series in 2020?"},
            {"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
            {"role": "user", "content": "Where was it played?"}
        ]
    )
    replay = chat.choices[0].message.content
    print(replay)
    return render(request,'index.html')

@csrf_exempt


def whatsupbot(request):
    print(request)
    message = request.POST['Body']
    name = request.POST['ProfileName']
    From = request.POST['From']
    input_data = str(message).split(' ')
    
    keywords = chatbot_keywords
    
    def send(data):
        message = client.messages.create(
                                from_='whatsapp:+14155238886',
                                body=data,
                                to=From
                            )
        
    for k in keywords:
        if k in input_data:
            data = keywords[k]
            send(data)
            

    return HttpResponse("bot is running")