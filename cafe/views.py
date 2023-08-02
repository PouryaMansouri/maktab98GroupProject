from django.shortcuts import render
from django.views import View
from .models import Category, Product
from django.db.models import Q

# Create your views here.
def Menu(request):
    all_categories = Category.objects.all()
    all_products = Product.objects.all()

    context = {'all_categories': all_categories, 'all_products': all_products}
    return render(request, 'cafe/menu.html', context)

class HomeView(View):
    def get(self, request):
        return render(request, 'cafe/index.html')    

    def post(self, request):
        return render(request, 'cafe/index.html')

class SearchView(View):
    def get(self, request):
        searched = request.GET.get('searched')
        results = Product.objects.filter(
            Q(name__icontains=searched) | Q(description__icontains=searched)
        ).distinct()
        return render(
            request,
            'cafe/search_results.html',
            {'results': results}
        )
        
