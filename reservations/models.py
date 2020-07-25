from django.db import models
from core import models as core_models
from django.utils import timezone

class Reservation(core_models.TimeStampedModel):

    """ Reservation Model """

    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELED = "canceled"

    STATUS_CHOICES = (
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELED, "Canceled"),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, max_length=12, default=STATUS_PENDING
    )
    check_in = models.DateField()
    check_out = models.DateField()
    guest = models.ForeignKey("users.User",related_name='reservations',on_delete=models.CASCADE)
    room = models.ForeignKey("rooms.Room",related_name='reservations',on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.room.name} - {self.check_in}"

    def in_progress(self):
        now = timezone.now().date()
        return now > self.check_in and now < self.check_out
    
    in_progress.boolean = True

    def is_finished(self):
        now = timezone.now().date()
        return now > self.check_out 

    is_finished.boolean = True     