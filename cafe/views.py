from django.shortcuts import render
from django.views.generic import DetailView
from django.views import View
from .models import Product, Category
from orders.forms import CartAddForm
from django.db.models import Q
from dynamic.models import PageData


class HomeView(View):
    def get(self, request):
        all_categories = Category.objects.all()
        all_products = Product.objects.all()
        form = CartAddForm()
        page_data = PageData.get_page_date('Menu_Page')
        context = {
            "all_categories": all_categories,
            "all_products": all_products,
            "form": form,
            "page_data": page_data,
        }
        return render(request, "cafe/home.html", context)


class SearchView(View):
    def get(self, request):
        searched = request.GET.get("searched")
        results = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched)
        ).distinct()
        page_data = PageData.get_page_date('Search_Page')
        return render(request, "cafe/search_results.html", {"results": results, "page_data": page_data})

class ProductDetailView(DetailView):
    model = Product
    template_name = 'cafe/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartAddForm()
        return context


