# chat/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json
from authentication.models import User

def index(request):
    return render(request, 'chat/index.html', {})

@login_required
def room(request, room_name):
    users = User.objects.all()
    ctx = dict(
        room_name_json=mark_safe(json.dumps(room_name)),
        users=users
    )
    return render(request, 'chat/room.html', ctx)
