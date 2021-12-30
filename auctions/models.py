from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=300)
    starting_price = models.DecimalField(decimal_places=2, max_digits=9, validators=[MinValueValidator(1)])
    current_price = models.DecimalField(decimal_places=2, max_digits=9, validators=[MinValueValidator(1)], default=0.0)
    img = models.URLField(max_length=200, default="https://res.cloudinary.com/dxeibizaf/image/upload/v1616122320/auctions/27_a1hx87.jpg")
    timestamp = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    # foreign key
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller")
    winner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="winner")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=9)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    writer = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=100)
    timestamp = models.DateTimeField(auto_now=True)

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listing)