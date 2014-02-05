#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import os
from datetime import datetime
from py3compat import implements_to_string

from Common import peewee
from Common.models import Owner, BaseModel
from configuration import Config

FDATE = u"%c"


@implements_to_string
class Category(BaseModel):

    name = peewee.CharField(max_length=30, unique=True)

    def __str__(self):
        return "{name}".format(name=self.name)

    def display_name(self):
        return "{}".format(self.name)

    @classmethod
    def get_or_create(cls, text):
        try:
            catg = cls.objects.get(name=text)
        except cls.DoesNotExist:
            catg = cls.objects.create(name=text)
        return catg


@implements_to_string
class Records(BaseModel):

    date = peewee.DateTimeField(default=datetime.now())
    code = peewee.CharField(max_length=30, unique=True, null=True, blank=True)
    name = peewee.CharField(max_length=50, unique=True)
    doc_file_mane = peewee.CharField(max_length=200, null=True, blank=True)
    doc_file_slug = peewee.CharField(max_length=200, null=True, blank=True, unique=True)
    category = peewee.ForeignKeyField(Category, null=True, blank=True)

    def __str__(self):
        return "{}({})".format(self.name, self.category)

    def display_name(self):
        return u"{}".format(self.name)

    def save(self):
        """ """
        self.code = self.name.replace(" ", "_")
        super(Records, self).save()

    def get_doc_file_mane(self, filename):
        ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
        return "{}{}".format(os.path.join(ROOT_DIR + "Archiving/", Config.des_image_record), filename)

    def rename_doc(self, filename):
        """ Rename file in banc docs  params: name file
            return newname"""

        from Common.ui.util import to_jstimestamp
        destination = Config.des_image_record
        newname = "{}.{}".format(to_jstimestamp(datetime.now()),
                                 filename.split(".")[-1])
        filename = "{}/{}".format(destination, filename)
        newname = "{}/{}".format(destination, newname)
        os.rename(filename, newname)
        return newname

    def import_doc(self, path_filename, filename):
        """ Copy the file, rename file in banc and return new name of the doc
            created folder banc doc if not existe

        """
        import shutil
        destination = Config.des_image_record
        if not os.path.exists(destination):
            os.mkdir(destination)
        dst = u"{}/{}".format(destination, filename)
        shutil.copyfile(path_filename, dst)

        return self.rename_doc(filename)

    def remove_doc(self):
        """ Remove doc and file """
        self.delete_instance()
        try:
            os.remove(self.doc_file_slug)
        except TypeError:
            pass
