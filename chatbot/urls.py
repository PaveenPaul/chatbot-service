from django.urls import path
from chatbot import views
urlpatterns = [
    path("", views.chatbot_view, name="chatbot"),
]
