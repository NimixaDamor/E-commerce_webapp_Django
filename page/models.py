from django.contrib.auth.models import User
from django.db import models

STATUS_CHOICE=(
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On the way','On the way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)



class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=50,default="")
    image = models.ImageField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    original_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.name


class AddItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.quantity} x {self.name}'

    def total_price(self):
        return self.quantity * self.product.price


class Contact(models.Model):
    username = models.CharField(max_length=50)
    email= models.EmailField()
    subject = models.CharField(max_length=100,default="")
    message = models.CharField(max_length=500,default="")


    def __str__(self):
        return self.username


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.name} - {self.product.name}"


class OrderDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=250,default=1)
    quantity = models.IntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending', choices=STATUS_CHOICE)


class Checkout(models.Model):
    order = models.ForeignKey(OrderDetail, on_delete=models.CASCADE,default=1)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    number = models.IntegerField()
    add1 = models.TextField(max_length=100)
    add2 = models.TextField(max_length=100)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zipcode = models.IntegerField()

    def __str__(self):
        return self.firstname