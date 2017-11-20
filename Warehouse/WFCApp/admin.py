from django.contrib import admin

# Register your models here.
from .models import *

class APIAdmin(admin.ModelAdmin):
	list_display = ('api', 'active')

class SellerAdmin(admin.ModelAdmin):
	list_display = ('user', 'sellerAPI', 'endpoint')
	
class ItemAdmin(admin.ModelAdmin):
	list_display = ('sku', 'sellerAPI', 'quantity', 'status', 'shipping_address')

admin.site.register(API, APIAdmin)
admin.site.register(Status)
admin.site.register(Seller, SellerAdmin)
admin.site.register(Item, ItemAdmin)
