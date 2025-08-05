from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Donation
from receiver.models import ReceiverRequest
from .serializers import DonationSerializer,ReceiverRequestSerializer

class DonorDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        donations = Donation.objects.filter(donor=request.user).order_by('-created_at')
        serializer = DonationSerializer(donations, many=True)
        return Response(serializer.data)

class MakeDonationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DonationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(donor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.permissions import BasePermission
class DonationRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, donation_id):
        donation = Donation.objects.filter(id=donation_id, donor=request.user).first()
        if not donation:
            return Response({"error": "Donation not found or not owned by you"}, status=403)

        requests = donation.receiver_requests.all()
        serializer = ReceiverRequestSerializer(requests, many=True)
        return Response(serializer.data)
# donor/views.py
class AcceptReceiverRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_id = request.data.get("request_id")
        try:
            receiver_request = ReceiverRequest.objects.get(id=request_id)
        except ReceiverRequest.DoesNotExist:
            return Response({"error": "Request not found"}, status=404)

        if receiver_request.donation.donor != request.user:
            return Response({"error": "Not authorized to accept this request"}, status=403)

        # Accept the selected receiver request
        receiver_request.status = "accepted"
        receiver_request.save()

        # Update donation status
        donation = receiver_request.donation
        donation.status = "accepted_by_receiver"
        donation.save()

        return Response({"message": "Receiver request accepted successfully."})

class DonationDeliveryStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, donation_id):
        donation = Donation.objects.filter(id=donation_id, donor=request.user).first()
        if not donation:
            return Response({"error": "Donation not found or not yours"}, status=403)

        deliveries = donation.delivery_requests.all()
        from volunteer.serializers import DeliveryRequestSerializer  # make sure import is correct
        serializer = DeliveryRequestSerializer(deliveries, many=True)
        return Response(serializer.data)
