from django.db import models

# Create your models here.
class Users(models.Model):
    admin_email = models.CharField(max_length=100,default='')
    email=models.CharField(max_length=100,default='')
    contact=models.CharField(max_length=20)
    count = models.IntegerField(default=-1)#1,2,3
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
    Bot_Task=models.CharField(max_length=20,choices=(('intelligent_bot','intelligent_bot'),('collect_data','collect_data')),default='collect_data')
    Bot_Status=models.CharField(max_length=20,choices=(('running','running'),('not_running','not_running')),default='running')
    
    
    def __str__(self) -> str:
        return self.admin_email
    

class Templates_v1(models.Model):
    template_name = models.CharField(max_length=100,default='')
    template_status = models.CharField(max_length=100,default='')
    first_name = models.CharField(max_length=50,choices=(('enable','enable'),('disable','disable')))
    last_name = models.CharField(max_length=50,choices=(('enable','enable'),('disable','disable')))
    contact = models.CharField(max_length=50,choices=(('enable','enable'),('disable','disable')))
    email = models.CharField(max_length=50,choices=(('enable','enable'),('disable','disable')))
    quetion_1 = models.CharField(max_length=50,choices=(('enable','enable'),('disable','disable')))
    quetion_2 = models.CharField(max_length=50,choices=(('enable','enable'),('disable','disable')))
    quetion_3 = models.CharField(max_length=50,choices=(('enable','enable'),('disable','disable')))
    quetion_4 = models.CharField(max_length=50,choices=(('enable','enable'),('disable','disable')))
    quetion_5 = models.CharField(max_length=50,choices=(('enable','enable'),('disable','disable')))
    