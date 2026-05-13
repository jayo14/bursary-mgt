from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class DashboardView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        if request.user.role == 'ADMIN':
            return redirect('admin_dashboard')
        return redirect('student_dashboard')

class StudentDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/student.html'

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/admin.html'
