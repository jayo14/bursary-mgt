from django.urls import path
from . import views

urlpatterns = [
    path('', views.DisbursementListView.as_view(), name='disbursement_list'),
    path('<int:pk>/process/', views.DisbursementProcessView.as_view(), name='disbursement_process'),
]
