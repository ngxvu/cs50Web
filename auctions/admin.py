from django.contrib import admin

# Register your models here.
# auctions/admin.py

from django.contrib import admin
from .models import Listing, Comment, Bid, Category

# Register the Listing model
admin.site.register(Listing)

# Register the Comment model
admin.site.register(Comment)

# Register the Bid model
admin.site.register(Bid)

# Register the Category model
admin.site.register(Category)