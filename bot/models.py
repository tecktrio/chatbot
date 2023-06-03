from django.db import models

# Create your models here.
class Users(models.Model):
    admin_email = models.CharField(max_length=100,default='')
    email=models.CharField(max_length=100,default='')
    contact=models.CharField(max_length=100,default='')
    bot_contact=models.CharField(max_length=20,default='')
    # count = models.IntegerField(default=-1)#1,2,3
    first_name=models.CharField(max_length=100,default='')
    last_name=models.CharField(max_length=100,default='')
    waiting_for=models.CharField(max_length=100,default='')
    
    
    def __str__(self) -> str:
        return self.contact
    
class Admins(models.Model):
    email=models.CharField(max_length=100)
    username=models.CharField(max_length=100)
    contact=models.CharField(max_length=20)
    authorization_token = models.CharField(max_length=200,default='')
    password = models.CharField(max_length=100)
    total_customers=models.CharField(max_length=100,default='')
    total_contact=models.CharField(max_length=100,default='')
    total_mail_id=models.CharField(max_length=100,default='')
    account_status=models.CharField(max_length=100,default='running',choices=(('pending','pending'),('running','running'),('broken','broken')))
    
    def __str__(self) -> str:
        return self.email
    
class BotCollection(models.Model):
    admin_email=models.CharField(max_length=100)
    Bot_contact=models.CharField(max_length=20)
    Bot_name=models.CharField(max_length=20,default='')
    Bot_Template=models.CharField(max_length=20,choices=(('intelligent_bot','intelligent_bot'),('collect_data','collect_data')),default='collect_data')
    Bot_Status=models.CharField(max_length=20,choices=(('running','running'),('not_running','not_running')),default='running')
    
    
    def __str__(self) -> str:
        return self.admin_email
    

class Templates_v1(models.Model):
    template_name = models.CharField(max_length=100,default='new template')
    admin_email = models.CharField(max_length=100,default='')
    template_status = models.CharField(max_length=100,default='disable')
    first_name = models.CharField(max_length=50,default='disable')
    first_name_q = models.CharField(max_length=100,default='what is your first name?' )
    last_name = models.CharField(max_length=50,default='disable')
    last_name_q = models.CharField(max_length=100,default='what is your Last name?' )
    contact = models.CharField(max_length=50,default='disable')
    contact_q = models.CharField(max_length=100,default='Please provide your contact ?' )
    email = models.CharField(max_length=50,default='disable')
    email_q = models.CharField(max_length=100,default='what is your Mail id?' )
    quetion_1 = models.CharField(max_length=50,default='disable')
    quetion_1_q = models.CharField(max_length=100,default='question 1' )
    quetion_2 = models.CharField(max_length=50,default='disable')
    quetion_2_q = models.CharField(max_length=100,default='question 2' )
    quetion_3 = models.CharField(max_length=50,default='disable')
    quetion_3_q = models.CharField(max_length=100,default='question 3' )
    quetion_4 = models.CharField(max_length=50,default='disable')
    quetion_4_q = models.CharField(max_length=100,default='question 4' )
    quetion_5 = models.CharField(max_length=50,default='disable')
    quetion_5_q = models.CharField(max_length=100,default='question 5' )
    welcome_message = models.CharField(max_length=500,default='hi' )
    end_message = models.CharField(max_length=500,default='thank you' )
    confirmation_message = models.CharField(max_length=500,default='confirm your details' )
    
class Media(models.Model):
    admin_email = models.CharField(max_length=100)
    media = models.CharField(max_length=100)
    media_type = models.CharField(max_length=100)