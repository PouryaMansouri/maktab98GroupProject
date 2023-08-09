from django.urls import path
from . import views


app_name = "orders"

urlpatterns = [
    path("add_order/", views.AddOrderView.as_view(), name="add_order"),
    path("order_detail/", views.OrderDetailView.as_view(), name="order_detail"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart_add/<int:product_id>/", views.CartAddView.as_view(), name="cart_add"),
    path(
        "cart_remove/<int:product_id>/",
        views.CartRemoveView.as_view(),
        name="cart_remove",
    ),
    path("accept/<int:pk>", views.OrderAccept.as_view(), name="order_accept"),
    path("reject/<int:pk>", views.OrderReject.as_view(), name="order_reject"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
]
