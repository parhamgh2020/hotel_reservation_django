from django.contrib import admin
from .models import Room, Hotel, Reservation

admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(Reservation)