from django import forms
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

# Category model
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

# Auction Listing model
class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    image_url = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="listings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, related_name="watchlist", blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_listings")

    def close_auction(self):
        self.active = False
        self.save()

    def __str__(self):
        return self.title

# Bid model
class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.amount} on {self.listing.title} by {self.bidder.username}"

# Comment model
class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} on {self.listing.title}"

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
        labels = {
            'amount': 'Place a bid',
        }