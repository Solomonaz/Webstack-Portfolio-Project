from django.shortcuts import render, redirect
from authentication.models import Account
from django.shortcuts import get_object_or_404
from .forms import MessageForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Message, SentMessageInfo

@login_required
def index(request):
    users = Account.objects.exclude(id=request.user.id) 
    message_data = Message.objects.all()
 
    context = {
        'users': users,
        'message_data': message_data,
    }
    
    return render(request, 'chat/index.html', context)

@login_required
def direct_message_detail(request, user_id):
    receiver = get_object_or_404(Account, id=user_id)
    # receiver = request.user
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
    ).order_by('timestamp')

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            new_data = SentMessageInfo(
                sender_content = message_form.content,
                sender_timestamp = Message.timestamp,
                sender_info  = request.user,
                receiver_info = receiver,
            )
            new_data.save()
            return redirect('index/')  
    context = {
        'message_form':message_form,
    }          
    return render(request, 'chat/index.html', context)