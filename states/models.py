from django.db import models
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Country')
        verbose_name_plural = _(u'Countries')

    def __str__(self):
        return self.name


class State(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('name',)
        verbose_name = _(u'Nigerian State')
        verbose_name_plural = _(u'Nigerian States')

    def __str__(self):
        return self.name


class LGA(models.Model):
    state = models.ForeignKey(State, related_name='local_govt_areas')
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ('state', 'name',)
        verbose_name = _(u'Nigerian Local Government Area')
        verbose_name_plural = _(u'Nigerian Local Government Areas')

    def __str__(self):
        return self.name
