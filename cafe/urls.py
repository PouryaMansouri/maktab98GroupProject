from django.urls import path
from .views import Menu
from .views import SearchView

app_name = "cafe"

urlpatterns = [
    path("", Menu, name="menu"),
    path("search_results/", SearchView.as_view(), name="search_results"),
]
