#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 coding=utf-8
# maintainer: katembu

'''  Update date of Birth form  '''



from django.utils.translation import ugettext as _
from childcount.utils import DOBProcessor
from childcount.forms import CCForm
from childcount.models import Patient, Encounter
from childcount.exceptions import ParseError, BadValue, Inapplicable

     
#update DoB class
class UpdateDOBForm(CCForm):

    KEYWORDS = {
        'en': ['udob'],
    }
    
    ENCOUNTER_TYPE = Encounter.TYPE_PATIENT

    def process(self, patient):
        
        dob = None
        
        if len(self.params) <  2:
            raise BadValue(_(u"Information not enough healthid | +udob | " \
                                "New DOB"))

        dob, variance = DOBProcessor.from_age_or_dob(lang, self.params[1:])
        
        if dob:
            patient.dob = dob
            days, weeks, months = patient.age_in_days_weeks_months()
            if days < 60 and variance > 1:
                raise BadValue(_(u"You must provide an exact birth date " \
                                      "for children under 2 months"))
            elif months < 24 and variance > 30:
                raise BadValue(_(u"You must provide an exact birth date " \
                                      "or the age in months for children " \
                                      "under two years"))


        if not dob:
            raise ParseError(_(u"Could not understand age or " \
                                    "date_of_birth of %(string)s") % \
                                    {'string': tokens[i + 1]})

        patient.estimated_dob = variance > 1
	
        patient.save
        
        #display response
        self.response = _("You successfuly changed DOB of %(patient)s ")  \
                           % {'patient': patient }

