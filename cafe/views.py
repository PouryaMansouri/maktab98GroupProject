from django.shortcuts import render
from django.views import View

# Create your views here.
def Menu(request):
    context = {}
    return render(request, 'cafe/home.html', context)

class HomeView(View):
    def get(self, request):
        return render(request, 'cafe/home.html')    

    def post(self, request):
        return render(request, 'home/home.html')
