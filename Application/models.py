from django.db import models


# Create your models here.

class MerchantInfo(models.Model):
    name = models.CharField(max_length=160, blank=True, null=True)
    city_name = models.CharField(max_length=160, blank=True, null=True)
    seller_score = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Name: {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=160, blank=True, null=True)
    brand = models.CharField(max_length=160, blank=True, null=True)
    category = models.CharField(max_length=160, blank=True, null=True)

    def __str__(self):
        return f"Name: {self.name}"


class ProductSeller(models.Model):
    merchant = models.ForeignKey(MerchantInfo, models.CASCADE, blank=True, null=True)
    product = models.ForeignKey(Product, models.CASCADE, blank=True, null=True)
    selling_price = models.CharField(max_length=160, blank=True, null=True)
    discounted_price = models.CharField(max_length=160, blank=True, null=True)

    def __str__(self):
        return f"Merchant: {self.merchant} - Product: {self.product} - Selling Price: {self.selling_price}"