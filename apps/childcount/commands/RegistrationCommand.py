#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 coding=utf-8
# maintainer: dgelvin

import re

from django.utils.translation import ugettext as _

from reporters.models import Reporter
from reporters.models import Role
from locations.models import Location

from childcount.commands import CCCommand
from childcount.exceptions import ParseError
from childcount.exceptions import BadValue
from childcount.models import CHW


class RegistrationCommand(CCCommand):
    ENGLISH = 'en'
    ENGLISH_CHW_JOIN = 'chw'
    
    KEYWORDS = {
        '*': [ENGLISH_CHW_JOIN],
    }

    def process(self):
        if self.params[0] == self.ENGLISH_CHW_JOIN:
            reporter_language = self.ENGLISH

        CHW_ROLE_CODE = 'chw'
        if len(self.params) < 3:
            raise ParseError(_(u"Not enough information. Expected: " \
                                "%(keyword)s location names") % \
                                {'keyword': self.params[0]})

        location_code = self.params[1]
        try:
            location = Location.objects.get(code=location_code)
        except Location.DoesNotExist:
            raise BadValue(_(u"Location %(location)s does not exist") % \
                              {'location': location_code})

        if len(self.params) == 3:
            raise ParseError(_(u"You must give more than one name"))
            
        last_name = self.params[2].title()
        first_name = ' '.join(self.params[3:]).title()

        reporter = self.message.persistant_connection.reporter
        if not reporter:
            chw = CHW()
        else:
            try:
                chw = reporter.chw
            except CHW.DoesNotExist:
                chw = CHW(reporter_ptr=reporter)
                chw.save_base(raw=True)


        orig_alias = CHW.generate_alias(first_name, last_name)[:20]
        alias = orig_alias.lower()

        if alias != chw.alias and not re.match(r'%s\d' % alias, chw.alias):            
            n = 1
            while CHW.objects.filter(alias__iexact=alias).count():
                alias = "%s%d" % (orig_alias.lower(), n)
                n += 1
            chw.alias = alias

        chw.first_name = first_name
        chw.last_name = last_name
        chw.language = reporter_language

        try:
            chw_role = Role.objects.get(code=CHW_ROLE_CODE)
        except Role.DoesNotExist:
            #TODO what if there is no chw role?
            pass
        else:
            chw.role = chw_role

        chw.location = location

        # set account active
        # /!\ we use registered_self as active
        chw.registered_self = True

        chw.save()

        # attach the reporter to the current connection
        self.message.persistant_connection.reporter = chw.reporter_ptr
        self.message.persistant_connection.save()

        # inform target
        self.message.respond(
            _(u"Success. You are now registered at %(location)s with " \
               "alias @%(alias)s.") \
               % {'location': location, 'alias': chw.alias})

        '''
        #inform admin
        if message.persistant_connection.reporter != reporter:
            message.respond(_("Success. %(reporter)s is now registered as " \
                            "%(role)s at %(loc)s with alias @%(alias)s.") \
                            % {'reporter': reporter, 'loc': location, \
                            'role': reporter.role, 'alias': reporter.alias})
        '''
        return True
