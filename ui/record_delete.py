#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import os

from PyQt4.QtGui import (QVBoxLayout, QHBoxLayout, QGridLayout, QDialog)
from PyQt4.QtCore import Qt

from Common.ui.common import (F_Widget, F_PageTitle, Button, F_Label)
from Common.ui.util import raise_success


class DeleteRecordsViewWidget(QDialog, F_Widget):
    def __init__(self, record, parent, *args, **kwargs):
        QDialog.__init__(self, parent, *args, **kwargs)
        super(DeleteRecordsViewWidget, self).__init__(parent=parent, *args, **kwargs)
        self.record = record

        self.setWindowTitle(u"Confirmation de le suppression")
        self.title = F_PageTitle(u"Voulez vous vraiment le supprimer?")

        self.title.setAlignment(Qt.AlignHCenter)
        title_hbox = QHBoxLayout()
        title_hbox.addWidget(self.title)
        report_hbox = QGridLayout()

        report_hbox.addWidget(F_Label(u"Le document {} ".format(self.record.display_name())))
        #delete and cancel hbox
        Button_hbox = QHBoxLayout()

        #Delete Button widget.
        delete_but = Button(u"Supprimer")
        Button_hbox.addWidget(delete_but)
        delete_but.clicked.connect(self.delete)
        #Cancel Button widget.
        cancel_but = Button(u"Annuler")
        Button_hbox.addWidget(cancel_but)
        cancel_but.clicked.connect(self.cancel)

        #Create the QVBoxLayout contenaire.
        vbox = QVBoxLayout()
        vbox.addLayout(title_hbox)
        vbox.addLayout(report_hbox)
        vbox.addLayout(Button_hbox)
        self.setLayout(vbox)

    def cancel(self):
        self.close()

    def delete(self):
        from ui.records import RecordsViewWidget
        self.record.remove_doc()
        self.cancel()
        self.change_main_context(RecordsViewWidget)
        raise_success(u"Confirmation", u"<b>le document à été bien supprimé</b>")
