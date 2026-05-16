from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404, redirect
from .models import User
from django.db.models import Q

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
