from django.shortcuts import render
from django.views import View
from .models import Product
from django.db.models import Q

# Create your views here.
def Menu(request):
    context = {}
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
            'search_results.html'
        )
    
    def post(self, request):
        pass
        
