from django.db import models


class Category(models.Model):
    category_code = models.CharField(max_length=255, unique=True)
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category_code} - {self.category_name}"


class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory_code = models.CharField(max_length=255, unique=True)
    subcategory_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.category.category_code} - {self.subcategory_code} - {self.subcategory_name}"


class Users(models.Model):
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, null=True)
    telegram_id = models.BigIntegerField(unique=True)

    def __str__(self):
        return self.full_name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart Item: {self.product.name} - Quantity: {self.quantity}"


class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by: {self.user.full_name} - Total Amount: {self.price}"
