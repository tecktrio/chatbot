'''THIS CODE IS DEVELOPED BY WIDECITY FOR CHATBOT. THIS IS CURRENTLY WORKING AT bots.widecity.in'''
'''author : amal benny'''


# import boto3  # pip install boto3

# # Let's use Amazon S3
    
# importing the neccessary modules
import datetime
import json
import random
import pandas as pd

# from django 
from django.http                    import HttpResponse, JsonResponse
from django.shortcuts               import redirect, render
from django.views.decorators.csrf   import csrf_exempt

# from this package
from .              import reply_generator_model_1
from .serializers   import User_Serializer
from .models        import Admins, BotCollection, Templates_v1, Users
from .              import chatbot_keywords as elements
from .Response_system  import half_intelligent , fully_intelligent, pretrained

# other
from mybot.settings         import TWILIO_ACCOUNT_SID, TWILIO_TOKEN
from twilio.rest            import Client
from rest_framework.views   import APIView


# Initializing the Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_TOKEN)

# METHODS USED FOR BOT SERVICE IS GIVEN BELOW
@csrf_exempt
def bot_registration(request):
    '''METHOD IS USED TO REGISTER NEW BOT TO AN ADMIN'''
    admin =  get_admin(request)
    if request.method == 'POST':
        print('FETCHING DATA FROM REQUEST')
        bot_contact     = request.POST.get('bot_contact')
        bot_name        = request.POST.get('bot_name')
        bot_template    = request.POST.get('bot_task')
        
        print('VERIFYING AND STARTING BOT REGISTRATION PROCESS')
        if bot_contact != '':
            if not BotCollection.objects.filter(Bot_contact=bot_contact).exists():
                if not BotCollection.objects.filter(Bot_name=bot_name).exists():
                    new_bot =BotCollection.objects.create(admin_email=admin.email,Bot_contact = bot_contact,Bot_name = bot_name, Bot_Template = bot_template)
                    new_bot.save()
                    print(f'NEW BOT WITH BOT CONTACT "{new_bot.Bot_contact}" REGISTERED SUCCESSFULLY')
                    return redirect(chatbots)
                else:return render(request,'bot_registration.html',{'error':'Bot name is already taken'})
            else:return render(request,'bot_registration.html',{'error':'This bot is already registered.please check your bot list'})        
        else:return render(request,'bot_registration.html',{'error':'provide a valid bot number'})
        
    print(admin.email)
    templates = Templates_v1.objects.filter(admin_email=admin.email)
    print(templates)
    context = {
        'templates':templates
    }
    return render(request, 'bot_registration.html',context)

# METHOD USED TO RENDER THE BOT TEMPLATE PAGE
def templates(request):
    menus       = elements.template_menus
    admin       = get_admin(request)
    templates   = Templates_v1.objects.filter(admin_email = admin.email)
    
    context = {
        'menus'     :menus,
        'templates' :templates
    }
    return render(request, 'bot_templates.html',context)

def new_bot_tempates(request):
    admin           = get_admin(request)
    template_name   = random.randint(100000,999999)
    while Templates_v1.objects.filter(admin_email=admin.email, template_name=template_name).exists():
            template_name = random.randint(100000,999999)

    new = Templates_v1.objects.create(admin_email = admin.email, template_name=template_name)
    new.save()
    
    fields                  = Templates_v1.objects.get(id=new.id)
    end_elements            = elements.end_elements
    welcome_elements        = elements.welcome_elements
    confirmation_elements   = elements.confirmation_elements
    context                 = {
                                'fields' : fields,
                                'end_elements':end_elements,
                                'welcome_elements':welcome_elements,
                                'confirmation_elements':confirmation_elements
                            }
    return render(request,'new_bot_template.html',context)

@csrf_exempt
def change_bot_template(request):
    if request.method == 'POST':
        bot_id              = request.POST.get('id')
        template            = request.POST.get('template')
        bot                 =  BotCollection.objects.get(id=bot_id)
        bot.Bot_Template    = template
        bot.save()
    return redirect(to=chatbots)

@csrf_exempt
def edit_bot_tempates(request,id):  
    if request.method == 'POST':

        first_name      = request.POST.get('first_name')
        first_name_q    = request.POST.get('first_name_q')
        last_name       = request.POST.get('last_name')
        last_name_q     = request.POST.get('last_name_q')
        contact         = request.POST.get('contact')
        contact_q       = request.POST.get('contact_q')        
        email           = request.POST.get('email')
        email_q         = request.POST.get('email_q')
        template_name   = request.POST.get('template_name')
        welcome_message = request.POST.get('welcome_message')
        confirmation_message = request.POST.get('confirmation_message')
        end_message     = request.POST.get('end_message')
        queston_1       = request.POST.get('question_1')
        queston_2       = request.POST.get('question_2')
        queston_3       = request.POST.get('question_3')
        queston_4       = request.POST.get('question_4')
        queston_5       = request.POST.get('question_5')
        queston_1_q     = request.POST.get('queston_1_q')
        queston_2_q     = request.POST.get('queston_2_q')
        queston_3_q     = request.POST.get('queston_3_q')
        queston_4_q     = request.POST.get('queston_4_q')
        queston_5_q     = request.POST.get('queston_5_q')
        brain_model     = request.POST.get('brain_model')

        end_message_media               = request.FILES.get('end_message_media')
        confirmation_message_media      = request.FILES.get('confirmation_message_media')
        welcome_message_media           = request.FILES.get('welcome_message_media')
        
        # admin = get_admin(request)
        # Media.objects.create(admin_email=admin.email, media=end_message_media, media_type='image',media_url='https://s3.amazonaws.com/bots.widecity.in/'+end_message_media.name).save()
        # Media.objects.create(admin_email=admin.email, media=confirmation_message_media, media_type='image',media_url='https://s3.amazonaws.com/bots.widecity.in/'+confirmation_message_media.name).save()
        # Media.objects.create(admin_email=admin.email, media=welcome_message_media, media_type='image',media_url='https://s3.amazonaws.com/bots.widecity.in/'+welcome_message_media.name).save()
      

        template = Templates_v1.objects.get(id=id)  
              
        if str(first_name).strip() == 'on': template.first_name = 'enable'
        else: template.first_name = 'disable' 
                     
        if str(last_name).strip() == 'on': template.last_name = 'enable'
        else: template.last_name = 'disable'

        if str(contact).strip() == 'on': template.contact = 'enable'
        else: template.contact = 'disable'

        if str(email).strip() == 'on': template.email = 'enable'
        else: template.email = 'disable'  
                    
        if str(queston_1).strip() == 'on': template.quetion_1 = 'enable'
        else: template.quetion_1 = 'disable' 
                
                     
        if str(queston_2).strip() == 'on': template.quetion_2 = 'enable'
        else: template.quetion_2 = 'disable'
                     
        if str(queston_3).strip() == 'on': template.quetion_3 = 'enable'
        else: template.quetion_3 = 'disable'

        if str(queston_4).strip() == 'on': template.quetion_4 = 'enable'
        else: template.quetion_4 = 'disable'
        
        if str(queston_5).strip() == 'on': template.quetion_5 = 'enable'
        else: template.quetion_5     = 'disable'

        template.first_name_q       = first_name_q
        template.last_name_q        = last_name_q
        template.contact_q          = contact_q
        template.email_q            = email_q
        template.template_name      = template_name
        template.welcome_message    = welcome_message
        template.confirmation_message    = confirmation_message
        template.end_message        = end_message
        template.quetion_1_q        = queston_1_q
        template.quetion_2_q        = queston_2_q
        template.quetion_3_q        = queston_3_q
        template.quetion_4_q        = queston_4_q
        template.quetion_5_q        = queston_5_q
        template.brain_model        = brain_model
        template.welcome_message_media              = welcome_message_media
        template.end_message_media                  = end_message_media
        template.confirmation_message_media         = confirmation_message_media
        template.welcome_message_media_type         = 'image'
        template.end_message_media_type             = 'image'
        template.confirmation_message_media_type    = 'image'
        
        
        template.save()
        print(template.quetion_1)
        return redirect(templates)
    template                = Templates_v1.objects.get(id=id)
    end_elements            = elements.end_elements
    welcome_elements        = elements.welcome_elements
    confirmation_elements   = elements.confirmation_elements
    brain_models             = elements.brain_models
    context={
        'fields'                : template,
        'end_elements'          : end_elements,
        'welcome_elements'      : welcome_elements,
        'confirmation_elements' : confirmation_elements,
        'brain_models' : brain_models,
    }
    return render(request,'new_bot_template.html',context)


def Change_Bot_Status(request,contact):
    try:
        bot = BotCollection.objects.get(Bot_contact=contact)
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
        email               = request.POST.get('email')
        password            = request.POST.get('password')
        response            = ''
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
        email                           = request.POST.get('email')
        username                        = request.POST.get('username')
        password                        = request.POST.get('password')
        contact                         = request.POST.get('contact')
        new_admin                       = Admins.objects.create(username=username, password=password, contact=contact, email=email)
        response                        = ''
        authorization_token             = random.randint(1000000000,9999999999)
        new_admin.authorization_token   = authorization_token
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
    users           = Users.objects.all()
    serialized_data = User_Serializer(users,many=True)
    pd.DataFrame(serialized_data.data).to_excel('output.xlsx')
    path            = 'output.xlsx'
    response        = HttpResponse('downloading...')
    with open(path, 'rb') as f:
        response                            = HttpResponse(f.read(), content_type="application/ms-excel")
        response['Content-Disposition']     = 'attachment; filename={}_Report{}'.format('customer','.xlsx')
        return response

def Dashboard(request):
    
    if not check_user_login_status(request):
        return redirect(Login)
    else:
        admin               = get_admin(request)
        username            = admin.username
        account_status      = admin.account_status
        today               = datetime.datetime.now()
        temperature         = ''
        city                = ''
        country             = ''
        new_customers       = ''
        duration            = 'last 16 days'
        user                = Users.objects.filter(admin_email=admin.email)
        total_customers     = user.count()
        total_contact       = user.count()
        total_mail_id       = user.count()
        menus               = elements.template_menus
        list_menu           = [
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
            'username'          :username,
            'account_status'    :account_status,
            'today'             :today,
            'temperature'       :temperature,
            'city'              :city,
            'country'           :country,
            'new_customers'     :new_customers,
            'duration'          :duration,
            'total_customers'   :total_customers,
            'total_contact'     :total_contact,
            'total_mail_id'     :total_mail_id,
            'menus'             :menus,
            'list_menu'         :list_menu,
            'Users'             :users
        }
        return render(request, 'dashboard/index.html',context)

def chatbots(request):
    admin_email         = get_admin(request).email
    bots                = BotCollection.objects.filter(admin_email=admin_email)
    template_list       = Templates_v1.objects.filter(admin_email=admin_email)
    menus               = elements.template_menus
    context             = {
                            'bots'          :bots,
                            'menus'         :menus,
                            'template_list' :template_list
                        }
    return render(request,'Chatbots.html',context)


# This method works as the endpoint for whatsup bots

@csrf_exempt
def whatsupbot(request):
    # handles the post request comming from twilio
    '''This will only work if
    * Twilio Client Access token and twilio sid are valid
    * Make sure the endpoint is whatsupbot
    * Request should be post'''
    if request.method == 'POST':
        # gathering the neccessary fields from the post request
        message                     = request.POST.get('Body')
        # name = request.POST.get('ProfileName')
        user_number                 = request.POST.get('From')
        bot_number_with_platform    = request.POST.get('To')
        # filtering the data for processing
        bot_number                  = bot_number_with_platform[9:]
        
        # COLLECTED - MESSAGE, USER NUMBER, BOT NUMBER
        
        # trying to make the incomming message to lower case and removing the space around it as message filter
        try:message = str(message).lower().strip()
        except: pass
        # requesting the twilio to send message data from bot_number_with_platform to user_number
        # (***************************************************************************)
        
        def send(text='', media_url='' ,type='text'):
            media_url_list =[]
            SEND_STATUS =False
            print(type)
            if type == 'text':
                 client.messages.create(
                                            from_   = bot_number_with_platform,
                                            body    = text,
                                            to      = user_number
                                            )
            SEND_STATUS = True
            if type == 'media':
                    client.messages.create(
                                            from_       = bot_number_with_platform,
                                            media_url   = media_url_list.append(media_url),
                                            to          = user_number
                                        )
                    SEND_STATUS = True
                    
            if type == 'media_with_text': 
                    media_url_list.append(media_url)
                    print(media_url_list)
                    client.messages.create(
                                            from_       = bot_number_with_platform,
                                            body        = text,
                                            media_url   = media_url_list,
                                            to          = user_number
                                        )
                    SEND_STATUS = True
            if SEND_STATUS:        
                print('REPLAY SEND SUCCESSFULLY')
            else:
                print('FAILED TO SEND REPLY')
        # (*****************************************************************************)
        # Verifying the bot registration and choosing the type of brain
        # AVAILABLE BRAIN MODELS
        '''
        * PRETRAINED
        * HALF-INTELLIGENT
        * FULLY-INTELLIGENT
        '''
        if BotCollection.objects.filter(Bot_contact=bot_number).exists():
            bot = BotCollection.objects.get(Bot_contact=bot_number)
            if bot.Bot_Status == 'running':
                # ******************************************************************
                # Fetching the template that this particular bot use
                print('FETCHING THE BOT TEMPLATE')
                template_name  = bot.Bot_Template
                print('FETCHING THE ADMIN EMAIL FROM BOTCOLLECTION')
                try:
                    admin_email = BotCollection.objects.get(Bot_contact=bot_number).admin_email
                except:
                    reply = 'I am registered to any admin till now. Please tell the admin to register me.'
                    send(text=reply)
                    return HttpResponse('done')        
                try:
                    bot_template = Templates_v1.objects.get(template_name = template_name,admin_email=admin_email)
                except:
                    send(text='I am so sorry, i dont know what should i say.Please contact my owner.Tell him to select a template for me.')
                    return HttpResponse('bot does not have a response system')
                print('BOT TEMPLATE :',bot_template.template_name)
                # ***********************************************************************8
                brain_model = bot_template.brain_model
            else:
                send(text='I am very sorry, Currently my services are not available. Please contact the admin')
                return HttpResponse('bot is not running')
            
        else:
            send(text='I am not registered to any companies. Please register my number at bots.widecity.in if you are my owner.')
            return HttpResponse('bot is running')
            
        data = 'sry, i am not able to recognize you. my mind is blank.'
        
        
        # setting up the response system according to the brain
        print('SELECTING THE BRAIN MODEL AND PASSING THE REQUEST TO THE MODEL')
        if brain_model == 'half-intelligent':
            print('BRAIN MODEL : ','HALF-INTELLIGENT')
            reply, type = half_intelligent(message)
            send(reply,type)
            
        if brain_model == 'fully-intelligent':
            print('BRAIN MODEL : ','FULLY-INTELLIGENT')
            reply = fully_intelligent(message)
            send(reply,type)
            
        # forwarding the control to pretrained model for response
        if brain_model=='pretrained':
            print('BRAIN MODEL : ','PRETRAINED')
            text, media_url, type = pretrained(message=message, bot_number=bot_number, user_number=user_number,admin_email=admin_email,bot_template_name=template_name)
            send(text=text,media_url=media_url,type=type)
            
        return HttpResponse('bot is running')
    else:
        return HttpResponse("bot is running")

class webbot(APIView):
    @csrf_exempt
    def post(self,request):
        data    = json.load(request)
        key     = data.get('key')
        value   = data.get('value')
        if key == 'read':
            data = f'{value}'
        return JsonResponse({'status':'success','voice':data})

