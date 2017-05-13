from django.db import models

class Subscription(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class Contact(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

# Create your models here.
