 
from bot.models import Users


def Reply(bot_template,user_contact,message,admin_email):
    
    user = Users.objects.get(contact=user_contact,admin_email=admin_email)
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
    
    reply = 'Something happened at my server. its not your problem, its ours. I will get back to you soon'
    for question in bot_template:
        #  replay if there is nother to ask.
        reply = 'Thank you, We will contact you soon.'
        got_a_question = False
        # if first_name required
        if question.first_name == 'enable':
            if user.first_name == '':
                reply = question.first_name_q
                user.waiting_for = 'first_name'
                user.save()
                break
        # if last_name required
        if question.last_name == 'enable':
            if user.last_name == '':
                reply = question.last_name_q
                user.waiting_for = 'last_name'
                user.save()
                break
        # if first_name required
        if question.contact == 'enable':
            if user.contact == '':
                reply = question.contact_q
                user.waiting_for = 'contact'
                user.save()
                break
        # if first_name required
        if question.email == 'enable':
            if user.email == '':
                reply = question.email_q
                user.waiting_for = 'email'
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