'''
Registrations
'''

from datetime import timedelta

from django.db import connection

from django.utils.translation import ugettext as _

from indicator import Indicator
from indicator import QuerySetType

from childcount.models import Patient

class Total(Indicator):
    type_in     = QuerySetType(Patient)
    type_out    = int

    slug        = "total"
    short_name  = _("Registered")
    long_name   = _("Total number registered patients")

    @classmethod
    def _value(cls, period, data_in):
        return data_in\
            .filter(created_on__lte=period.end)\
            .count()

class UnderFive(Indicator):
    type_in     = QuerySetType(Patient)
    type_out    = int

    slug        = "under_five"
    short_name  = _("U5")
    long_name   = _("Total number registered under-fives")

    @classmethod
    def _value(cls, period, data_in):
        return data_in\
            .filter(created_on__lte=period.end)\
            .under_five(period.start, period.end)\
            .count()

class UnderSixMonths(Indicator):
    type_in     = QuerySetType(Patient)
    type_out    = int

    slug        = "under_six_months"
    short_name  = _("U6m")
    long_name   = _("Total number registered kids under 6 months of age")

    @classmethod
    def _value(cls, period, data_in):
        return data_in\
            .filter(created_on__lte=period.end)\
            .under_six_months(period.start, period.end)\
            .count()

class Household(Indicator):
    type_in     = QuerySetType(Patient)
    type_out    = int

    slug        = "household"
    short_name  = _("HH")
    long_name   = _("Total number registered households")

    @classmethod
    def _value(cls, period, data_in):
        return data_in\
            .filter(created_on__lte=period.end)\
            .household(period.start, period.end)\
            .count()

class Mobile(Indicator):
    type_in     = QuerySetType(Patient)
    type_out    = int

    slug        = "mobile"
    short_name  = _("Mobile")
    long_name   = _("Total registered patients with mobile number")

    @classmethod
    def _value(cls, period, data_in):
        return data_in\
            .filter(created_on__lte=period.end)\
            .alive(period.start, period.end)\
            .exclude(mobile='')\
            .exclude(mobile__isnull=True)\
            .count()
