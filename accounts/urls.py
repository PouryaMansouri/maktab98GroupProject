from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('verify_personnel/', views.UserVerifyPersonnelView.as_view(), name='verify_personnel'),
    path('manage_orders/' , views.ManageOrders.as_view() , name='manage_orders'),
]