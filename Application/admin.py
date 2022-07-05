from django.contrib import admin
from Application.models import MerchantInfo, Product, ProductSeller

# Register your models here.

admin.site.register(MerchantInfo)
admin.site.register(Product)
admin.site.register(ProductSeller)