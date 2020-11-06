from django.shortcuts import render,redirect
from .models import Product,Order,OrderItem,Shipping_Address
from account.models import Account
from django.http import JsonResponse
import json
import datetime
from .forms import UserRegisterForm
from django.contrib import messages
def index(request):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user
        print(customer)
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {
            'total_cartitem_price':0,
            'total_cartitem':0
        }
        # for i in cart:
        #     try:
        #         order['total_cartitem'] += cart[i]['quantity']
        #         product = Product.objects.get(id=i)
        #         total = product.price*cart[i]['quantity']
        #         order['total_cartitem_price'] += total

        #         item = {
        #             'product':{
        #                 'id':product.id,
        #                 'name':product.name,
        #                 'price':product.price,
        #                 'imageURL':product.imageURL

        #             },
        #             'quantity': cart[i]['quantity'],
        #             'total':total
        #         }
        #         items.append(item)
        #         if product.digital == False:
        #             order['shipping'] == True
        #     except:
        #         pass
    context = {
        'products':products,
        'order':order
    }
    return render(request,'index.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        print(customer)
        order,created = Order.objects.get_or_create(customer=customer,complete=False)
        items = order.orderitem_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {
            'total_cartitem_price':0,
            'total_cartitem':0
        }
        for i in cart:
            try:
                order['total_cartitem'] += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = product.price*cart[i]['quantity']
                order['total_cartitem_price'] += total

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL

                    },
                    'quantity': cart[i]['quantity'],
                    'total':total
                }
                items.append(item)
                if product.digital == False:
                    order['shipping'] == True
            except:
                pass
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
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {
            'total_cartitem_price':0,
            'total_cartitem':0
        }
        for i in cart:
            try:
                order['total_cartitem'] += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = product.price*cart[i]['quantity']
                order['total_cartitem_price'] += total

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL

                    },
                    'quantity': cart[i]['quantity'],
                    'total':total
                }
                items.append(item)
                if product.digital == False:
                    order['shipping'] == True
            except:
                pass

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
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {
            'total_cartitem_price':0,
            'total_cartitem':0
        }
        for i in cart:
            try:
                order['total_cartitem'] += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = product.price*cart[i]['quantity']
                order['total_cartitem_price'] += total

                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'imageURL':product.imageURL

                    },
                    'quantity': cart[i]['quantity'],
                    'total':total
                }
                items.append(item)
                if product.digital == False:
                    order['shipping'] == True
            except:
                pass

        username = data['form']['username']
        email = data['form']['email']
        firstname = data['form']['firstname']
        lastname = data['form']['lastname']

        customer,created = Account.objects.get_or_create(email=email,username=username,firstname=firstname,lastname=lastname)
        customer.save()
        order = Order.objects.create(customer=created,complete=False)
        for item in items:
            product = Product.objects.get(item['product']['id'])
            orderitem = OrderItem.objects.create(
                product=product,
                order = order,
                quantity = item['quantity']
            )
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

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your Account Was Successfully Created')
            return redirect('login')

    else:
        form = UserRegisterForm()
    context = {
        'form':form
    }            
    return render(request,'register.html',context)