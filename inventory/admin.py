from django.contrib import admin
from .models import Item, ProductIdCount, Sale

admin.site.register(Item)
admin.site.register(ProductIdCount)
admin.site.register(Sale)