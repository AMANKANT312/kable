# admin.py
from django.contrib import admin
from .models import Qrcode, usedQrcode, Retailer, Electrician, Wallet ,ManagerModel

@admin.register(Qrcode)
class QrcodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'cashAmount', 'gifts', 'createdQr', 'createdFor', 'created_at']

@admin.register(usedQrcode)
class UsedQrcodeAdmin(admin.ModelAdmin):
    list_display = ['usedBy', 'cashAmount', 'gifts', 'usedQr', 'createdFor', 'used_at']

@admin.register(Retailer)
class RetailerAdmin(admin.ModelAdmin):
    list_display = ['user', 'firm_name', 'owner_name', 'mobile_no', 'dob', 'gst', 'address', 'pincode', 'doa_marriage', 'firm_image', 'is_verified']

@admin.register(Electrician)
class ElectricianAdmin(admin.ModelAdmin):
    list_display = ['user', 'selfi_image', 'name', 'mobile_no', 'address', 'adhar', 'pan', 'dob', 'doa_marriage', 'pincode', 'is_verified']

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ['user', 'gifts', 'cash_coins']

@admin.register(ManagerModel)
class ManagerModelAdmin(admin.ModelAdmin):
    list_display = ['manager']