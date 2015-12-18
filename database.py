#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Fadiga

from __future__ import (unicode_literals, absolute_import,
                        division, print_function)

from Common.models import SettingsAdmin, Version, FileJoin, Organization, Owner
from model import Records, Category


def setup(drop_tables=False):
    """ create tables if not exist """

    did_create = False

    for model in [Records,
                  Owner,
                  Category,
                  Organization,
                  SettingsAdmin,
                  Version,
                  FileJoin]:
        if drop_tables:
            model.drop_table()
        if not model.table_exists():
            model.create_table()
            did_create = True

    if did_create:
        from fixture import fixt_init
        fixt_init().creat_all_or_pass()

setup()
