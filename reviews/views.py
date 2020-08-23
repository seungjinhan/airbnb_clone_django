from django.contrib import messages
from django.shortcuts import redirect, reverse
from rooms import models as room_models
from . import forms


def create_review(req, room):
    if req.method == "POST":
        form = forms.CreateReviewForm(req.POST)
        room = room_models.Room.objects.get_or_none(pk=room)
        if not room:
            return redirect(reverse("core:home"))

        if form.is_valid():
            review = form.save()
            review.room = room
            review.user = req.user
            review.save()
            messages.success(req, "리뷰 등록 성공")
            return redirect(reverse("rooms:detail", kwargs={'pk': room.pk}))
