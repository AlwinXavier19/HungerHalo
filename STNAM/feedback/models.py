
from django.db import models
from django.conf import settings
from donor.models import Donation 

class Feedback(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]

    donation = models.ForeignKey(Donation, on_delete=models.CASCADE, related_name='feedbacks')
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_given')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedback_received')
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('donation', 'from_user', 'to_user')  # Prevent duplicates

    def __str__(self):
        return f"{self.from_user} → {self.to_user} ({self.rating}★)"

