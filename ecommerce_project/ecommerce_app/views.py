from django.shortcuts import render,redirect
from .models import Product,Order,OrderItem,Shipping_Address
from account.models import Account

def index(request):
    return render(request,'index.html')

def cart(request):
    return render(request,'cart.html')

def checkout(request):
    return render(request,'checkout.html')        
