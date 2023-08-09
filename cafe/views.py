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


class SearchView(View):
    def get(self, request):
        searched = request.GET.get("searched")
        results = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched)
        ).distinct()
        return render(request, "cafe/search_results.html", {"results": results})
