import re

from django.db import models
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class ProductManager(models.Manager):
    def validations(self, data):
        errors = {}
        if len(data['code']) == 0:
            errors['code'] = "Code field cannot be empty"

        if len(data['name']) == 0:
            errors['name'] = "Name field cannot be empty"

        if len(data['price']) == 0:
            errors['price'] = "Price field cannot be empty"
        elif int(data['price']) <= 0:
            errors['price'] = "Price cannot be negative"

        if len(data['stock']) == 0:
            errors['stock'] = "Stock field cannot be empty"
        elif int(data['stock']) < 0:
            errors['stock'] = "Stock cannot be negative"

        return errors


class StoreManager(models.Manager):
    def validations(self, data):
        errors = {}
        if len(data['name']) == 0:
            errors['name'] = "Name field cannot be empty"

        if len(data['email']) == 0:
            errors['email'] = "Email field cannot be empty"
        else:
            email_regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[-]?\w+[.]\w{2,3}$"
            if not re.fullmatch(email_regex, data['email']):
                errors['email'] = "Not valid email"

        if len(data['address']) == 0:
            errors['address'] = "Address field cannot be empty"

        if len(data['city']) == 0:
            errors['city'] = "City field cannot be empty"

        if len(data['country']) == 0:
            errors['country'] = "Country field cannot be empty"

        if len(data['phone']) == 0:
            errors['phone'] = "Phone field cannot be empty"

        return errors


class PersonManager(models.Manager):
    def validations(self, data):
        errors = {}
        if len(data['first_name']) == 0:
            errors['first_name'] = "First name field cannot be empty"

        if len(data['last_name']) == 0:
            errors['last_name'] = "Last name field cannot be empty"

        if len(data['birthday']) == 0:
            errors['birthday'] = "Birthday field cannot be empty"
        else:
            today = timezone.now().date()
            birthday = timezone.make_aware(data['birthday'])

            if today > birthday:
                errors['birthday'] = "Birthday must be in the past"

        if len(data['email']) == 0:
            errors['email'] = "Email field cannot be empty"
        else:
            email_regex = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[-]?\w+[.]\w{2,3}$"
            if not re.fullmatch(email_regex, data['email']):
                errors['email'] = "Not valid email"

        if len(data['address']) == 0:
            errors['address'] = "Address field cannot be empty"

        if len(data['city']) == 0:
            errors['city'] = "City field cannot be empty"

        if len(data['country']) == 0:
            errors['country'] = "Country field cannot be empty"

        if len(data['phone']) == 0:
            errors['phone'] = "Phone field cannot be empty"

        return errors


class OrderManager(models.Manager):
    def validations(self, data):
        errors = {}
        if len(data['purchase_date']) == 0:
            errors['purchase_date'] = "Purchase date field cannot be empty"
        else:
            today = timezone.now().date()
            purchase_date = timezone.make_aware(data['purchase_date'])
            if purchase_date > today:
                errors['purchase_date'] = "Purchase date cannot be in the future"

        if len(data['address']) == 0:
            errors['address'] = "Address field cannot be empty"

        if len(data['city']) == 0:
            errors['city'] = "City field cannot be empty"

        if len(data['country']) == 0:
            errors['country'] = "Country field cannot be empty"

        if len(data['phone']) == 0:
            errors['phone'] = "Phone field cannot be empty"

        return errors


class OrderDetailsManager(models.Manager):
    def validations(self, data):
        errors = {}
        if len(data['quantity']) == 0:
            errors['quantity'] = "Quantity field cannot be empty"
        else:
            if int(data['quantity']) < 0:
                errors['quantity'] = "Quantity cannot be negative"

        return errors


class Product(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200, null=False)
    description = models.CharField(max_length=1000)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    stock = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)
    objects = ProductManager()

    class Meta:
        db_table = 'products'


class Store(models.Model):
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=225)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)
    products = models.ManyToManyField(Product, related_name="stores", db_table="stores_products")
    objects = StoreManager()

    class Meta:
        db_table = 'stores'


class Person(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    birthday = models.DateField()
    email = models.EmailField(max_length=225)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    works_at = models.ForeignKey(Store, null=True, on_delete=models.CASCADE, related_name="employees")
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)
    objects = PersonManager()

    class Meta:
        db_table = 'persons'


class Order(models.Model):
    client = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="orders")
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")
    purchase_date = models.DateTimeField(null=False)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)
    objects = OrderManager()

    class Meta:
        db_table = 'orders'


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="orderDetails")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="orderDetails")
    quantity = models.IntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = AutoDateTimeField(default=timezone.now)
    objects = OrderDetailsManager()

    class Meta:
        db_table = 'orders_details'
