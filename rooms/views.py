from datetime import datetime
from django.shortcuts import render
from . import models


def all_rooms(request):

    all_rooms = models.Room.objects.all()

    return render(request, 'rooms/all_rooms.html', context={
        'rooms': all_rooms})
