from django.urls import path
from . import views

#URLconfiguration
urlpatterns = [
    path('hello/',views.say_hello)
]