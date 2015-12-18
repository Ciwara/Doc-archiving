#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# Maintainer: Fad

import os

from Common.cstatic import CConstants

ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))


class Constants(CConstants):

    def __init__(self):
        CConstants.__init__(self)

        self.license.update({'00:24:54:f2:6d:9f': 'fad'})

    ORG_AUT = u"Copyright © 2014"
    ARMOIRE = "ARMOIRE"
    des_image_record = os.path.join(ROOT_DIR, ARMOIRE)
    # Si la persionne n'a pas tout payé
    credit = 17
    tolerance = 50
    nb_warning = 5

    # ------------------------- Application --------------------------#

    DOC_SUPPORT = "*.ppt *.txt *.odt *.ods *.xls *.xlsx *.gif *.png \
                   *.jpg *.doc *.docx *.pdf *.jpeg"

    NAME_MAIN = "main_record.py"
    APP_NAME = "Gestion d'archive"
    APP_VERSION = u"1.0.2"
    APP_DATE = u"01/2014"
    img_media = os.path.join(os.path.join(ROOT_DIR, "static"), "images/")
    APP_LOGO =  os.path.join(img_media, "logo.png")
    APP_LOGO_ICO = os.path.join(img_media, "logo.ico")
