import datetime
from django import template
from reservations import models as reservation_model
register = template.Library()


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return False
    try:
        date = datetime.datetime(
            year=day.year, month=day.month, day=day.number)
        reservation_model.BookedDay.objects.get(
            day=date, reservation__room=room)
        print(date)
        print(room)

        return True
    except reservation_model.BookedDay.DoesNotExist:
        return False
