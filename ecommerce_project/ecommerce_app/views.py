from django.shortcuts import render,redirect
from .models import Product,Order,OrderItem,Shipping_Address
from account.models import Account
from django.http import JsonResponse
import json
import datetime
def index(request):
    products = Product.objects.all()
    context = {
        'products':products
    }
    return render(request,'index.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        print(customer)
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    context = {
        'items':items,
        'order':order
    }    


    return render(request,'cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        print(customer)
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    context = {
        'items':items,
        'order':order
    }
    return render(request,'checkout.html',context)   

def updateuseritem(request):
    data = json.loads(request.body)
    productid = data['productid']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productid)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    orderitem,created = OrderItem.objects.get_or_create(product=product,order=order)
    print(orderitem.quantity)
    if action == 'add':
        orderitem.quantity += 1
    elif action == 'remove':
        orderitem.quantity -= 1
    orderitem.save()
    if orderitem.quantity <= 0:
        orderitem.delete()        
    return JsonResponse('item was added',safe=False)

def processorder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.total_cartitem_price):
        order.complete = True
    order.save()

    if order.shipping == True:
       Shipping_Address.objects.create(
           customer=customer,
           order=order,
           address=data['shipping']['address'],
           city=data['shipping']['city'],
           static=data['shipping']['state'],
           zipcode=data['shipping']['zipcode'],
       )     


    return JsonResponse('Payment Complete...',safe=False)