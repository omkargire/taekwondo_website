from django.contrib import admin

from webstore.models import User, Category, Product

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Product)
