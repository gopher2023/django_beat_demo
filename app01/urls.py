
from django.contrib import admin
from django.urls import path
from .views import send_mail_view
urlpatterns = [
    path('send/', send_mail_view),
]
