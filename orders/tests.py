from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from .views import CartView
from .cart import Cart


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_cart_view(self):
        response = self.client.get(reverse("orders:cart"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/cart.html")
        self.assertIsInstance(response.context["cart"], Cart)
