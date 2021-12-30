from django.contrib import admin
from .models import *

# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'seller', 'title', 'category', 'description', 'starting_price', 'current_price', 'timestamp', 'active', 'winner')

class WatchListAdmin(admin.ModelAdmin):
    list_display = ('id', 'user')

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist, WatchListAdmin)
