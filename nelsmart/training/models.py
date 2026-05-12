from django.db import models

class Application(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(blank=True)

    def __str__(self):
        return self.name

class TrainingContent(models.Model):
    title = models.CharField(max_length=100)
    video = models.FileField(upload_to='training_videos/')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title