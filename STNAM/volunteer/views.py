from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import DeliveryRequest
from .serializers import DeliveryRequestSerializer
from .permissions import IsVolunteer

# View for Volunteer to List Available Donations
from donor.models import Donation
from donor.serializers import DonationSerializer

class AvailableDonationsView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated, IsVolunteer]

    def get_queryset(self):
        # Only show donations accepted by receiver and not yet picked up
        return Donation.objects.filter(
            status='accepted_by_receiver'
        ).exclude(
            delivery_requests__status='delivered'
        )



# Volunteer creates delivery request
class DeliveryRequestCreateView(generics.CreateAPIView):
    queryset = DeliveryRequest.objects.all()
    serializer_class = DeliveryRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsVolunteer]

    def perform_create(self, serializer):
        serializer.save(volunteer=self.request.user)


# Volunteer views their delivery requests
class DeliveryRequestListView(generics.ListAPIView):
    serializer_class = DeliveryRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsVolunteer]

    def get_queryset(self):
        return DeliveryRequest.objects.filter(volunteer=self.request.user)


class UpdateDeliveryStatusView(generics.UpdateAPIView):
    serializer_class = DeliveryRequestSerializer
    permission_classes = [permissions.IsAuthenticated, IsVolunteer]
    queryset = DeliveryRequest.objects.all()
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.status == 'delivered':
            donation = instance.donation
            donation.status = 'delivered'
            donation.save()

