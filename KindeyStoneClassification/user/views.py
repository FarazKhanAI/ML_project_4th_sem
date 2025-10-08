from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from .forms import CustomUserCreationForm, CustomAuthenticationForm

class RegisterView(View):
    """
    Handles user registration with custom form
    """
    template_name = 'user/register.html'
    form_class = CustomUserCreationForm
    
    @method_decorator(csrf_protect)
    def get(self, request):
        # Redirect authenticated users to dashboard
        if request.user.is_authenticated:
            return redirect('classification:home')
        
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password1', 'password2'))
    def post(self, request):
        form = self.form_class(request.POST)
        
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.save()
                
                # Auto-login after registration
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password1')
                user = authenticate(request, username=email, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Account created successfully! Welcome to KidneyStoneAI.')
                    return redirect('classification:home')
                else:
                    messages.error(request, 'Registration successful but automatic login failed. Please login manually.')
                    return redirect('user:login')
                    
            except Exception as e:
                messages.error(request, f'Error creating account: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, self.template_name, {'form': form})

class LoginView(View):
    """
    Handles user authentication
    """
    template_name = 'user/login.html'
    form_class = CustomAuthenticationForm
    
    @method_decorator(csrf_protect)
    def get(self, request):
        # Redirect authenticated users to dashboard
        if request.user.is_authenticated:
            return redirect('classification:home')
        
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
    
    @method_decorator(csrf_protect)
    @method_decorator(sensitive_post_parameters('password'))
    def post(self, request):
        form = self.form_class(request, data=request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_short_name()}!')
                
                # Redirect to next parameter if exists
                next_url = request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('classification:home')
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
        
        return render(request, self.template_name, {'form': form})

class LogoutView(View):
    """
    Handles user logout
    """
    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            messages.info(request, 'You have been successfully logged out.')
        return redirect('user:login')