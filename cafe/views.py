from django.shortcuts import render
from django.views import View
from .models import Category, Product

# Create your views here.
def Menu(request):
    all_categories = Category.objects.all()
    all_products = Product.objects.all()
    context = {'all_categories': all_categories, 'all_products': all_products}
    return render(request, 'cafe/home.html', context)

class HomeView(View):
    def get(self, request):
        return render(request, 'cafe/home.html')    

    def post(self, request):
        return render(request, 'cafe/home.html')    

    def post(self, request):
        return render(request, 'cafe/home.html')
