 
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
    if user.waiting_for == 'confirmation':
        if message == 'yes' or message == 'y':
            user.waiting_for = 'done'
            user.save()
            return reply
        pass
    
    reply = 'Something happened at my server. its not your problem, its ours. I will get back to you soon'
    #  replay if there is nother to ask.
    reply = 'Thank you, We will contact you soon.'
    # if first_name required
    while True:
        if bot_template.first_name == 'enable':
            if user.first_name == '':
                reply = bot_template.first_name_q
                user.waiting_for = 'first_name'
                New_Question_Ready = True
                user.save()
                break
        # if last_name required
        if bot_template.last_name == 'enable':
            if user.last_name == '':
                reply = bot_template.last_name_q
                user.waiting_for = 'last_name'
                New_Question_Ready = True
                user.save()
                break
        # if first_name required
        if bot_template.contact == 'enable':
            if user.contact == '':
                reply = bot_template.contact_q
                user.waiting_for = 'contact'
                New_Question_Ready = True
                user.save()
                break
        # if first_name required
        if bot_template.email == 'enable':
            if user.email == '':
                reply = bot_template.email_q
                user.waiting_for = 'email'
                New_Question_Ready = True
                user.save()
                break
            
        if New_Question_Ready == False:
            reply = bot_template.end_message
            reply = reply.replace('$first_name$',user.first_name)
            reply = reply.replace('$last_name$',user.last_name)
            reply = reply.replace('$contact$',user.contact)
            reply = reply.replace('$email$',user.email)
            reply = reply.replace('$next_line$','\n')
            reply = reply.replace('$next_line$','\n')
            reply = reply + '\n' + chatbot_keywords.edit_message
            user.waiting_for = 'confirmation'
            user.save()
            break
        # if first_name required
        # if question.quetion_1 == 'enable':
        #     if user.quetion_1 == '':
        #         reply = question.quetion_1_q
        #         user.waiting_for = 'question_1'
        #         user.save()
        #         break
        
    return reply