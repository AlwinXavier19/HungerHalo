from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from donor.models import Donation

class DeliveryRequest(models.Model):
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE,related_name='delivery_requests')
    
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('pickedup', 'Pickedup'), ('delivered', 'Delivered')],
        default='pending'
    )
    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.volunteer.username} -> {self.donation.item_name} ({self.status})"
