from django.contrib.auth.models import User
from django.db import models


class Hotel(models.Model):
    """
    Model representing a hotel.
    """
    name = models.CharField(max_length=30, default="hotel espinas")
    owner = models.CharField(max_length=20, default="parham")
    location = models.CharField(max_length=50)
    state = models.CharField(max_length=50, default="tehran")
    country = models.CharField(max_length=50, default="iran")

    def __str__(self):
        return self.name


class Room(models.Model):
    """
    Model representing a room in a hotel.
    """
    ROOM_STATUS = (
        ("1", "available"),
        ("2", "not available"),
    )

    ROOM_TYPE = (
        ("1", "premium"),
        ("2", "deluxe"),
        ("3", "basic"),
    )

    room_type = models.CharField(max_length=50, choices=ROOM_TYPE)
    capacity = models.IntegerField()
    price = models.IntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    status = models.CharField(choices=ROOM_STATUS, max_length=15)
    room_number = models.IntegerField()

    def __str__(self):
        return f"hotel {self.hotel.name}, room {self.room_number}"


class Reservation(models.Model):
    """
    Model representing a guest's reservation.
    """
    check_in = models.DateField(auto_now=False)
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.guest.username



