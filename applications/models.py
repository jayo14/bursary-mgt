from django.db import models
from django.conf import settings

class Application(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        UNDER_REVIEW = 'UNDER_REVIEW', 'Under Review'
        RECOMMENDED = 'RECOMMENDED', 'Recommended'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'
        DISBURSED = 'DISBURSED', 'Disbursed'

    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    # Financial Info
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    household_size = models.PositiveIntegerField()
    reason_for_applying = models.TextField()

    # Session/Duplicate prevention
    academic_session = models.CharField(max_length=20) # e.g., "2023/2024"

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'academic_session'], name='unique_application_per_session')
        ]

    def __str__(self):
        return f"App #{self.id} - {self.student.username} ({self.academic_session})"

class ApplicationDocument(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50) # e.g., "ID", "Transcript", "Income Proof"
    file = models.FileField(upload_to='application_docs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_type} for {self.application}"

class Review(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comments = models.TextField()
    decision = models.CharField(max_length=20, choices=Application.Status.choices)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer} for {self.application}"

class EligibilityReview(models.Model):
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='eligibility_review')
    is_eligible = models.BooleanField(default=False)
    review_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"Eligibility Review for {self.application}"
