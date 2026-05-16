from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.ApplicationWizardView.as_view(), name='apply'),
    path('<int:pk>/', views.ApplicationDetailView.as_view(), name='application_detail'),
    path('<int:pk>/review/', views.ApplicationReviewView.as_view(), name='application_review'),
]
