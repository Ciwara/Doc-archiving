#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import os
import time
from datetime import datetime
from py3compat import implements_to_string

from Common import peewee
from Common.models import Owner, BaseModel, Settings, SettingsAdmin

from static import Constants

FDATE = u"%c"


@implements_to_string
class Category(BaseModel):
    class Meta:
        ordering = (('name', 'desc'))

    name = peewee.CharField(max_length=30, unique=True)

    def __str__(self):
        return "{name}".format(name=self.name)

    def display_name(self):
        return "{}".format(self.name)

    @classmethod
    def get_or_create(cls, text):
        try:
            catg = cls.get(name=text)
        except cls.DoesNotExist:
            catg = cls.create(name=text)
        return catg


@implements_to_string
class Records(BaseModel):
    class Meta:
        ordering = (('date', 'desc'))


    date = peewee.DateTimeField(default=datetime.now())
    description = peewee.TextField(null=True, unique=True)
    doc_file_mane = peewee.CharField(max_length=200, null=True)
    doc_file_slug = peewee.CharField(max_length=200, null=True, unique=True)
    category = peewee.ForeignKeyField(Category, null=True)
    trash = peewee.BooleanField(default=False)

    def __str__(self):
        return "{}({})".format(self.description, self.category)

    def display_name(self):
        return u"Categorie: {catg} Nom: {slug}".format(catg=self.category,
                                                       slug=self.doc_file_mane)

    # def get_doc_file_mane(self, filename):
    #     ROOT_DIR = os.path.dirname(os.path.abspath('__file__'))
    #     return os.path.join(os.path.join(ROOT_DIR, Constants.des_image_record), filename)

    def rename_doc(self, filename):
        """ Rename file in banc docs  params: name file
            return newname"""
        destination = Constants.des_image_record
        filename = os.path.join(destination, filename)
        newname = os.path.join(destination, self.slug_mane_doc())
        os.rename(filename, newname)
        return newname

    def slug_mane_doc(self):
        from Common.ui.util import to_jstimestamp
        return "{catg}_{name}.{extension}".format(catg=self.category,
                                      name=to_jstimestamp(datetime.now()),
                                      extension=self.doc_file_mane.split(".")[-1])

    def import_doc(self, path_filename, filename):
        """ Copy the file, rename file in banc and return new name of the doc
            created folder banc doc if not existe
        """
        import shutil
        destination = Constants.des_image_record
        if not os.path.exists(destination):
            os.mkdir(destination)
        dst = os.path.join(destination, filename)
        shutil.copyfile(path_filename, dst)

        return self.rename_doc(filename)

    def remove_doc(self):
        """ Remove doc and file """
        self.delete_instance()
        try:
            os.remove(self.doc_file_slug)
        except TypeError:
            pass

    def istrash(self):
        """ """
        self.trash = True
        self.save()

    def isnottrash(self):
        self.trash = False
        self.save()

    @property
    def os_info(self):
        return os.stat(self.doc_file_slug)

    @property
    def created_date(self):
        return time.ctime(self.os_info.st_ctime)

    @property
    def modification_date(self):
        return time.ctime(self.os_info.st_mtime)

    @property
    def last_date_access(self):
        return time.ctime(self.os_info.st_atime)

    @property
    def get_taille(self):
        """ La taille du document"""
        octe = 1024
        q = octe
        kocte = octe * octe
        unit = "ko"

        taille_oct = float(self.os_info.st_size)
        if kocte < taille_oct:
            unit = "Mo"
            q = kocte

        taille = round(taille_oct / q, 2)
        return "{} {}".format(taille, unit)
