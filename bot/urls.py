from django.urls import path
from .views import mybot,whatsupbot
urlpatterns = [
    path('',mybot),
    path('/whatsupbot',whatsupbot)
]