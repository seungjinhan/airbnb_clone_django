import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from . import models
from rooms import models as room_models


class CreateError(Exception):
    pass


def create(req, room, year, month, day):
    try:
        date_obj = datetime.datetime(year=year, month=month, day=day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        raise CreateError()

    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(req, '방예약을 할 수 없음')
        return redirect(reverse('core:home'))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=req.user,
            room=room,
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={'pk': reservation.pk}))


class ReservationDetailView(View):

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (reservation.guest != self.request.user and reservation.room.host != self.request.user):
            raise Http404()

        return render(self.request, "reservations/detail.html", {"reservation": reservation})


def edit_reservation(req, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (reservation.guest != req.user and reservation.room.host != req.user):
        raise Http404()

    if verb == 'confirm':
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == 'cancel':
        reservation.status = models.Reservation.STATUS_CANCELED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(req, "예약 업데이트 완료")
    return redirect(reverse('reservations:detail', kwargs={'pk': reservation.pk}))
