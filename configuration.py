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

    LOGIN = True
    LOGIN = False

    NAME_MAIN = "main_record.py"
    # ------------------------- Organisation --------------------------#

    APP_NAME = "Gestion d'archivage"
    NAME_ORGA = u"Demo "
    CONTACT_ORGA = u"Bamako-Rep. du Mali"
    TEL_ORGA = u""
    ADRESS_ORGA = u"Bamako djiélibougou"
    BP = u"B.P:177"
    EMAIL_ORGA = u"demo@gmail.com"
