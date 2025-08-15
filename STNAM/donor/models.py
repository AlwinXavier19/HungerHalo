from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Donation(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="donations_received")
    volunteer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="volunteered_donations")

    item_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    quantity = models.PositiveIntegerField()
    pickup_address = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('picked', 'Picked Up'),
            ('delivery_assigned', 'Delivery Assigned'),
            ('cancelled', 'Cancelled'),
            ('accepted_by_receiver', 'Accepted by Receiver'),
            ('delivered', 'Delivered'),
        ],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} by {self.donor.username}"
# receiver/models.py


