from django.shortcuts import render
from authentication.models import Account
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm
from django.db.models import Q


@login_required
def index(request):
    users = Account.objects.exclude(id=request.user.id)
    message_data = Message.objects.all()
    context = {
        'users':users,
        'message_data':message_data,
    }
    return render(request, 'chat/index.html', context)


@login_required
def direct_message_detail(request):
    receiver = get_object_or_404(Account)
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
    ).order_by('timestamp')
    
    print("Before form validation")
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        print(message_form.data)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('index')
    else:
        message_form = MessageForm()

    context = {'receiver': receiver, 'messages': messages, 'message_form': message_form}
    return render(request, 'chat/index.html', context)

