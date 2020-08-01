# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.views.generic import ListView
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context['now'] = now
        return context


# def all_rooms(request):

#     page = request.GET.get('page')
#     room_list = models.Room.objects.all()
#     paginator = Paginator(room_list, 10, orphans=5)
#     try:
#         rooms = paginator.get_page(page)
#         return render(request, "rooms/all_rooms.html", {"pages": rooms})
#     except EmptyPage:
#         return redirect

    # page = request.GET.get('page', 1)
    # page = int(page or 1)
    # page_size = 10
    # limit = page_size * page
    # offset = limit - page_size
    # all_rooms = models.Room.objects.all()[offset:limit]
    # page_count = math.ceil(models.Room.objects.count() / page_size)

    # return render(request, 'rooms/all_rooms.html', context={
    #     'rooms': all_rooms, 'page': page, 'page_count': page_count, 'page_range': range(0, page_count)})
