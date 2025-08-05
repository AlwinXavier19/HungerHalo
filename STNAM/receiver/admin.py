from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import ReceiverRequest

@admin.register(ReceiverRequest)
class ReceiverRequestAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'donation', 'status', 'timestamp')
    list_filter = ('status', 'timestamp')
    search_fields = ('receiver__email', 'donation__item_name')
from django.contrib import admin
from .models import ReceiverProfile

@admin.register(ReceiverProfile)
class ReceiverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'phone')
    search_fields = ('user__email', 'phone', 'address')
