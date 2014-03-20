#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from static import Constants


class Config(Constants):
    """ docstring for Config
                            """
    def __init__(self):
        Constants.__init__(self)



    # ------------------------- Organisation --------------------------#

    from model import Settings
    try:
        sttg = Settings.get(id=1)
        LOGIN = sttg.login
        NAME_ORGA = sttg.name_orga #u"Demo "
        TEL_ORGA = sttg.phone #u""
        ADRESS_ORGA = sttg.adress_org #u"Bamako Boulkassoumbougou"
        BP = sttg.bp #u"B.P:177"
        EMAIL_ORGA = sttg.email_org #u"demo@gmail.com"
    except:
        LOGIN = True
        NAME_ORGA = u"Demo "
        TEL_ORGA = u""
        ADRESS_ORGA = u"Bamako Boulkassoumbougou"
        BP = u"B.P:177"
        EMAIL_ORGA =u"demo@gmail.com"
