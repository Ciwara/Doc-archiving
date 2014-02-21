#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QMessageBox, QMenuBar, QIcon, QAction, QPixmap)
from PyQt4.QtCore import SIGNAL, SLOT

from configuration import Config
from Common.exports import export_database_as_file
from Common.ui.common import F_Widget
from ui.records import RecordsViewWidget
from ui.record_consultation import RecordConsultationViewWidget
from ui.help import HTMLEditor


class MenuBar(QMenuBar, F_Widget):

    def __init__(self, parent=None, admin=False, *args, **kwargs):
        QMenuBar.__init__(self, parent=parent, *args, **kwargs)

        self.setWindowIcon(QIcon(QPixmap("{}".format(Config.APP_LOGO_ICO))))

        self.parent = parent
        #Menu File
        file_ = self.addMenu(u"&Fichier")
        # Export
        export = file_.addMenu(u"&Export des données")
        export.addAction(u"base de données de sauvegarde", self.goto_export_db)

        file_.addAction(u"Déconnexion", self.logout)

        # Exit
        exit_ = QAction(QIcon("{}exit.png".format(Config.img_cmedia)), "Exit", self)
        exit_.setShortcut("Ctrl+Q")
        exit_.setToolTip(u"Quiter l'application")
        self.connect(exit_, SIGNAL("triggered()"), self.parentWidget(),
                                          SLOT("close()"))
        file_.addAction(exit_)

        # Menu aller à
        goto_ = self.addMenu(u"&Aller a")

        # Records
        record = QAction(QIcon("{}archive_add.png".format(Config.img_media)),
                         u"Gestion des documents", self)
        record.setShortcut("Ctrl+P")
        self.connect(record, SIGNAL("triggered()"), self.goto_record)
        goto_.addAction(record)

        # consultation
        consultation = QAction(QIcon("{}archive.png".format(Config.img_media)),
                               u"Consultation", self)
        consultation.setShortcut("Ctrl+C")
        self.connect(consultation, SIGNAL("triggered()"), self.goto_consul)
        goto_.addAction(consultation)

        #Menu Aide
        help_ = self.addMenu(u"Aide")
        help_.addAction(QIcon("{}help.png".format(Config.img_cmedia)),
                        "Aide", self.goto_help)
        help_.addAction(QIcon("{}info.png".format(Config.img_cmedia)),
                              u"À propos", self.goto_about)

    def logout(self):
        from Common.ui.login import LoginWidget
        # self.parent.restart()
        # self.change_main_context(LoginWidget)
        LoginWidget().exec_()

    def goto_record(self):
        self.change_main_context(RecordsViewWidget)

    def goto_consul(self):
        self.change_main_context(RecordConsultationViewWidget)

    #Export the database.
    def goto_export_db(self):
        export_database_as_file()

    # Admin
    def goto_admin(self):
        self.change_main_context(AdminViewWidget)

    #Aide
    def goto_help(self):
        self.open_dialog(HTMLEditor, modal=True)

    #About
    def goto_about(self):
        QMessageBox.about(self,
                                u"À propos",
                                u"<h2>%(app_name)s version: %(version)s</h2>"
                                u"<i>Logiciel de gestion d'archive.</i>"
                                u"<ul><li></li>"
                                u"<li><b>Developpeur</b>: %(autor)s</li>"
                                u"<li><b>Adresse: </b>%(adress)s</li>"
                                u"<li><b>Tel: </b> %(phone)s</li>"
                                u"<li><b>E-mail: </b> %(email)s<br/></li>"
                                u"<li>© 2012 Kalanène s.à.r.l</li>"
                                % {"email": Config.EMAIL_AUT,
                                  "app_name": Config.APP_NAME,
                                  "adress": Config.ADRESS_AUT,
                                  "autor": Config.AUTOR,
                                  "version": Config.APP_VERSION,
                                  "phone": Config.TEL_AUT})
