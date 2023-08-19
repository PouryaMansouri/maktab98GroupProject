# django imports
from django.urls import path

# inner modules imports
from . import views


app_name = "orders"

urlpatterns = [
    path("add_order/", views.AddOrderView.as_view(), name="add_order"),
    path("orders_history/", views.OrdersHistoryView.as_view(), name="orders_history"),
    path("reorder/<int:order_id>", views.ReorderView.as_view(), name="reorder"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart_add/<int:product_id>/", views.CartAddView.as_view(), name="cart_add"),
    path(
        "cart_remove/<int:product_id>/",
        views.CartRemoveView.as_view(),
        name="cart_remove",
    ),
    path("order_accept/<int:pk>", views.OrderAccept.as_view(), name="order_accept"),
    path("order_reject/<int:pk>", views.OrderReject.as_view(), name="order_reject"),
    path("checkout/", views.CheckoutView.as_view(), name="checkout"),
]
