from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum, Avg
from applications.models import Application
from disbursements.models import Disbursement

class ReportsDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'reports/dashboard.html'

    def test_func(self):
        return self.request.user.role == 'ADMIN'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Aggregations
        context['total_applications'] = Application.objects.count()
        context['approved_count'] = Application.objects.filter(status='APPROVED').count()
        context['total_disbursed'] = Disbursement.objects.filter(status='PAID').aggregate(Sum('amount'))['amount__sum'] or 0
        
        if context['total_applications'] > 0:
            context['approval_rate'] = (context['approved_count'] / context['total_applications']) * 100
        else:
            context['approval_rate'] = 0
            
        # Chart Data (Placeholder for actual chart logic)
        context['dept_stats'] = Application.objects.values('department').annotate(
            count=Count('id'),
            total_aid=Sum('annual_income') # Just as an example
        ).order_by('-count')
        
        return context
