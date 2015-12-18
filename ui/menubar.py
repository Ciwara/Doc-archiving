#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (
    unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QMessageBox, QMenuBar, QIcon, QAction, QPixmap)
from PyQt4.QtCore import SIGNAL, SLOT

from configuration import Config
from Common.exports import export_database_as_file, export_backup, import_backup
from Common.ui.common import FWidget
from Common.ui.cmenubar import FMenuBar
from Common.ui.license_view import LicenseViewWidget
from ui.records import RecordsViewWidget
# from ui.admin import AdminViewWidget
from ui.consultation import ConsultationViewWidget
from ui.help import HTMLEditor


class MenuBar(FMenuBar, FWidget):

    def __init__(self, parent=None, admin=False, *args, **kwargs):
        FMenuBar.__init__(self, parent=parent, *args, **kwargs)

        self.setWindowIcon(QIcon(QPixmap("{}".format(Config.APP_LOGO))))
        self.parent = parent

        menu = [{"name": u"Gestion des documents", "icon": 'archive_add', "admin":
                 False, "shortcut": "Ctrl+T", "goto": RecordsViewWidget},
                {"name": u"Consultation", "admin": True,  "icon": 'archive',
                    "shortcut": "Ctrl+P", "goto": ConsultationViewWidget},
                ]

        # Menu aller à
        goto_ = self.addMenu(u"&Aller a")

        for m in menu:
            el_menu = QAction(
                QIcon("{}{}.png".format(Config.img_media, m.get('icon'))), m.get('name'), self)
            el_menu.setShortcut(m.get("shortcut"))
            self.connect(
                el_menu, SIGNAL("triggered()"), lambda m=m: self.goto(m.get('goto')))
            goto_.addSeparator()
            goto_.addAction(el_menu)

        # Menu Aide
        help_ = self.addMenu(u"Aide")
        help_.addAction(QIcon.fromTheme('help-contents', QIcon('')),
                        "Aide", self.goto_help)
        help_.addAction(QIcon.fromTheme('help-about', QIcon('')),
                        u"À propos", self.goto_about)

    # Aide
    def goto_help(self):
        self.open_dialog(HTMLEditor, modal=True)
