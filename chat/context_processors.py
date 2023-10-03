from authentication.models import Account
from django.shortcuts import  get_object_or_404
from .models import Message
from .forms import MessageForm
from django.db.models import Q


def message_context(request):
    context = {}

    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Fetch the receiver's account based on some logic (e.g., user_id)
        receiver_id = get_receiver_id_somehow(request)  # Implement this logic

        if receiver_id:
            receiver = get_object_or_404(Account, id=receiver_id)

            messages = Message.objects.filter(
                (Q(sender=request.user, receiver=receiver) | Q(sender=receiver, receiver=request.user))
            ).order_by('timestamp')

            message_form = MessageForm()

            context = {
                'receiver': receiver,
                'messages': messages,
                'message_form': message_form,
            }

    return context

