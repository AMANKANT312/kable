from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Retailer,Electrician,Wallet,Qrcode,usedQrcode

class UserModelSerilizer(ModelSerializer):
    class Meta:
        model=User
        fields=['username','password']


class RetailerModelSerializer(ModelSerializer):
    class Meta:
        model=Retailer
        fields=['firm_name', 'owner_name', 'mobile_no', 'dob', 'gst', 'address', 'pincode', 'doa_marriage', 'firm_image', 'is_verified']

class ElectricianModelSerializer(ModelSerializer):
    class Meta:
        model=Electrician
        fields=[  'name', 'mobile_no', 'address', 'adhar', 'pan', 'dob', 'doa_marriage', 'pincode', 'is_verified']

class QrcodeModelSerializer(ModelSerializer):
    class Meta:
        model = Qrcode
        fields=[ 'cashAmount', 'gifts', 'createdFor', 'created_at']

class UsedqrcodeModelSerializer(ModelSerializer):
    class Meta:
        model = usedQrcode
        fields=['usedBy', 'cashAmount', 'gifts', 'usedQr', 'createdFor', 'used_at']

class WalletModelSerializer(ModelSerializer):
    class Meta:
        model = Wallet
        fields=['user', 'gifts', 'cash_coins']