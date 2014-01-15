#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QVBoxLayout, QHBoxLayout, QTableWidgetItem,
                         QIcon, QGridLayout, QSplitter, QFrame,
                         QMenu, QCompleter, QComboBox, QPushButton)
from PyQt4.QtCore import QDate, Qt, QVariant, SIGNAL

from configuration import Config
from model import (Records, Category)
from data_helper import date_datetime

from common.peewee import Q
from common.ui.util import uopen_file, raise_error, is_int
from common.ui.table import F_TableWidget
from common.ui.common import (F_Widget, FormLabel, Button, F_Label,
                              F_BoxTitle, LineEdit)

from ui.record_new import RecordsNewViewWidget


class RecordConsultationViewWidget(F_Widget):

    def __init__(self, record="", parent=0, *args, **kwargs):
        super(RecordConsultationViewWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parentWidget().setWindowTitle(Config.NAME_ORGA +
                                           u"   Consultation des documents")
        self.parent = parent

        vbox = QVBoxLayout(self)
        gridbox = QGridLayout()

        self.liste_categ = Category.all()

        self.combo_categ = QComboBox()
        for index in xrange(0, len(self.liste_categ)):
            op = self.liste_categ[index]
            sentence = u"%(name)s" % {'name': op.name}
            self.combo_categ.addItem(sentence, QVariant(op.id))

        self.combo_categ.connect(self.combo_categ,
                               SIGNAL("currentIndexChanged(int)"),
                               self.finder)

        self.search_field = LineEdit()
        self.search_field.setToolTip("Recherche")
        self.search_field.setMaximumSize(200, self.search_field.maximumSize().height())
        self.search_field.textChanged.connect(self.finder)

        self.vline = QFrame()
        self.vline.setFrameShape(QFrame.VLine)
        self.vline.setFrameShadow(QFrame.Sunken)

        self.table_resultat = ResultatTableWidget(parent=self)
        self.table_info = InfoTableWidget(parent=self)

        self.table_resultat.refresh_("Tous", "")
        gridbox.addWidget(FormLabel(u"Categorie:"), 0, 0)
        gridbox.addWidget(self.combo_categ, 1, 0)
        gridbox.addWidget(self.vline, 0, 2, 2, 1)
        gridbox.addWidget(FormLabel(u"Recherche:"), 0, 1)
        gridbox.addWidget(self.search_field, 1, 1)
        gridbox.setColumnStretch(3, 3)
        gridbox.setRowStretch(2, 2)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setFrameShape(QFrame.StyledPanel)
        splitter_left = QSplitter(Qt.Vertical)
        splitter_left.addWidget(F_BoxTitle(u"Tableau des Documents"))
        splitter_left.addWidget(self.table_resultat)
        splitter_rigth = QSplitter(Qt.Vertical)
        splitter_rigth.addWidget(F_BoxTitle(u"Les détails d'un document stocké"))
        splitter_rigth.addWidget(self.table_info)
        splitter_rigth.resize(100, 1000)
        splitter.addWidget(splitter_left)
        splitter.addWidget(splitter_rigth)

        gridbox.addWidget(splitter, 2, 0, 5, 4)
        vbox.addLayout(gridbox)
        self.setLayout(vbox)

    def finder(self):

        self.current_categ = self.liste_categ[self.combo_categ.currentIndex()]
        categ = unicode(self.current_categ),
        value = unicode(self.search_field.text())
        self.table_resultat.refresh_(categ, value)


class ResultatTableWidget(F_TableWidget):
    """docstring for ResultatTableWidget"""
    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.parent = parent
        self.hheaders = ["i", u"Categorie", u"Documents"]
        self.stretch_columns = [2]
        self.align_map = {1: 'l'}
        self.display_vheaders = True
        # self.ecart = -250
        self.display_fixed = True
        self.refresh_("", "")

    def refresh_(self, categ, value):

        # pw = self.width() / len(self.hheaders)
        pw = 100
        self.setColumnWidth(0, 20)
        self.setColumnWidth(1, pw * 2)
        self.setColumnWidth(2, pw)
        self._reset()
        self.set_data_for(categ, value)
        self.refresh()

    def set_data_for(self, categ, value):
        records = []
        if categ in ["tous", "Tous"]:
            records = Records.all()
        else:
            records = Records.filter(Q(category__name__icontains=categ) |
                                     Q(name__icontains=value))
        try:
            self.data = [("", record.category, record.name) for record in records]
        except AttributeError:
            pass

    def _item_for_data(self, row, column, data, context=None):
        if column == 0:
            return QTableWidgetItem(QIcon(u"{}info.png".format(Config.img_cmedia)), "")
        return super(ResultatTableWidget, self)._item_for_data(row, column,
                                                               data, context)

    def click_item(self, row, column, *args):
        self.choix = Records.filter(name=self.data[row][2]).get()
        self.parent.table_info.refresh_(self.choix.id)


class InfoTableWidget(F_Widget):

    def __init__(self, parent, *args, **kwargs):
        super(F_Widget, self).__init__(parent=parent, *args, **kwargs)

        self.parent = parent

        self.refresh()
        self.name = F_Label(" ")
        self.category = F_Label(" ")
        self.date = F_Label(" ")
        self.chow_doc = Button("")
        self.chow_doc.setIcon(QIcon.fromTheme('document-new',
                                              QIcon(u"{}logo.png".format(Config.img_cmedia))))

        gridbox = QGridLayout()
        gridbox.addWidget(self.name, 1, 0)
        gridbox.addWidget(self.date, 2, 0)
        gridbox.addWidget(self.category, 4, 0, 1, 2)
        gridbox.addWidget(self.chow_doc, 5, 0, 1, 5)

        vbox = QVBoxLayout()
        vbox.addLayout(gridbox)
        self.setLayout(vbox)

    def refresh_(self, idd):

        self.record = Records.get(id=idd)
        self.name.setText(u"<h4>Nom du document: </h4> </br> <h6>{name}</h6>".format(name=self.record.name.title()))
        self.category.setText(u"<h4>Categorie: </h4> </br> <h6>{category}</h6>".format(category=self.record.category.display_name().title()))
        self.date.setText(u"<h4>Date de Création: </h4> </br> <h6>{date}</h6>".format(date=self.record.date.strftime(u"%x")))
        self.chow_doc.clicked.connect(self.print_doc)
        self.chow_doc.setText(u" Afficher ")
        self.chow_doc.setStyleSheet("")
        self.chow_doc.setStyleSheet("background: url({chow_doc}) no-repeat scroll 20px 110px #CCCCCC;"
                                     "width: 55px".format(chow_doc=self.record.doc_file_mane))


    def print_doc(self):
        """ """
        uopen_file(self.record.doc_file_slug)
        return False
