#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 coding=utf-8
# maintainer: rgaudin

from django.contrib import admin

from childcount.models import *
from childcount.models.reports import *

admin.site.register(Configuration)
admin.site.register(CHW)
admin.site.register(Clinic)
admin.site.register(Patient)
admin.site.register(PatientRegistrationReport)
admin.site.register(BirthReport)
admin.site.register(DeathReport)
admin.site.register(StillbirthMiscarriageReport)
admin.site.register(FollowUpReport)
admin.site.register(PregnancyReport)
admin.site.register(NeonatalReport)
admin.site.register(UnderOneReport)

admin.site.register(Case)
admin.site.register(Referral)

admin.site.register(Commodity)
admin.site.register(DangerSign)
admin.site.register(DangerSignTranslation)
admin.site.register(HealthReport)

admin.site.register(FeverReport)

admin.site.register(MUACReport)
admin.site.register(ReferralReport)

