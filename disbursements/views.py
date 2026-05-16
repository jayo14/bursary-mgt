from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from .models import Disbursement
from applications.models import Application, StatusHistory
from django.utils import timezone

class DisbursementListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Disbursement
    template_name = 'disbursements/list.html'
    context_object_name = 'disbursements'

    def test_func(self):
        return self.request.user.role == 'ADMIN'

    def get_queryset(self):
        return Disbursement.objects.all().order_by('-created_at')

class DisbursementProcessView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Disbursement

    def test_func(self):
        return self.request.user.role == 'ADMIN'

    def post(self, request, *args, **kwargs):
        disbursement = self.get_object_or_404(Disbursement, pk=kwargs['pk'])
        
        # Mark as paid
        disbursement.status = Disbursement.Status.PAID
        disbursement.payment_date = timezone.now()
        disbursement.transaction_reference = f"TRX-{timezone.now().strftime('%Y%m%d')}-{disbursement.id}"
        disbursement.save()
        
        # Update application status
        application = disbursement.application
        application.status = Application.Status.DISBURSED
        application.save()
        
        # Add to history
        StatusHistory.objects.create(
            application=application,
            status=Application.Status.DISBURSED,
            notes=f"Disbursement processed: {disbursement.transaction_reference}",
            changed_by=request.user
        )
        
        if request.htmx:
            return render(request, 'disbursements/partials/disbursement_row.html', {'disbursement': disbursement})
        return redirect('disbursement_list')
