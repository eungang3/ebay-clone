from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import template
from django.contrib.auth.decorators import login_required

from django.forms import ModelForm
from .models import User, Listing, Bid, Comment, Category, Watchlist


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings" : listings
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

# create a listing
def create(request):
    class ListingForm(ModelForm):
        class Meta:
            model = Listing
            fields = ['title', 'category', 'starting_price', 'description', 'img']
        
        def __init__(self, *args, **kwargs):
            super(ListingForm, self).__init__(*args, **kwargs)
            for fname, f in self.fields.items():
                f.widget.attrs['class'] = 'form-control'
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.current_price = listing.starting_price
            listing.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

    return render(request, "auctions/create.html", {
        "form" : ListingForm()
    })

  
class WatchlistForm(ModelForm):
    class Meta:
        model = Watchlist
        fields = ['listing']
    def __init__(self, *args, **kwargs):
            super(WatchlistForm, self).__init__(*args, **kwargs)
            self.fields['listing'].label = ""
    
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    return render(request, "auctions/listing.html", {
        "listing" : listing, 
        "form" : WatchlistForm(data={'listing': listing_id})
    })

@login_required
def watchlist(request):
    if request.method == "POST":
        form = WatchlistForm(request.POST)
        if form.is_valid():
            watchlist = form.save(commit=False)
            watchlist.user = request.user
            watchlist.save()
            print("success")
        return HttpResponseRedirect("watchlist")

    return render(request, "auctions/watchlist.html", {
        "listings" : Watchlist.objects.filter(user=request.user)
    }) 

def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html", {
        "categories" : categories
    })

def category_listing(request, category_id):
    category = Category.objects.get(pk=category_id)
    listings = Listing.objects.filter(category=category_id)
    
    return render(request, "auctions/category_listing.html", {
        "category_name" : category.name,
        "listings" : listings
    })

