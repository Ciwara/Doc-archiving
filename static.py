#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# Maintainer: Fad

from Common.cstatic import CConstants


class Constants(CConstants):

    def __init__(self):
        CConstants.__init__(self)

        self.license.update({'00:24:54:f2:6d:9f': 'fad'})

    ORG_AUT = u"Copyright © 2014"
    des_image_record = "ARMOIRE"
    # Si la persionne n'a pas tout payé
    credit = 17
    tolerance = 50
    nb_warning = 5
    # ------------------------- Application --------------------------#
    APP_NAME = "Gestion d'archive"
    APP_VERSION = u"1.0"
    APP_DATE = u"01/2014"
    img_media = "media/images/"

    APP_LOGO = "{}logo.jpg".format(img_media)
    APP_LOGO_ICO = "{}logo.ico".format(img_media)
