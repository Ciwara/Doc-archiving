#!/usr/bin/env python
# encoding=utf-8
# Autor: Fadiga

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from model import (Records, Owner, Category, Settings, SettingsAdmin, Version)


def setup(drop_tables=False):
    """ create tables if not exist """

    did_create = False

    for model in [Records,
                  Owner,
                  Category,
                  Settings,
                  SettingsAdmin,
                  Version]:
        if drop_tables:
            model.drop_table()
        if not model.table_exists():
            model.create_table()
            did_create = True

    if did_create:
        from Common.fixture import init_fuxture
        print(u"---- Creation de la BD -----")
        init_fuxture()
