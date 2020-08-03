# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from django_countries import countries
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


class RoomDetail(DetailView):

    """ Room Detail Definition """

    model = models.Room


def search(request):
    city = request.GET.get('city', 'Anywhere')
    city = str.capitalize(city)
    country = request.GET.get('country', 'KR')
    room_type = int(request.GET.get('room_type', 0))
    price = request.GET.get('price', 0)
    guests = request.GET.get('guests', 0)
    bedrooms = request.GET.get('bedrooms', 0)
    beds = request.GET.get('beds', 0)
    baths = request.GET.get('baths', 0)
    instant = request.GET.get('instant', False)
    superhost = request.GET.get('superhost', False)
    s_amenities = request.GET.getlist('amenities')
    s_facilities = request.GET.getlist('facilities')

    print(s_facilities)
    form = {
        'city': city,
        's_country': country,
        's_room_type': room_type,
        'price': price,
        'guests': guests,
        'bedrooms': bedrooms,
        'beds': beds,
        'baths': baths,
        's_amenities': s_amenities,
        's_facilities': s_facilities,
        'instant': instant,
        'superhost': superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        'countries': countries,
        'room_types': room_types,
        'amenities': amenities,
        'facilities': facilities
    }

    return render(
        request,
        'rooms/search.html',
        {
            **form,
            **choices
        })

# def room_detail(request, pk):

#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, 'rooms/detail.html', {'room': room})
#     except models.Room.DoesNotExist:
#         # return redirect(reverse('core:home'))
#         raise Http404()

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
