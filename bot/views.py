# importing the neccessary modules
import datetime
import io
import json
import mimetypes
import os
import random
import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from twilio.rest import Client
from rest_framework.views import APIView

from .serializers import User_Serializer
from .models import Admins, BotCollection, Users
from mybot.settings import TWILIO_ACCOUNT_SID, TWILIO_TOKEN
from .chatbot_keywords import chatbot_keywords
from .chatbot_keywords import do_not_understand
from django.views.decorators.csrf import csrf_exempt
from .intelligence import getIntelligent
# Create your views here.

# variables
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_TOKEN
client = Client(account_sid, auth_token)

# 
def Bots(request):
    return render(request,'index.html')

@csrf_exempt
def bot_registration(request):
    if request.method == 'POST':
        admin =  get_admin(request)
        bot_contact = request.POST.get('bot_contact')
        bot_name = request.POST.get('bot_name')
        bot_task = request.POST.get('bot_task')
        if bot_contact != '':
            new_bot =BotCollection.objects.create(admin_email=admin.email,Bot_contact = bot_contact,Bot_name = bot_name, Bot_Task = bot_task)
            new_bot.save()
            return render(request,'bot_registration.html',{'success':'Bot registered successfully. you can now go to dashboard.'})
        else:
            return render(request,'bot_registration.html',{'error':'provide a valid bot number'})
    return render(request, 'bot_registration.html')
    
def check_user_login_status(request):
    if 'widecity_chatbot_email' in request.COOKIES:
        try:
            email = request.COOKIES['widecity_chatbot_email']
            token = request.COOKIES['widecity_chatbot_token']
            if Admins.objects.filter(email=email):
                if Admins.objects.get(email=email).authorization_token == token:
                    return True
        except Exception as e:
            print('got an exception ',e)
            return False
    return False

def get_admin(request):
        email = request.COOKIES['widecity_chatbot_email']
        return Admins.objects.get(email=email)
        

@csrf_exempt
def Login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        response = ''
        authorization_token = random.randint(1000000000,9999999999)
        print(email)
        if Admins.objects.filter(email=email).exists():
            user = Admins.objects.get(email=email)
            if user.password == password:
                response = redirect(Dashboard)
                response.set_cookie('widecity_chatbot_token',authorization_token)
                response.set_cookie('widecity_chatbot_email',email)
                user.authorization_token = authorization_token
                user.save()
                return response
            response = render(request,'login.html',{'error':'invalid password'})
            return response
        response = render(request,'login.html',{'error':'invalid mail id'})
        return response
    if check_user_login_status(request):
        return redirect(Dashboard)
    return render(request, 'login.html')

@csrf_exempt
def SignUp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        contact = request.POST.get('contact')
        new_admin = Admins.objects.create(username=username, password=password, contact=contact, email=email)
        response = ''
        authorization_token = random.randint(1000000000,9999999999)
        new_admin.authorization_token = authorization_token
        new_admin.save()
        response = redirect(Dashboard)
        response.set_cookie('widecity_chatbot_token',authorization_token)
        response.set_cookie('widecity_chatbot_email',email)
        return response
    return render(request, 'signup.html')

def Logout(request):
    response = redirect(Login)
    response.delete_cookie('widecity_chatbot_token')
    response.delete_cookie('widecity_chatbot_email')
    return response

def Download_exel(request):
    users = Users.objects.all()
    serialized_data = User_Serializer(users,many=True)
    pd.DataFrame(serialized_data.data).to_excel('output.xlsx')
    path = 'output.xlsx'
    response = HttpResponse('downloading...')
    with open(path, 'rb') as f:
        response = HttpResponse(f.read(), content_type="application/ms-excel")
        response['Content-Disposition'] = 'attachment; filename={}_Report{}'.format('customer','.xlsx')
        return response

def Dashboard(request):
    
    if not check_user_login_status(request):
        return redirect(Login)
    else:
        admin  = get_admin(request)
        username = admin.username
        account_status = admin.account_status
        today = datetime.datetime.now()
        temperature = ''
        city = ''
        country = ''
        new_customers = ''
        duration = ''
        total_customers = admin.total_customers
        total_contact = admin.total_contact
        total_mail_id = admin.total_mail_id
        menus = [{
            'title':'DashBoard',
            'link':'dashboard'
            },
            {
            'title':'Chatbots',
            'link':'chatbots'
        }]
        list_menu = [
            # {
            #     'title':'Messaging',
            #     'item_1':'whatsup',
            #     'item_2':'instagram',
            #     'item_3':'facebook'
            # },
            # {
            #     'title':'Calls',
            #     'item_1':'whatsup',
            #     'item_2':'instagram',
            #     'item_3':'facebook'
            # }
        ]
        
        users  = Users.objects.filter(admin_email=admin.email)
        
        context = {
            'username' : username,
            'account_status' : account_status,
            'today':today,
            'temperature':temperature,
            'city':city,
            'country':country,
            'new_customers':new_customers,
            'duration':duration,
            'total_customers':total_customers,
            'total_contact':total_contact,
            'total_mail_id':total_mail_id,
            'menus':menus,
            'list_menu':list_menu,
            'Users':users
        }
        return render(request, 'dashboard/index.html',context)

def chatbots(request):
    return redirect(bot_registration)

@csrf_exempt
def whatsupbot(request):
    print(request)
    if request.method == 'POST':
        message = request.POST.get('Body')
        name = request.POST.get('ProfileName')
        From = request.POST.get('From')
        input_data = str(message).lower().split(' ')
        Bot_contact = '+14155238886'
        keywords = chatbot_keywords
        
        def send(data):
            message = client.messages.create(
                                    from_=f'whatsapp:{Bot_contact}',
                                    body=data,
                                    to=From
                                )
        # if isinstance(message,str):
        #     message = str(message).lower()
        # else:
        #     send('your replay is not found. please provide a valid replay')
        brain = 'collect_data'#intelligent, pretrained
        data = 'sry, i am not able to recognize you. my mind is blank.type start please.'
        if brain=='intelligent':
            data = getIntelligent(message)
        elif brain=='collect_data':
            if not Users.objects.filter(contact=From[9:]).exists():
                if BotCollection.objects.filter(Bot_contact=Bot_contact).exists():
                    new_user = Users.objects.create(contact=From[9:])
                    admin_email = BotCollection.objects.get(Bot_contact=Bot_contact).admin_email
                    new_user.admin_email = admin_email
                    new_user.save()
                    data = 'Hi, Seems like new to here. My name is Widy, i can here to assist you. I am here with a good news. I have opened an account for you just now. To start type "start"'
                    # print(From[9:])
                else:
                    data = 'Your bot does not belong to any user. Please be aware. '
            else:
                # if str(message).lower() == 'start':
                    user = Users.objects.get(contact=From[9:])
                    
                    if message == 'edit':
                        user.count = 0
                        user.save()
                    
                    if message == 'start':
                        user.count = 0
                        user.save()
                        
                    count = user.count
                    
                    if count == 0:
                        data = 'Please provide your first name.'
                        user.count = 1
                        user.save()
                    if count == 1:
                        user.first_name = message
                        data = 'Please provide your last name.'
                        user.count = 2
                        user.save()
                    if count ==2:
                        user.last_name = message
                        data = f'hello {user.first_name}, please provide your mail id?'
                        user.count = 3
                        user.save()
                    if count ==3:
                        if not str(message).find('@') == -1:
                            user.email = message
                            user.count = 4
                            user.save()
                            data = 'Thank you for your patients. We will contact you as soon as possible ?'
                        else:
                            data = 'we are sry, please provide a valid mail id.'
                    if count == 4:
                        data = 'We already have the neccessary details to connect with you.You are on our waiting list. Please type "edit", to change your details.'
                # else:
                #     data = 'You should type start to continue.'
        send(data)
    else:
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

