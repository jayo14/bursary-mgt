from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
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

    def is_student(self):
        return self.role == self.Role.STUDENT

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
