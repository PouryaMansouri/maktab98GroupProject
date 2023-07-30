from django.urls import path
from .views import Menu

app_name = 'cafe'

urlpatterns = [
        path('', Menu , name="menu"),
]