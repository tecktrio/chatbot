from django.urls import path
from .views import mybot,whatsupbot,webbot
urlpatterns = [
    path('',mybot),
    path('/whatsupbot',whatsupbot),
    path('/webbot',webbot.as_view())
]