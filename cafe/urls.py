from django.urls import path
from .views import SearchView, HomeView

app_name = "cafe"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("search_results/", SearchView.as_view(), name="search_results"),
]
