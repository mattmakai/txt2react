from django.contrib import admin
from .models import Customer, Purchase, PurchaseItem

admin.site.register(Customer)
admin.site.register(Purchase)
admin.site.register(PurchaseItem)
