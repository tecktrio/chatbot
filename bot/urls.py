from django.urls import path
from .views import Download_exel,whatsupbot,webbot,Dashboard,Login,templates,edit_bot_tempates
from .views import SignUp,Logout,bot_registration,chatbots,Change_Bot_Status,new_bot_tempates
urlpatterns = [
    path('',Login),
    path('whatsupbot',whatsupbot),
    path('webbot',webbot.as_view()),
    path('dashboard',Dashboard),
    path('login',Login),
    path('logout',Logout),
    path('signup',SignUp),
    path('bot_registration',bot_registration),
    path('chatbots',chatbots),
    path('templates',templates),
    path('new_bot_template',new_bot_tempates),
    # path('edit_bot_template',edit_bot_tempates),
    path('edit_bot_template/<int:id>',edit_bot_tempates),
    path('download_excel',Download_exel),
    path('change_bot_status/<str:contact>',Change_Bot_Status),
]
# openpyxl