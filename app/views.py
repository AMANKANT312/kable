from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from . serializers import QrcodeModelSerializer,UsedqrcodeModelSerializer,UserModelSerilizer,RetailerModelSerializer,ElectricianModelSerializer,WalletModelSerializer
from .models import Qrcode ,Electrician,Retailer ,Wallet,usedQrcode , ManagerModel
import qrcode
from PIL import Image
from io import BytesIO
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.files.base import ContentFile
import uuid
import json
from django.contrib.auth import authenticate ,login
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

# Create your views here.
def home(request):
    return render(request, "app/home.html")

# managersss viewsss
def manager(request):
    user= "manager@123"
    userid = User.objects.filter(username=user)
    # print(userid)
    for user in userid:
        userid=user.id
    print(userid)
    unverified_electrician = Electrician.objects.filter(is_verified=False)
    unverified_retailer =Retailer.objects.filter(is_verified=False)
    # print(unverified_retailer[0].id)
    unverifieduser = list(unverified_electrician)+ list(unverified_retailer)
    mymanager = ManagerModel.objects.filter(manager=userid)
    print(mymanager)
    customer=[]
    for manager in mymanager:
        # customer_usernames = manager.customer.values_list('username', flat=True)
        # print(list(customer_usernames))
        # customer.append(customer_usernames)
        customers = manager.customer.all()
        customer.append(customers)
    #     for cust in manager:
    #      print(cust)
    print(customer)
    for cust in customer:
        for c in cust:
         print(c.id )
    return render(request,'app/manager.html',{"user":unverifieduser , "customer":customer})

def showUser(request,pk):
    print(id)
    users = User.objects.get(id=pk)
    print(users)
    electrician = Electrician.objects.filter(user=users)
    retailer = Retailer.objects.filter(user=users)
    print(electrician )
    print(retailer)
    data=""
    if electrician:
        data = electrician
    if retailer:
        data = retailer
    print(data)
    return  render(request,'app/showuser.html',{'id':pk , 'data':data})

def check_user_is_staff(user):
    return user.is_staff
def veryfiedUser(request,pk):
    print(id)
    veryfiedby = User.objects.get(username="manager@123")
    print(veryfiedby)
    is_user_staff = check_user_is_staff(veryfiedby)
    if is_user_staff:

        print("he is staff")
        users = User.objects.get(id=pk)
        print(users)
        electrician = Electrician.objects.filter(user=users)
        retailer = Retailer.objects.filter(user=users)
        print(electrician )
        print(retailer)
        data=""
        if electrician:
            for electrician in electrician :
             electrician.is_verified=True
             electrician.save()
             managers= ManagerModel.objects.create(manager=veryfiedby)
             managers.customer.add(users)
             managers.save()
        if retailer:
            for retailer in retailer :
             retailer.is_verified=True
             retailer.save()
            
        print(data)
    return  render(request,'app/showuser.html',{'id':"verified user page" , 'data':data})    

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# @login_required
authentication_classes = [TokenAuthentication]
# permission_classes = [IsAuthenticated]
class UsedQrcodeView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request,*args,**kwargs):
        id = request.POST['id']
        qr = Qrcode.objects.get(id=id)
        data = QrcodeModelSerializer(qr)
        print(data.data)

        user=request.user
        print(user)
        userdata = User.objects.get(username=user)
        # userid=userdata.id
        # print(userid)
        useddata = usedQrcode()
        qrimg =Image.open(qr.createdQr)
        buffer = BytesIO()
        qrimg.save(buffer , format='PNG')
        
        print(userdata)
        useddata.usedBy=userdata
        # if data.data['cashAmount'] >0:
        # cashAmount=0+data.data['cashAmount']
        useddata.cashAmount=data.data['cashAmount']
        useddata.gifts=data.data['gifts']
        useddata.usedQr.save(f'{id}.png', ContentFile(buffer.getvalue()))
        useddata.save()
        print(useddata)


        return Response({"message":"read successfull"})


class Qrcodeview(APIView):
    def post(self,request, *args, **kwargs):
        serializer = QrcodeModelSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            id=uuid.uuid4()
            serializer.validated_data["id"]=id
            qr.add_data(serializer.validated_data)
            qr.make(fit=True)

            # Create a temporary file to save the QR code image
            temp_file = NamedTemporaryFile()
            qr_image = qr.make_image(fill_color="black", back_color="white")
            qr_image.save(temp_file, format="PNG")

            # Create a QRCodeModel instance
            qr_code_instance = Qrcode()

            # Save the QR code image to the model's ImageField
            qr_code_instance.createdQr.save(f"qrcode_{id}.png", File(temp_file))
            qr_code_instance.cashAmount=serializer.data['cashAmount']
            qr_code_instance.gifts=serializer.data['gifts']
            qr_code_instance.id=id
            print(id)
            # Save the model instance to the database
            Qrcodes = qr_code_instance.save()
           
            # print(Qrcodes)
            return Response({"qrcode":"qrcode"})


class SignupView(APIView):
    def post(self, request, *args, **kwargs):
        print(request.data)
        # Get user data from the request
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        # Validate data
        if not username or not password or not email:
            return Response({'error': 'Username, password, and email are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username is already taken
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is already taken.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new user
        user = User.objects.create_user(username=username, password=password, email=email)

        # Create a token for the user
        token = get_tokens_for_user(user)

        # Return success response
        return Response({'token': token}, status=status.HTTP_201_CREATED)
    
    def get(self,request):
        return Response({"message":"get request from signup view"})
  
 
class UserSigninView(APIView):

    def post(self,request , *args ,**kwargs):
            username = request.POST["username"]
            password = request.POST['password']
            user = User.objects.get(username=username)
            print(user)
            electrician = Electrician.objects.get(user=user)
            print(electrician.user)
            if not Electrician:
                retailer = Retailer.objects.get(user=user)
                if not retailer:
                    pass
                else :
                    if (retailer.is_verified):
                        pass
                    else:
                        return Response ({
                            "message":"Your account is under supervision"
                        })
            else:
                if(electrician.is_verified):
                    pass
                else:
                    return Response ({
                            "message":"Your account is under supervision"
                        } )          
            print(user)
            if user is not None:
                user = authenticate(username=username,password=password)
                if user is not None:
                 login(request,user)
                 tokens = get_tokens_for_user(user)
                 data = {
                     "username":username
                     
                 }
                #  usernames=request.user
                 return Response({"user":"sucess","token":tokens,"data":data})
                return Response({'message':'username and password mismatch'})
            return Response ({
                "error":"Username is not found"
              })

class ElectricianSignupView(APIView):
    def post(self,request):
        serializer = UserModelSerilizer(data=request.data)
        if serializer.is_valid():
            Electrician = ElectricianModelSerializer(data=request.data)
            # print(Electrician)
            if Electrician.is_valid():
                user = User.objects.create_user(username=serializer.data['username'],password=serializer.data['password'])
                # user = serializer.save()
                Electrician.save(user=user)
                Wallet.objects.create(user=user)
                # print(serializer)
                print("elelctrician is data is saved ")
                # print(Electrician.data)
                user = {"username":serializer.data["username"]}
                
                return Response({"user":user})
            return Response({"error":Electrician.error_messages})
        return Response({"error":"username and password is not valid"})
        
class RetailerSignupView(APIView):
    def post(self,request):
        serializer = UserModelSerilizer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            # print(request.data)
            Retailer = RetailerModelSerializer(data=request.data)
            print(Retailer)
            if Retailer.is_valid():
                # print(serializer)
                print(Retailer.data)
                return Response({"user":"user"})
            return Response({"error":Retailer.error_messages})
        return Response({"error":"username and password is not valid"})