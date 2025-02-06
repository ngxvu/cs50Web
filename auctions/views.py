from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import ListingForm, BidForm, CommentForm
from .models import Listing, User,Category, Comment
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    active_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user
            listing.current_bid = listing.starting_bid
            listing.save()
            return redirect('index')
    else:
        form = ListingForm()
    return render(request, 'auctions/create_listing.html', {'form': form})


def listing_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    comments = Comment.objects.filter(listing=listing)
    is_owner = request.user == listing.user
    is_watching = request.user in listing.watchlist.all()
    highest_bid = listing.bids.order_by('-amount').first()
    user_won = highest_bid and highest_bid.bidder == request.user and not listing.active

    if request.method == 'POST':
        if 'amount' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                bid = bid_form.save(commit=False)
                if bid.amount >= listing.starting_bid and (highest_bid is None or bid.amount > highest_bid.amount):
                    bid.listing = listing
                    bid.bidder = request.user
                    bid.save()
                    listing.current_bid = bid.amount
                    listing.save()
                    messages.success(request, 'Your bid has been placed successfully.')
                else:
                    messages.error(request, 'Bid must be at least as large as the starting bid and greater than any other bids.')
            else:
                messages.error(request, 'Invalid bid. Please try again.')
        elif 'content' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.listing = listing
                comment.user = request.user
                comment.save()
                messages.success(request, 'Your comment has been added.')
            else:
                messages.error(request, 'There was an error with your comment.')
        elif 'watchlist' in request.POST:
            if is_watching:
                listing.watchlist.remove(request.user)
                messages.success(request, 'Removed from your watchlist.')
            else:
                listing.watchlist.add(request.user)
                messages.success(request, 'Added to your watchlist.')
        elif 'close' in request.POST and is_owner:
            listing.active = False
            if highest_bid:
                listing.winner = highest_bid.bidder
            listing.save()
            messages.success(request, 'The auction has been closed.')

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'comments': comments,
        'bid_form': BidForm(),
        'comment_form': CommentForm(),
        'is_owner': is_owner,
        'is_watching': is_watching,
        'highest_bid': highest_bid,
        'user_won': user_won
    })

@login_required
def watchlist(request):
    user_watchlist = request.user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": user_watchlist
    })

@login_required
def categories(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": all_categories
    })

@login_required
def category_listings(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    listings = Listing.objects.filter(category=category, active=True)
    return render(request, "auctions/category_listing.html", {
        "category": category,
        "listings": listings
    })

@login_required
def closed_listings(request):
    closed_listings = Listing.objects.filter(active=False)
    return render(request, "auctions/closed_listings.html", {
        "listings": closed_listings
    })

@login_required
def remove_from_watchlist(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user.is_authenticated:
        request.user.watchlist.remove(listing)
    return redirect('watchlist')