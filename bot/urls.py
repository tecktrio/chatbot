from django.urls import path
from .views import Download_exel,whatsupbot,webbot,Dashboard,Login,SignUp,Logout,bot_registration,chatbots
urlpatterns = [
    path('',Login),
    path('/whatsupbot',whatsupbot),
    path('/webbot',webbot.as_view()),
    path('/dashboard',Dashboard),
    path('/login',Login),
    path('/logout',Logout),
    path('/signup',SignUp),
    path('/bot_registration',bot_registration),
    path('/chatbots',chatbots),
    path('/download_excel',Download_exel),
]
# openpyxl