from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    
    ROLE_CHOICES = (
        ('donor', 'Donor'),
        ('volunteer', 'Volunteer'),
        ('receiver', 'Receiver'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.role})"
