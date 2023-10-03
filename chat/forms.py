from django import forms
from .models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

    content = forms.CharField(
    widget=forms.TextInput(
        attrs={
            "placeholder": "Type your message...",
            "class": "form-control"
        }
    ))