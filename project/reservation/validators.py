from django.db.models import Q
from rest_framework.exceptions import ValidationError

from .models import Reservation


def validate_reservation_date(check_in, check_out, room):
    """
    Checks if a reservation with the given check-in and check-out dates for a room already exists.
    Raises a ValidationError if a reservation with the same date range is found.
    Also calls validate_arrangement_date to check if the given dates are valid.

    Parameters:
    - check_in (datetime.date): the check-in date of the reservation
    - check_out (datetime.date): the check-out date of the reservation
    - room (int): the ID of the room for the reservation
    """
    validate_arrangement_date(check_in, check_out)
    cond1 = Q(check_in__range=[check_in, check_out],
              check_out__range=[check_in, check_out],
              room=room)
    cond2 = Q(check_in__lte=check_in,
              check_out__gte=check_out,
              room=room)
    cond3 = Q(check_in__range=[check_in, check_out],
              room=room)
    cond4 = Q(check_out__range=[check_in, check_out],
              room=room)
    reservation = Reservation.objects.filter(cond1 | cond2 | cond3 | cond4)
    if reservation:
        raise ValidationError('A reservation with this date range already reserved.')


def validate_arrangement_date(start, end):
    """
    Checks if the given arrangement dates are valid.
    Raises a ValidationError if the end date is less than or equal to the start date.

    Parameters:
    - start (datetime.date): the start date of the arrangement
    - end (datetime.date): the end date of the arrangement
    """
    if end <= start:
        raise ValidationError('check-out/start_date must be greater than check-in/end_date')
