from django.shortcuts import render, redirect
from django.views import View
from forms import UserLoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Create your views here.
class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    
    def dispatch(self, request, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(
            request,
            self.template_name,
            {'form' : form }
        )
        
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username = cd['phone_number'],
                password = cd['password']
            )
            if user is not None:
                login(request, user)
                messages.success(
                    request,
                    'Logged in Successfully',
                    'success'
                )
                return redirect('index')
            messages.error(
                request,
                'Invalid Phone number or password'
            )
        return render(request, self.template_name, {'form' : form})
            
            