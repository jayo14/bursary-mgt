from django.views.generic import DetailView, ListView, CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, render, redirect
from .models import Application, Review, StatusHistory, ApplicationDocument
from django.urls import reverse

class ApplicationDetailView(LoginRequiredMixin, DetailView):
    model = Application
    template_name = 'applications/detail.html'
    context_object_name = 'application'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = self.object.reviews.all().order_by('-created_at')
        context['history'] = self.object.status_history.all()
        return context

class ApplicationReviewView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Application
    template_name = 'applications/review.html'
    context_object_name = 'application'

    def test_func(self):
        return self.request.user.role in ['ADMIN', 'REVIEWER']

    def post(self, request, *args, **kwargs):
        application = self.get_object()
        decision = request.POST.get('decision')
        comments = request.POST.get('comments')
        
        # Save review
        Review.objects.create(
            application=application,
            reviewer=request.user,
            comments=comments,
            decision=decision
        )
        
        # Update application status
        application.status = decision
        application.save()
        
        # Add to history
        StatusHistory.objects.create(
            application=application,
            status=decision,
            notes=comments,
            changed_by=request.user
        )
        
        if request.htmx:
            return render(request, 'applications/partials/review_success.html', {'application': application})
        return redirect('admin_dashboard')

class ApplicationWizardView(LoginRequiredMixin, TemplateView):
    template_name = 'applications/apply.html'

    def get(self, request, *args, **kwargs):
        # Check if user already has an application for the current session
        current_session = "2024/2025" # This should ideally be dynamic
        if Application.objects.filter(student=request.user, academic_session=current_session).exists():
            return redirect('dashboard')
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        step = request.POST.get('step', '1')
        
        # This is a simplified wizard logic for demonstration.
        # In a real app, you'd handle form validation and partial data saving.
        
        if step == '1':
            # Save step 1 data to session or draft model
            request.session['apply_step1'] = request.POST.dict()
            return render(request, 'applications/partials/step2.html')
        elif step == '2':
            request.session['apply_step2'] = request.POST.dict()
            return render(request, 'applications/partials/step3.html')
        elif step == '3':
            # Handle file uploads
            request.session['apply_step3'] = request.POST.dict()
            return render(request, 'applications/partials/step4.html')
        elif step == 'submit':
            # Create final application
            s1 = request.session.get('apply_step1', {})
            s2 = request.session.get('apply_step2', {})
            
            app = Application.objects.create(
                student=request.user,
                matric_number=s1.get('matric_number'),
                department=s1.get('department'),
                level=s1.get('level'),
                gpa=s1.get('gpa', 0),
                annual_income=s2.get('annual_income', 0),
                household_size=s2.get('household_size', 1),
                reason_for_applying=s2.get('reason_for_applying', ''),
                academic_session="2024/2025"
            )
            
            # Record initial history
            StatusHistory.objects.create(
                application=app,
                status=Application.Status.PENDING,
                notes="Initial application submission",
                changed_by=request.user
            )
            
            return render(request, 'applications/partials/submit_success.html', {'application': app})
        
        return render(request, f'applications/partials/step{step}.html')
