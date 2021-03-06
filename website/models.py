from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True,blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200,null=True)
    email = models.EmailField(max_length=200,null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    CATEGORY = (
        ('Drinks','Drinks'),
        ('Chinese','Chinese'),
        ('Indian','Indian'),
    )
    name = models.CharField(max_length=20,null=False,blank=False)
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=200,null=True,choices=CATEGORY)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    image = models.ImageField(null=True,blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE,blank=True,null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(max_length=200,null=True)
    transaction_id = models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.customer)

    @property
    def total_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def total_price(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.product.price for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product,blank=True,null=True,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,blank=True,null=True,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0,null=True,blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.product)

    @property
    def total(self):
        return self.product.price * self.quantity

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer,blank=True,null=True,on_delete=models.CASCADE)
    order = models.ForeignKey(Order,blank=True,null=True,on_delete=models.CASCADE)
    address = models.CharField(max_length=200,blank=False)
    city = models.CharField(max_length=200,null=False)
    state = models.CharField(max_length=200,null=True)
    zipcode = models.CharField(max_length=200,null=False)
    data_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.address)


