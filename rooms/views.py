# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from . import models, forms


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


class SearchView(View):

    def get(self, request):

        country = request.GET.get('country')

        if country:
            form = forms.SearchForm(request.GET)
            if form.is_valid():

                city = form.cleaned_data.get('city')
                country = form.cleaned_data.get('country')
                room_type = form.cleaned_data.get('room_type')
                price = form.cleaned_data.get('price')
                guests = form.cleaned_data.get('guests')
                bedrooms = form.cleaned_data.get('bedrooms')
                beds = form.cleaned_data.get('beds')
                baths = form.cleaned_data.get('baths')
                instant_book = form.cleaned_data.get('instant_book')
                superhost = form.cleaned_data.get('superhost')
                amenities = form.cleaned_data.get('amenities')
                facilities = form.cleaned_data.get('facilites')

                filter_args = {}

                if city != 'Anywhere':
                    filter_args['city__startswith'] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args['room_type'] = room_type

                if price is not None:
                    filter_args['price__lte'] = price

                if guests is not None:
                    filter_args['guest__gte'] = guests

                if bedrooms is not None:
                    filter_args['bedrooms__gte'] = bedrooms

                if beds is not None:
                    filter_args['beds__gte'] = beds

                if baths is not None:
                    filter_args['baths__gte'] = baths

                if instant_book is True:
                    filter_args['instant_book'] = True

                if superhost is True:
                    filter_args['host__superhost'] = True

                for a in amenities:
                    filter_args['amenities'] = a

                for a in facilities:
                    filter_args['facilities'] = a

                qs = models.Room.objects.filter(
                    **filter_args).order_by('-created')

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get('page', 1)

                rooms = paginator.get_page(page)

            return render(
                request,
                'rooms/search.html',
                {
                    "form": form, "rooms": rooms
                })
        else:
            form = forms.SearchForm()

        return render(
            request,
            'rooms/search.html',
            {
                "form": form
            })

# def room_detail(request, pk):

#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, 'rooms/detail.html', {'room': room})
#     except models.Room.DoesnotExist:
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
