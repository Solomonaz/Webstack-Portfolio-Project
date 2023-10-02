from django.shortcuts import render
from authentication.models import Account

# Create your views here.
def index(request):
    users = Account.objects.all()
    context = {
        'users':users,
    }
    return render(request, 'chat/index.html', context)