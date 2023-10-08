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

class SentMessageInfo(models.Model):
    sender_content = models.TextField()
    sender_timestamp = models.DateTimeField(auto_now_add=True)
    sender_info = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_message')
    receiver_info = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_message')

    class Meta:
        ordering = ['sender_timestamp']

    def __str__(self):
        return f'{self.sender_info.username} - {self.sender_timestamp}'