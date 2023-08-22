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
        expected_initial = {"phone_number": [9876543210]}
        # self.assertEqual(response.context["form"].initial, expected_initial)


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cart_view(self):
        response = self.client.get(reverse("orders:cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/cart.html")


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

    def test_add_order_view(self):
        print(self.add_order_url)
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

        self.assertEqual(order.customer, self.customer)
        self.assertEqual(order.table, self.table)
        self.assertEqual(order_item.order, order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.price, 10.00)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(
            session["orders_info"][str(order.id)][0]["product"], "Test Product"
        )
        self.assertEqual(session["orders_info"][str(order.id)][0]["price"], "10.00")
        self.assertEqual(session["orders_info"][str(order.id)][0]["quantity"], 2)
        self.assertEqual(session["orders_info"][str(order.id)][0]["sub_total"], "20.00")
        self.assertEqual(session["orders_info"][str(order.id)][1], "20.00")
        self.assertEqual(
            session["orders_info"][str(order.id)][2], self.customer.phone_number
        )
        self.assertNotIn(self.client.COOKIES["cart"], self.client.cookies)


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
