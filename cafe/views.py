from django.shortcuts import render
from django.views import View

# Create your views here.
def Menu(request):
    context = {}
    return render(request, 'cafe/menu.html', context)

class HomeView(View):
    def get(self, request):
        return render(request, 'home/index.html')    

    def post(self, request):
        return render(request, 'home/index.html')
