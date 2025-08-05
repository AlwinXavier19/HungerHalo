from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Donation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'donor', 'quantity', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['item_name', 'donor__username']
