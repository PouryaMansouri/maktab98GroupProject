from django.shortcuts import render
from django.views import View
from .models import Product, Category
from orders.forms import CartAddForm
from django.db.models import Q

def Menu(request):
    all_categories = Category.objects.all()
    all_products = Product.objects.all()
    form = CartAddForm()
    context = {
        "all_categories": all_categories,
        "all_products": all_products,
        "form": form,
    }
    return render(request, "cafe/home.html", context)

class HomeView(View):
    def get(self, request):
        return render(request, "cafe/home.html")

    def post(self, request):
        return render(request, "cafe/home.html")


class SearchView(View):
    def get(self, request):
        searched = request.GET.get("searched")
        results = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched)
        ).distinct()
        return render(request, "cafe/search_results.html", {"results": results})


class ProductDetail(View):
    def get(self, request):
        products = Product.objects.filter(is_available=True)
        return render(request, "cafe/product.html", {"products": products})


class ProductDetail2(View):
    def get(self, request, pk):
        productd = Product.objects.get(pk=pk)
        return render(request, "cafe/product_detail.html", {"productd": productd})
