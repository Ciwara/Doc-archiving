#!/usr/bin/env python
# encoding=utf-8
# Autor: Fadiga

from model import Owner

PASS = 'fad 86'


def init_fuxture():

    values = [Owner(username="root", password=PASS,
                    group="superuser", last_login=0),
              Owner(username="anomime", password="anomime",
                   group="admin", last_login=0)]

    for obj in values:
        obj.save()
