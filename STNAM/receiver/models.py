from django.db import models
from django.conf import settings
from donor.models import Donation

# receiver/models.py

from django.db import models
from django.conf import settings
from donor.models import Donation

class ReceiverRequest(models.Model):
    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name="receiver_requests")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_donation_requests')
    message = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('requested', 'Requested'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'),
        ],
        default='requested'
    )
    timestamp = models.DateTimeField(auto_now_add=True)  # replaces requested_at

    def __str__(self):
        return f"{self.receiver.username} requested {self.donation.item_name}"


class ReceiverProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username}'s Profile"
