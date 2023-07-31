from django.urls import path
from .views import Menu
from .views import HomeView ,ProductDetail , ProductDetail2, SearchView

app_name = 'cafe'

urlpatterns = [
    path('', Menu , name="menu"),
    path('home/', HomeView.as_view(), name='home'),
    path('search_results/', SearchView.as_view(), name='search_results'),
    path('product/' , ProductDetail.as_view() , name="product"),
    path('product_detail/<int:pk>/', ProductDetail2.as_view() , name="product_detail"),
]