from django.shortcuts import render
from django.views import View
from .models import Product

# Create your views here.
def Menu(request):
    products = Product.objects.all()
    context = {}
    return render(request, 'cafe/menu.html',  {'products':products})

class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')    

    def post(self, request):
        return render(request, 'home/index.html')
    
class ProductDetail(View):
    def get(self , request):
        products = Product.objects.filter(is_available = True)
        return render(request, 'cafe/product.html' , {'products':products})


class ProductDetail2(View):
    def get(self , request , pk):
        productd = Product.objects.get(pk=pk)
        return render(request, 'cafe/product_detail.html' , {'productd':productd})