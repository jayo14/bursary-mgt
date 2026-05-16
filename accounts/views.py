from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django import forms

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('dashboard')

class StudentSignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = User.Role.STUDENT
        if commit:
            user.save()
        return user

class StudentSignupView(CreateView):
    model = User
    form_class = StudentSignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users_list'

    def test_func(self):
        return self.request.user.role == 'ADMIN'

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        search = self.request.GET.get('search')
        role = self.request.GET.get('role')
        
        if search:
            queryset = queryset.filter(
                Q(username__icontains=search) | 
                Q(first_name__icontains=search) | 
                Q(last_name__icontains=search) | 
                Q(email__icontains=search)
            )
        
        if role and role != 'ALL':
            queryset = queryset.filter(role=role)
            
        return queryset

class UserToggleStatusView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User

    def test_func(self):
        return self.request.user.role == 'ADMIN'

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=kwargs['pk'])
        user.is_active = not user.is_active
        user.save()
        
        if request.htmx:
            return render(request, 'accounts/partials/user_row.html', {'target_user': user})
        return redirect('user_list')
