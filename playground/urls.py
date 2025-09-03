from django.urls import path
from . import views

#URLconfiguration
urlpatterns = [
    path('hello/',views.HelloView.as_view())
]
