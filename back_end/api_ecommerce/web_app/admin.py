from django.contrib import admin
from .models import User, Item, OrderItem, Order, Address, Payment, Coupon, Refund
# Register your models here.

class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'category', 'label']
    prepopulated_fields = {'slug': ('title',)}

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']
    
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'item', 'quantity']
    
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'street_address', 'apartment_address', 'country', 'zip', 'address_type', 'default']
    list_filter = ['default', 'address_type', 'country']
    search_fields = ['user', 'street_address', 'apartment_address', 'zip']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'timestamp']
    
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount']
    
class RefundAdmin(admin.ModelAdmin):
    list_display = ['order', 'reason', 'accepted', 'email']
    
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'full_name', 'phone', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'full_name', 'phone']
    list_filter = ['is_staff', 'is_active']

admin.site.register(User, UserAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Order , OrderAdmin)
admin.site.register(Address , AddressAdmin)
admin.site.register(Payment , PaymentAdmin)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Refund , RefundAdmin)
