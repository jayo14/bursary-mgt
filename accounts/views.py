from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import StudentSignupForm, LoginForm
from .models import User

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = LoginForm
    
    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.role == User.Role.ADMIN:
                return reverse_lazy('admin_dashboard')
            return reverse_lazy('dashboard')
        return reverse_lazy('login')

class StudentSignupView(CreateView):
    model = User
    form_class = StudentSignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

class DashboardRedirectView(TemplateView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        if request.user.role == User.Role.ADMIN:
            return redirect('admin_dashboard')
        return redirect('student_dashboard')
