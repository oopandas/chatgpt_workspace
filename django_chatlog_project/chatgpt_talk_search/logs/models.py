from django.db import models

class ChatLogModel(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    summary = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
    

# Create your models here.
