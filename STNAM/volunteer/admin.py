from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import DeliveryRequest

@admin.register(DeliveryRequest)
class DeliveryRequestAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'donation', 'status', 'requested_at')
    list_filter = ('status', 'requested_at')
    search_fields = ('volunteer__username', 'donation__item_name')
