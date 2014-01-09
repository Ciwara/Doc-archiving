#!/usr/bin/env python
# encoding=utf-8
# Autor: Fadiga

from model import Owner

PASS = 'fad 86'


def init_fuxture():

    values = [Owner(username="root", password=PASS, phone="76433890",
                    group="superuser", last_login=0)]

    for obj in values:
        obj.save()
