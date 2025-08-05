from django.urls import path
from .views import DonorDashboardView, MakeDonationView,DonationRequestsView,AcceptReceiverRequestView,DonationDeliveryStatusView

urlpatterns = [
    path('dashboard/', DonorDashboardView.as_view(), name='donor-dashboard'),
    path('donate/', MakeDonationView.as_view(), name='make-donation'),
    path('requests/<int:donation_id>/', DonationRequestsView.as_view(), name='donation-requests'),
    path('accept-request/', AcceptReceiverRequestView.as_view(), name='donor-accept-request'),
    path('<int:donation_id>/delivery-status/', DonationDeliveryStatusView.as_view()),
]
