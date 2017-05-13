from decimal import Decimal
from results.models import *
from django.db.models import Sum

class Computation(object):
    def __int__(self, total_points, total_units):
        self.total_points = Decimal(total_points)
        self.units = Decimal(total_units)

    def compute_result(self, student, scores, semester, level):

        units = Result.objects.filter(student=student, semester=semester, level=level).aggregate(units = Sum('unit'))['units']





