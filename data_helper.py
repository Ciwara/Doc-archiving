#!/usr/bin/env python
# -*- encoding: utf-8
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from datetime import datetime


def date_datetime(dat):
    "reçoit une date return une datetime"
    dat = str(unicode(dat))
    day, month, year = dat.split('/')
    dt = datetime.now()
    return datetime(int(year), int(month), int(day),
                    int(dt.hour), int(dt.minute),
                    int(dt.second), int(dt.microsecond))

def date_end(dat):
    dat = str(unicode(dat))
    day, month, year = dat.split('/')
    return datetime(int(year), int(month), int(day), 23, 59, 59)


def date_on(dat):
    dat = str(unicode(dat))
    day, month, year = dat.split('/')
    return datetime(int(year), int(month), int(day), 0, 0, 0)


def show_date(dat):
    return dat.strftime(u"%A le %d %b %Y a %Hh:%Mmn")
