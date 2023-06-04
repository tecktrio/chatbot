import openai
from bot import reply_generator_model_1
from bot.models import BotCollection, Templates_v1, Users
from mybot.settings import OPEN_AI_KEY
openai.organization = "org-1VZK0fl8oXM4HK6zyoHJNi6F"
openai.api_key = OPEN_AI_KEY
messages = []
def fully_intelligent(question):
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
        type = ''
        return reply , type
    
def half_intelligent(question):
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
    
def pretrained(message, bot_number, user_number, bot_template_name,admin_email):
        # ///////////  FILTERING THE USER FROM 10000 OF REQUEST /////
        # ////////////////////////////////////////////////////////////
        
        # GETTING THE ADMIN DETAILS TO WHOM THE BOT BELONGS TO
        try:
            bot_template = Templates_v1.objects.get(template_name = bot_template_name,admin_email=admin_email)
        except:
            pass
        print('BOT TEMPLATE :',bot_template.template_name)

        # CHECKING WHETHER THE USER IS NEW TO THE ADMIN
        if not Users.objects.filter(contact=user_number,admin_email=admin_email).exists():
            '''New User'''
            # creating the user account
            new_user = Users.objects.create(contact=user_number,admin_email=admin_email)
            print('New user, Account created successfully.')
        
            new_user.save()

            text = bot_template.welcome_message
            media_url = ''
            type = 'text'
            return text, media_url, type
            # pretrained(request)
        else:
            '''existing user'''
            # fetching the user information from database
            user            = Users.objects.get(contact=user_number,admin_email=admin_email)

            # updating the questions to ask
            '''question are updated based on the question file that can be controlled from dashboard'''
            user_contact    = user.contact
            text, media_url, type          = reply_generator_model_1.Reply(bot_template.template_name,user_contact,message,admin_email)    
            
            if user.waiting_for == 'done':  
                text = 'done'

            print('RETURNING REPLAY')
           

            return text, media_url, type