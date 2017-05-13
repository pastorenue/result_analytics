from django.db import models
from django.contrib.auth.models import User

class Session(models.Model):
    title = models.CharField(max_length=10, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    analyzer = models.ManyToManyField(User)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _(u'Workspace')
        verbose_name_plural = _(u'Workspaces')
    
    def __str__(self):
        return self.title

class Workspace(models.Model):
    session = models.ManyToManyField(Session)
    date_modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _(u'Workspace')
        verbose_name_plural = _(u'Workspaces')
        
    def __str__(self):
        return self.id


# Create your models here.
