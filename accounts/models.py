from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        REVIEWER = 'REVIEWER', 'Reviewer'
        STUDENT = 'STUDENT', 'Student'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STUDENT
    )
    phone_number = models.CharField(max_length=15, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def is_admin(self):
        return self.role == self.Role.ADMIN

    def is_reviewer(self):
        return self.role == self.Role.REVIEWER

    def is_student(self):
        return self.role == self.Role.STUDENT

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    matric_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    level = models.CharField(max_length=20)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.matric_number})"
