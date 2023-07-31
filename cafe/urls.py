from django.urls import path
from .views import Menu
from .views import HomeView

app_name = 'cafe'

urlpatterns = [
    path('', Menu , name="menu"),
    path('home/', HomeView.as_view(), name='home'),
]