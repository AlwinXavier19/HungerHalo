from django.urls import path
from .views import (
    AvailableDonationsView,
    DeliveryRequestCreateView,
    DeliveryRequestListView,
    UpdateDeliveryStatusView
)

urlpatterns = [
    path('available-donations/', AvailableDonationsView.as_view(), name='available-donations'),
    path('create/', DeliveryRequestCreateView.as_view(), name='delivery-create'),
    path('my-deliveries/', DeliveryRequestListView.as_view(), name='my-deliveries'),
    path('update-status/<int:pk>/', UpdateDeliveryStatusView.as_view(), name='update-delivery'),
]
