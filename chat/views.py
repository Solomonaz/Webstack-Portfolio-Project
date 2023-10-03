from django.shortcuts import render
from authentication.models import Account
from django.contrib.auth.decorators import login_required
from .models import Message



@login_required
def index(request):
    users = Account.objects.exclude(id=request.user.id)
    message_data = Message.objects.all()
    context = {
        'users':users,
        'message_data':message_data,
    }
    return render(request, 'chat/index.html', context)


