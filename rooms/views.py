# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.generic import ListView, DetailView, View, UpdateView, CreateView, FormView
from django.http import Http404
from django.urls import reverse
from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from users import mixins as user_mixins
from . import models, forms


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
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


class EditRoomView(user_mixins.LoggedInOnlyView, UpdateView):

    model = models.Room
    template_name = "rooms/room_edit.html"
    fields = (
        "name",
        "description",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
    )

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


class RoomPhotosView(user_mixins.LoggedInOnlyView, DetailView):

    model = models.Room
    template_name = "rooms/room_photos.html"

    def get_object(self, queryset=None):
        room = super().get_object(queryset=queryset)
        if room.host.pk != self.request.user.pk:
            raise Http404()
        return room


@login_required
def delete_photo(req, room_pk, photo_pk):

    user = req.user
    try:
        room = models.Room.objects.get(pk=room_pk)
        if room.host.pk != user.pk:
            messages.error(req, "삭제할 수 없음!!")
        else:
            models.Photo.objects.get(pk=photo_pk).delete()
            messages.success(req, "사진삭제성공")
        return redirect(reverse("rooms:photos", kwargs={"pk": room_pk}))
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))


class EditPhotoView(user_mixins.LoggedInOnlyView, SuccessMessageMixin, UpdateView):

    model = models.Photo
    template_name = 'rooms/photo_edit.html'
    pk_url_kwarg = 'photo_pk'
    success_message = '사진 업로드됨'

    fields = (
        "caption",
    )

    def get_success_url(self):
        room_pk = self.kwargs.get("room_pk")
        return reverse("rooms:photos", kwargs={"pk": room_pk})


class AddPhotoView(user_mixins.LoggedInOnlyView, FormView):

    model = models.Photo
    template_name = "rooms/photo_create.html"
    form_class = forms.CreatePhotoForm
    fields = (
        "caption",
        "file",
    )

    def form_valid(self, form):
        pk = self.kwargs.get('pk')
        form.save(pk)
        messages.success(self.request, "사진이 업로드됨")
        return redirect(reverse("rooms:photos", kwargs={"pk": pk}))

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
