from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('student/', views.StudentDashboardView.as_view(), name='student_dashboard'),
    path('admin/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]
