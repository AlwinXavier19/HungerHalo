from django.urls import path
from .views import ReceiverRequestCreateView,ReceiverProfileView, UpdateReceiverProfile,ReceiverRequestStatusView

urlpatterns = [
    path('request/', ReceiverRequestCreateView.as_view(), name='receiver-request'),
    # path('my-requests/', ReceiverRequestListView.as_view(), name='my-requests'),
    path('profile/', ReceiverProfileView.as_view(), name='receiver-profile'),
    path('profile/update/', UpdateReceiverProfile.as_view(), name='update-receiver-profile'),
    path('request-status/', ReceiverRequestStatusView.as_view()),

]

