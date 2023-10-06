from django.shortcuts import render, redirect
from authentication.models import Account
from django.shortcuts import get_object_or_404
from .forms import MessageForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def index(request):
    users = Account.objects.exclude(id=request.user.id)
    
    message_data = Message.objects.all()
    
    receiver = request.user
    
    messages = Message.objects.filter(
        (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
    ).order_by('timestamp')
    
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            message = message_form.save(commit=False)
            message.sender = request.user
            message.receiver = receiver
            message.save()
            return redirect('chat:index')  # Adjust the namespace and URL name if needed
    
    else:
        message_form = MessageForm()
    
    context = {
        'users': users,
        'message_data': message_data,
        'receiver': receiver,
        'messages': messages,
        'message_form': message_form
    }
    
    return render(request, 'chat/index.html', context)


def chat_room(request, room_name):
    return render(request, 'chat.html', {'room_name': room_name})




# @login_required
# def direct_message_detail(request, user_id):
#     receiver = get_object_or_404(Account, id=user_id)
#     messages = Message.objects.filter(
#         (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
#     ).order_by('timestamp')

#     if request.method == 'POST':
#         message_form = MessageForm(request.POST)
#         print(message_form)
#         if message_form.is_valid():
#             message = message_form.save(commit=False)
#             message.sender = request.user
#             message.receiver = receiver
#             message.save()
#             return redirect('index', user_id=user_id)
#     else:
#         message_form = MessageForm()

#     context = {'receiver': receiver, 'messages': messages, 'message_form': message_form}
#     return render(request, 'chat/index.html', context)