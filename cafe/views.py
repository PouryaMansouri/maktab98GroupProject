from django.shortcuts import render

# Create your views here.
def Menu(request):
    context = {}
    return render(request, 'menu.html', context)