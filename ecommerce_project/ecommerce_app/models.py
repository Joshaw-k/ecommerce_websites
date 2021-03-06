from django.db import models
from account.models import Account

class Product(models.Model):
    name = models.CharField(max_length=40)
    image = models.ImageField(null=True,blank=True)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    digital = models.BooleanField(default=False,null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except :
            url = '' 
        return url 

class Order(models.Model):
    customer = models.ForeignKey(Account,on_delete=models.CASCADE)
    complete = models.BooleanField(default=False,null=True, blank=True)
    transaction_id = models.CharField(max_length=60)
    date_ordered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.id

    @property
    def shipping(self):
        shipping = False
        items = self.orderitem_set.all()
        for item in items:
            if item.product.digital == False:
                shipping = True
        return shipping           

    @property
    def total_cartitem(self):
        items = self.orderitem_set.all()
        total = sum(item.quantity for item in items)  
        return total  
    
    @property
    def total_cartitem_price(self):
        items = self.orderitem_set.all()
        total = sum(item.total for item in items)
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)        
    order = models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        return self.product.price*self.quantity

class Shipping_Address(models.Model):
    customer = models.ForeignKey(Account,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    address = models.CharField(max_length=30,null=False)
    static = models.CharField(max_length=30,null=False)
    city = models.CharField(max_length=30,null=False)
    zipcode = models.CharField(max_length=30,null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address