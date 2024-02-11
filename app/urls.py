from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('home/',views.home,name="Home"),
    path('account/signup',views.SignupView.as_view(),name="Home"),
    path('account/signup/electrician',views.ElectricianSignupView.as_view(),name="electrician"),
    path('account/signup/retailer',views.RetailerSignupView.as_view(),name="retailer"),
    path("account/signin/",views.UserSigninView.as_view(), name="signin"),

    path('genqrcode/',views.Qrcodeview.as_view(),name='generatedqr'),
    path('usedqrcode/',views.UsedQrcodeView.as_view(),name='generatedqr'),

    # amanger urlssss /
    path("manager/",views.manager, name="manager"),
    # verify user 
    path("user/<int:pk>",views.showUser , name="user"),
    path("verified/<int:pk>",views.veryfiedUser , name="userverify"),
]