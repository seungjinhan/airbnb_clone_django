import math
from datetime import datetime
from django.shortcuts import render
from . import models


def all_rooms(request):

    page = request.GET.get('page', 1)
    page = int(page or 1)
    page_size = 10
    limit = page_size * page
    offset = limit - page_size
    all_rooms = models.Room.objects.all()[offset:limit]
    page_count = math.ceil(models.Room.objects.count() / page_size)

    return render(request, 'rooms/all_rooms.html', context={
        'rooms': all_rooms, 'page': page, 'page_count': page_count, 'page_range': range(0, page_count)})
