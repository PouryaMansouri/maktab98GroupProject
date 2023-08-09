from django.urls import path
from . import views


app_name='orders'

urlpatterns = [
    path('add_order/', views.AddOrderView.as_view(), name='add_order'),
    path('detail/' , views.OrderDetailView.as_view() , name='order_detail'),
    path('cart/', views.CartView.as_view(),name='cart'),
    path('cart/add/<int:product_id>/', views.CartAddView.as_view() , name="cart_add"),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view() , name="cart_remove"),
    path('<int:pk>/accept/', views.order_accept, name='order_accept'),
    path('<int:pk>/reject/', views.order_reject, name='order_reject'),
    path('checkout/' , views.CheckoutView.as_view() , name='checkout'),
]
