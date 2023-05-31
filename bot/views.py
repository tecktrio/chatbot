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
from .chatbot_keywords import questions_for_data_collection_task
from django.views.decorators.csrf import csrf_exempt
from .intelligence import getIntelligent
# Create your views here.

# variables
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_TOKEN
client = Client(account_sid, auth_token)
waiting_for = ''
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
            if not BotCollection.objects.filter(Bot_contact=bot_contact).exists():
                if not BotCollection.objects.filter(Bot_name=bot_name).exists():
                    new_bot =BotCollection.objects.create(admin_email=admin.email,Bot_contact = bot_contact,Bot_name = bot_name, Bot_Task = bot_task)
                    new_bot.save()
                    return redirect(chatbots)
                else:
                    return render(request,'bot_registration.html',{'error':'Bot name is already taken'})
            else:
                return render(request,'bot_registration.html',{'error':'This bot is already registered.please check your bot list'})        
        else:
            return render(request,'bot_registration.html',{'error':'provide a valid bot number'})
    return render(request, 'bot_registration.html')

def Change_Bot_Status(request,contact):
    Bot_contact = contact
    try:
        bot = BotCollection.objects.get(Bot_contact=Bot_contact)
        
        if bot.Bot_Status == 'running':
            bot.Bot_Status = 'not_running'
        else:
            bot.Bot_Status = 'running'
        bot.save()
    except:
        pass
    return redirect(chatbots)
    
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
    try:
        email = request.COOKIES['widecity_chatbot_email']
        return Admins.objects.get(email=email)
    except:
        return redirect(Logout)
        

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
        duration = 'last 16 days'
        user = Users.objects.filter(admin_email=admin.email)
        total_customers = user.count()
        total_contact = user.count()
        total_mail_id = user.count()
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
    admin_email = get_admin(request).email
    bots = BotCollection.objects.filter(admin_email=admin_email)
    menus = [{
    'title':'DashBoard',
    'link':'dashboard'
    },
    {
    'title':'Chatbots',
    'link':'chatbots'
    }]
    context={
        'bots':bots,
        'menus':menus
        }
    return render(request,'Chatbots.html',context)


# This method works as the endpoint for whatsup bots

@csrf_exempt
def whatsupbot(request):
    # handles the post request comming from twilio
    '''This will only work if the access token and accound id is valid. '''
    if request.method == 'POST':
        # setting up global variables
        global waiting_for
        # gathering the neccessary fields from the post request
        message = request.POST.get('Body')
        name = request.POST.get('ProfileName')
        From = request.POST.get('From')
        To = request.POST.get('To')
        
        # filtering the data for processing
        message_as_list = str(message).lower().split(' ')
        bot_number = To[9:]
                
        # trying to make the incomming message to lower case for enabling non case sensitive
        try:
            message = str(message).lower()
        except:
            pass

        # this method will send the message back to the user/twilio
        def send(data):
            client.messages.create(
                                    from_=f'whatsapp:{bot_number}',
                                    body=data,
                                    to=From
                                )

        
        # Verifying the bot and choosing the type of brain
        # intelligent, pretrained , this can be changed from admin dashboard
        if BotCollection.objects.filter(Bot_contact=bot_number).exists():
            bot = BotCollection.objects.get(Bot_contact=bot_number)
            if bot.Bot_Status == 'running':
                brain = bot.Bot_Task
            else:
                send('I am very sorry, Currently my services are not available. Please contact the admin')
                return HttpResponse('bot is not running')
        else:
            send('I am not registered to any companies. Please register my number at bots.widecity.in if you are my owner.')
            return HttpResponse('bot is running')
            
        data = 'sry, i am not able to recognize you. my mind is blank.'
        
        # setting up the response system according to the brain
        if brain=='intelligent':
            # forwarding the control to intelligent system for response
            data = getIntelligent(message)
            
        elif brain=='collect_data':
            '''checking whether the user is new to the admin'''
            if not Users.objects.filter(contact=From[9:]).exists():
                '''New User'''
                # creating the user account
                new_user = Users.objects.create(contact=From[9:])
                print('New user, Account created successfully.')
                
                # getting the admin_details of the bot
                admin_email = BotCollection.objects.get(Bot_contact=bot_number).admin_email
                
                # adding this user account to the admin data
                new_user.admin_email = admin_email
                new_user.save()

                data = 'Hi, Seems like new to here. My name is Widy, i can here to assist you. I am here with a good news. I have opened an account for you just now."'
                send(data)
                whatsupbot(request)
            else:
                '''existing user'''
                # fetching the user information from database
                user = Users.objects.get(contact=From[9:])
                         
                # waiting for response from the user is the bot already asked one
                if user.waiting_for == 'first_name':
                    user.first_name = message
                    waiting_for = ''
                    user.save()
                if user.waiting_for == 'last_name':
                    user.last_name = message
                    waiting_for = ''
                    user.save()
                if user.waiting_for == 'email':
                    user.email = message
                    waiting_for = ''
                    user.save()
                if user.waiting_for == 'contact':
                    user.contact = message
                    waiting_for = ''
                    user.save()
                    
                    
                # preparing the questions to ask (update from dashboard)
                questions  = questions_for_data_collection_task
                
                # updating the questions to ask
                '''question are updated based on the question file that can be controlled from dashboard'''
                for question in questions:
                    field = question['field']
                    #  replay if there is nother to ask.
                    data = 'Thank you, We will contact you soon.'
                    got_a_question = False
                    # if first_name required
                    if 'first_name' == field:
                        if user.first_name == '':
                            data = question['ask']
                            got_a_question = True
                    # if last_name required
                    if 'last_name' == field:
                        if user.last_name == '':
                            data = question['ask']
                            got_a_question = True
                    # if emai is required
                    if 'email' == field:
                        if user.email == '':
                            data = question['ask']
                            got_a_question = True
                    #  if contact is required
                    if 'contact' == field:
                        if user.contact == '':
                            data = question['ask']
                            got_a_question = True
                            
                    user.waiting_for = field
                    user.save()
                    if got_a_question:
                        break
                        

                send(data)
                return HttpResponse('bot is running')
        return HttpResponse('bot is running')
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

