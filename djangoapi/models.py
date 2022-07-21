from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Document(models.Model):
    name = models.CharField(max_length=80)
    path = models.CharField(max_length=200)  
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Result(models.Model):
    result_json = models.TextField()
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
