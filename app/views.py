from django.shortcuts import render, redirect
from django.db import transaction
from .models import Room
import haikunator


def index(request):
    return render(request, 'index.html', {})


def new_room(request):
    new_room = None

    while not new_room:
        with transaction.atomic():
            label = haikunator.haikunate()
            if Room.objects.filter(label=label).exists():
                continue
            new_room = Room.objects.create(label=label)

    return redirect(room, label=label)


def room(request, label):
    room, created = Room.objects.get_or_create(label=label)
    messages = reversed(room.messages.order_by('-timestamp')[:50])

    return render(request, "room.html", {'room': room, 'messages': messages, })
