 
import re
from bot.models import Templates_v1, Users
from . import chatbot_keywords

def Reply(bot_template_name,user_contact,message,admin_email):
    New_Question_Ready = False
    user = Users.objects.get(contact=user_contact,admin_email=admin_email)
    bot_template = Templates_v1.objects.get(template_name = bot_template_name,admin_email=admin_email)
    # waiting for response from the user is the bot already asked one
    if user.waiting_for == 'first_name':
        user.first_name = message
        user.save()
    if user.waiting_for == 'last_name':
        user.last_name = message
        user.save()
    if user.waiting_for == 'email':
        user.email = message
        user.save()
    if user.waiting_for == 'contact':
        user.contact = message
        user.save()
    if user.waiting_for == 'question_1':
        user.question_1 = message
        user.save()
    if user.waiting_for == 'question_2':
        user.question_2 = message
        user.save()
    if user.waiting_for == 'question_3':
        user.question_3 = message
        user.save()
    if user.waiting_for == 'question_4':
        user.question_4 = message
        user.save()
    if user.waiting_for == 'question_5':
        user.question_5 = message
        user.save()
    if user.waiting_for == 'confirmation':
        print(message)
        if message == 'yes' or message == 'y':
            user.waiting_for = 'done'
            media_url = chatbot_keywords.MediaUrl+str(bot_template.end_message_media)
            user.save()
            text =  bot_template.end_message
            type = 'media_with_text'
            return text, media_url, type
        elif message =='1':
            user.waiting_for = 'first_name'
            media_url = ''
            text =  bot_template.first_name_q
            type = 'text'
            return text, media_url, type
        elif message =='2':
            user.waiting_for = 'last_name'
            media_url = ''
            text =  bot_template.last_name_q
            type = 'text'
            return text, media_url, type
        elif message =='3':
            user.waiting_for = 'contact'
            media_url = ''
            text =  bot_template.contact_q
            type = 'text'
            return text, media_url, type
        elif message =='4':
            user.waiting_for = 'email'
            media_url = ''
            text =  bot_template.email_q
            type = 'text'
            return text, media_url, type
    
    reply = 'Something happened at my server. its not your problem, its ours. I will get back to you soon'
    #  replay if there is nother to ask.
    reply = 'Thank you, We will contact you soon.'
    # if first_name required
    while True:
        if bot_template.first_name == 'enable':
            if user.first_name == '':
                text = bot_template.first_name_q
                media_url = ''
                type = 'text'
                user.waiting_for = 'first_name'
                New_Question_Ready = True
                user.save()
                break
        # if last_name required
        if bot_template.last_name == 'enable':
            if user.last_name == '':
                text = bot_template.last_name_q
                media_url = ''
                type = 'text'
                user.waiting_for = 'last_name'
                New_Question_Ready = True
                user.save()
                break
        # if first_name required
        if bot_template.contact == 'enable':
            if user.contact == '':
                text = bot_template.contact_q
                media_url = ''
                type = 'text'
                user.waiting_for = 'contact'
                New_Question_Ready = True
                user.save()
                break
        # if first_name required
        if bot_template.email == 'enable':
            if user.email == '':
                text = bot_template.email_q
                media_url = ''
                type = 'text'
                user.waiting_for = 'email'
                New_Question_Ready = True
                user.save()
                break
        # if first_name required
        if bot_template.quetion_1 == 'enable':
            if user.question_1 == '':
                text = bot_template.quetion_1_q
                media_url = ''
                type = 'text'
                user.waiting_for = 'question_1'
                New_Question_Ready = True
                user.save()
                break
        # if first_name required
        if bot_template.quetion_2 == 'enable':
            if user.question_2 == '':
                text = bot_template.quetion_2_q
                media_url = ''
                type = 'text'
                user.waiting_for = 'question_2'
                New_Question_Ready = True
                user.save()
                break
        # if first_name required
        if bot_template.quetion_3 == 'enable':
            if user.question_3 == '':
                text = bot_template.quetion_3_q
                media_url = ''
                type = 'text'
                user.waiting_for = 'question_3'
                New_Question_Ready = True
                user.save()
                break
        # if first_name required
        if bot_template.quetion_4 == 'enable':
            if user.question_4 == '':
                text = bot_template.quetion_4_q
                media_url = ''
                type = 'text'
                user.waiting_for = 'question_4'
                New_Question_Ready = True
                user.save()
                break
        # if first_name required
        if bot_template.quetion_5 == 'enable':
            if user.question_5 == '':
                text = bot_template.quetion_5_q
                media_url = ''
                type = 'text'
                user.waiting_for = 'question_5'
                New_Question_Ready = True
                user.save()
                break
            
        if New_Question_Ready == False:
            text = bot_template.confirmation_message
            text = text.replace('$first_name$',user.first_name)
            text = text.replace('$last_name$',user.last_name)
            text = text.replace('$contact$',user.contact)
            text = text.replace('$email$',user.email)
            text = text.replace('$next_line$','\n')
            text = text + '\n' + chatbot_keywords.edit_message
  
            # media_url = chatbot_keywords.MediaUrl+str(bot_template.end_message_media)
            media_url = ''
            type = 'text'
            user.waiting_for = 'confirmation'
            user.save()
            break
        # if first_name required
        # if question.quetion_1 == 'enable':
        #     if user.quetion_1 == '':
        #         text = question.quetion_1_q
        #         user.waiting_for = 'question_1'
        #         user.save()
        #         break
        
    return text, media_url, type