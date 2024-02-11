import uuid
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Qrcode(models.Model):
    CATEGORY_CHOICES = [
        ('Retailer', 'Retailer'),
        ('Electrician', 'Electrician'),
    ]
    id = models.UUIDField( 
         primary_key = True, 
         default = uuid.uuid4, 
         editable = False)
    cashAmount = models.IntegerField(null=True,blank=True)
    gifts = models.CharField(max_length=8,null=True,blank=True)
    createdQr =models.ImageField(upload_to="media/createdQr/",default=None)
    createdFor= models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='Retailer',
    )
    created_at = models.DateTimeField(auto_now_add=True)

class usedQrcode(models.Model):
    usedBy = models.ForeignKey(User,on_delete = models.PROTECT)
    cashAmount = models.IntegerField(null=True,blank=True)
    gifts = models.CharField(max_length=150)
    usedQr = models.ImageField(upload_to="media/usedQr/" ,default=None)
    createdFor = models.CharField(max_length=20)
    used_at = models.DateTimeField(auto_now_add=True)

class Retailer(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    firm_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)
    dob = models.DateField()
    gst = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    doa_marriage = models.DateField(null=True, blank=True)
    firm_image = models.ImageField(upload_to='media/firm_images/')
    is_verified = models.BooleanField(default=False)
    def __str__(self):
        return self.firm_name
    
class Electrician(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    selfi_image = models.ImageField(upload_to='media/selfi_images/')
    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)
    address = models.TextField()
    adhar = models.CharField(max_length=20, unique=True)
    pan = models.CharField(max_length=20, unique=True)
    dob = models.DateField()
    doa_marriage = models.DateField(null=True, blank=True)
    pincode = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gifts = models.CharField(max_length=120,default="Empty")
    cash_coins = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username}'s Wallet"
    


class ManagerModel(models.Model):
    manager = models.ForeignKey(User,on_delete=models.PROTECT,related_name='manager')
    customer = models.ManyToManyField(User)

