from django.contrib import admin
from products.models import Product, Hashtag, Comment
# Register your models here.

admin.site.register(Product)
admin.site.register(Hashtag)
admin.site.register(Comment)
