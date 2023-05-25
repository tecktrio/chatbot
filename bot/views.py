import os
from django.http import HttpResponse
from django.shortcuts import render
from twilio.rest import Client

from mybot.settings import TWILIO_ACCOUNT_SID, TWILIO_TOKEN
from .chatbot_keywords import chatbot_keywords
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_TOKEN
client = Client(account_sid, auth_token)
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def mybot(request):
   
    
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