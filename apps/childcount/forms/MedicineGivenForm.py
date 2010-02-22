#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 coding=utf-8
# maintainer: dgelvin


from django.utils.translation import ugettext as _

from childcount.forms import CCForm
from childcount.models.reports import MedicineGivenReport
from childcount.models import CodedItem
from childcount.exceptions import ParseError


class MedicineGivenForm(CCForm):
    KEYWORDS = {
        'en': ['g'],
    }

    def process(self, patient):
        if len(self.params) < 2:
            raise ParseError(_(u"Not enough info, expected medicine " \
                                "codes"))

        chw = self.message.persistant_connection.reporter.chw

        mgr = MedicineGivenReport(created_by=chw, \
                            patient=patient)

        medicines = dict([(medicine.code.lower(), medicine) \
                             for medicine in \
                             CodedItem.objects.filter(\
                                type=CodedItem.TYPE_MEDICINE)])
        valid = []
        unkown = []
        for d in self.params[1:]:
            obj = medicines.get(d, None)
            if obj is not None:
                valid.append(obj)
            else:
                unkown.append(d)

        if unkown:
            invalid_str = _(u"Unkown medicine code(s): %(codes)s " \
                          "No medicines recorded.") % \
                         {'codes': ', '.join(unkown).upper()}
            raise ParseError(invalid_str)

        if valid:
            signs_string = ', '.join([ds.description for ds in valid])
            self.response = _(u"Medicine given: %(ds)s") % {'ds': signs_string}
            mgr.save()
            for obj in valid:
                mgr.medicines.add(obj)
            mgr.save()
