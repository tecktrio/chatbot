import json
import os
import random
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from twilio.rest import Client
from rest_framework.views import APIView
from mybot.settings import TWILIO_ACCOUNT_SID, TWILIO_TOKEN
from .chatbot_keywords import chatbot_keywords
from .chatbot_keywords import do_not_understand
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_TOKEN
client = Client(account_sid, auth_token)
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def mybot(request):
    return render(request,'index.html')

@csrf_exempt
def whatsupbot(request):
    print(request)
    message = request.POST.get('Body')
    name = request.POST.get('ProfileName')
    From = request.POST.get('From')
    input_data = str(message).lower().split(' ')
    
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
        else:
            data = random.choice(do_not_understand)
            

    return HttpResponse("bot is running")

class webbot(APIView):
    @csrf_exempt
    def post(self,request):
        

        data = json.load(request)
        key = data.get('key')
        value = data.get('value')
        print(key,value)
        if key == 'read':
            data = f'{value}'

        return JsonResponse({'status':'success','voice':data})