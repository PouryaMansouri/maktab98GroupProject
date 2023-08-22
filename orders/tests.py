from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from .views import ReorderView
from .models import Table, Order, OrderItem
from accounts.models import Customer
from cafe.models import Product
import json
import urllib.parse
from model_bakery import baker
from accounts.models import Personnel
from django.contrib.sessions.middleware import SessionMiddleware
from .views import OrdersHistoryView


class CheckoutViewTest(TestCase):
    def test_get(self):
        session_data = {
            "orders_info": {
                "order1": [
                    {"key1": "value1"},
                    {"key2": "value2"},
                    [1234567890],
                ],
                "order2": [
                    {"key3": "value3"},
                    {"key4": "value4"},
                    [9876543210],
                ],
            }
        }

        self.client.session.update(session_data)
        url = reverse("orders:checkout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/checkout.html")
        # expected_initial = {"phone_number": [9876543210]}
        # self.assertEqual(response.context["form"].initial, expected_initial)


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cart_view(self):
        response = self.client.get(reverse("orders:cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/cart.html")


class OrderRejectTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.personnel = baker.make(Personnel)
        self.order = baker.make(Order, personnel=self.personnel, status="p")

    def test_order_rejection(self):
        self.client.force_login(self.personnel)
        url = reverse("orders:order_reject", kwargs={"pk": self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("accounts:dashboard"))
        updated_order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(updated_order.status, "r")
        self.assertEqual(updated_order.personnel, self.personnel)


class OrderAcceptTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.personnel = baker.make(Personnel)
        self.order = baker.make(Order, personnel=self.personnel, status="p")

    def test_order_rejection(self):
        self.client.force_login(self.personnel)
        url = reverse("orders:order_accept", kwargs={"pk": self.order.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("accounts:dashboard"))
        updated_order = Order.objects.get(pk=self.order.pk)
        self.assertEqual(updated_order.status, "a")
        self.assertEqual(updated_order.personnel, self.personnel)


"""
class OrdersHistoryViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = baker.make(Personnel)
        self.order = baker.make(Order)

    def test_get_with_orders(self):
        request = self.factory.get("orders:order_history")
        request.user = self.user
        middleware = SessionMiddleware(get_response=None)
        middleware.process_request(request)
        request.session.save()
        request.session["orders_info"] = {self.order.id: "some_value"}
        request.session.save()

        response = OrdersHistoryView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/orders_history.html")
        self.assertContains(response, self.order.id)

    def test_get_without_orders(self):
        request = self.factory.get("/orders/history/")
        request.user = self.user

        response = OrdersHistoryView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/orders_history.html")
        self.assertNotContains(response, "orders:order_id")
"""


"""
class AddOrderViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_order_url = reverse("orders:add_order")
        self.table = baker.make(Table, table_number=1)
        self.product = baker.make(Product, name="Test Product", price=10.00)
        self.customer = baker.make(Customer)
        self.order = baker.make(Order, table=self.table, customer=self.customer)
        self.orderitem = baker.make(OrderItem, order=self.order, product=self.product)
        self.customer = baker.make(Customer)
        self.cart = {
            "1": {
                "name": "Test Product",
                "price": "10.00",
                "quantity": 2,
                "sub_total": "20.00",
            },
            "total_price": "20.00",
        }

    def test_post(self):
        session = self.client.session
        session["orders_info"] = {}
        session.save()
        self.client.cookies["cart"] = urllib.parse.quote(json.dumps(self.cart))
        response = self.client.post(
            reverse("orders:add_order"),
            {
                "phone_number": self.customer.phone_number,
                "table_number": self.table.table_number,
            },
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
        self.assertEqual(len(session["orders_info"]), 1)

        order = Order.objects.first()
        order_item = OrderItem.objects.first()

        self.assertEqual(session["orders_info"][str(order.id)][0]["price"], "10.00")
        self.assertEqual(session["orders_info"][str(order.id)][0]["quantity"], 2)
        self.assertEqual(session["orders_info"][str(order.id)][0]["sub_total"], "20.00")
        self.assertEqual(session["orders_info"][str(order.id)][1], "20.00")
        self.assertEqual(
            session["orders_info"][str(order.id)][2], self.customer.phone_number
        )
        self.assertNotIn(self.client.COOKIES["cart"], self.client.cookies)
"""
