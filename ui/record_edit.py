#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import shutil
import os
import sqlite3

from PyQt4.QtCore import Qt
from PyQt4.QtGui import (QIcon, QVBoxLayout, QFileDialog, QDialog, QTextEdit,
                         QIntValidator, QGridLayout, QPushButton, QCompleter)

from configuration import Config
from model import Category

from Common.ui.util import raise_error, raise_success
from Common.ui.common import (F_Widget, F_PageTitle, Button_save, FormLabel,
                              F_Label, LineEdit, IntLineEdit)


class EditRecordsViewWidget(QDialog, F_Widget):
    def __init__(self, record, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)

        self.record = record

        self.description = QTextEdit(self.record.description)
        self.image = os.path.basename(u"{}".format(self.record.doc_file_mane))
        self.path_ = FormLabel(self.image)
        try:
            category = Category.get(name=self.record.category).name
        except:
            category = ""
        self.category = LineEdit(category)

        completion_values =  [catg.name for catg in Category.all()]
        completer = QCompleter(completion_values, parent=self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        self.category.setCompleter(completer)

        gridbox = QGridLayout()
        gridbox.addWidget(F_Label(u"Désignation: "), 0, 0)
        gridbox.addWidget(self.description, 1, 0, 1, 2)
        gridbox.addWidget(F_Label(u"Categorie: "), 2, 0)
        gridbox.addWidget(self.category, 2, 1)
        gridbox.addWidget(F_Label(u"Image: "), 3, 0)
        gridbox.addWidget(self.path_, 3, 1, 1, 4)
        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.edit_prod)
        gridbox.addWidget(butt, 5, 1)

        vbox = QVBoxLayout()
        vbox.addWidget(F_PageTitle(u"Modification des documents"))
        vbox.addLayout(gridbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def edit_prod(self):

        description = unicode(self.description.toPlainText())
        category = unicode(self.category.text())

        self.description.setStyleSheet("")
        if description == "":
            self.description.setStyleSheet("background-color: rgb(255, 235, 235);")
            self.description.setToolTip(u"Ce champs est obligatoire.")
            return False

        record = self.record
        record.description = description
        # prev_image = unicode(self.record.doc_file_mane)

        record.category = Category.get_or_create(category)

        try:
            from ui.records import RecordsViewWidget
            record.save()
            self.change_main_context(RecordsViewWidget)
            self.cancel()
            raise_success(u"Confirmation", u"Le document <b>%s</b> "
                          u"a été mise à jour" % record.description)
        except sqlite3.IntegrityError as e:
            if u"description" in e:
                self.description.setStyleSheet("background-color: rgb(255, 235, 235);")
                self.description.setToolTip(u"Le document {} existe déjà dans la basse "
                                     u"de donnée.".fromat(record.description))
                return False
            if u"code_prod" in e:
                self.code.setStyleSheet("background-color: rgb(255, 235, 235);")
                self.code.setToolTip(u"Le code {} existe déjà dans la basse de "
                                     u"donnée.".format(record.code_prod))
                return False
