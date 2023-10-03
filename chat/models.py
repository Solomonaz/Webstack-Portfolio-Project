from django.db import models
from authentication.models import Account

class Message(models.Model):
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_messages')

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'{self.sender.username} - {self.timestamp}'