from django.db import models

class Document(models.Model):
  name = models.CharField(max_length=60)
  document = models.FileField(upload_to='documents/')
  uploaded_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name