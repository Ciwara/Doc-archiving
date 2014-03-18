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
from Common.ui.login_manage import LoginManageWidget
from ui.records import RecordsViewWidget
from ui.admin import AdminViewWidget
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

        # logout
        lock = QAction(QIcon("{}login.png".format(Config.img_cmedia)), "Verrouiller", self)
        # lock = QAction(QIcon.fromTheme('security-medium', QIcon('')), "Verrouiller", self)
        lock.setShortcut("Ctrl+l")
        lock.setToolTip(u"Verrouile l'application")
        self.connect(lock, SIGNAL("triggered()"), self.logout)
        file_.addAction(lock)

        # Exit
        exit_ = QAction(QIcon.fromTheme('application-exit', QIcon('')), "Exit", self)
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
        record.setShortcut("Ctrl+R")
        self.connect(record, SIGNAL("triggered()"), self.goto_record)
        goto_.addAction(record)

        # consultation
        consultation = QAction(QIcon("{}archive.png".format(Config.img_media)),
                               u"Consultation", self)
        consultation.setShortcut("Ctrl+C")
        self.connect(consultation, SIGNAL("triggered()"), self.goto_consul)
        goto_.addAction(consultation)

        # Comptes utilisateur
        admin = self.addMenu(u"Admistration")
        gest_user = QAction(QIcon.fromTheme('emblem-system', QIcon('')),
                               u"Gestion d'utilisateur", self)
        gest_user.setShortcut("Ctrl+U")
        self.connect(gest_user, SIGNAL("triggered()"), self.goto_gest_user)
        admin.addAction(gest_user)

        admin_ = QAction(QIcon.fromTheme('emblem-system', QIcon('')),
                               u"Gestion Admistration", self)
        admin_.setShortcut("Ctrl+A")
        self.connect(admin_, SIGNAL("triggered()"), self.goto_admin)
        admin.addAction(admin_)

        licience = QAction(QIcon.fromTheme('emblem-system', QIcon('')),
                               u"Licience", self)
        licience.setShortcut("Ctrl+L")
        self.connect(licience, SIGNAL("triggered()"), self.goto_licience)
        admin.addAction(licience)

        #Menu Aide
        help_ = self.addMenu(u"Aide")
        help_.addAction(QIcon.fromTheme('help-contents', QIcon('')),
                        "Aide", self.goto_help)
        help_.addAction(QIcon.fromTheme('help-about', QIcon('')),
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

    # G. licience
    def goto_licience(self):
        print("licience")
        # self.change_main_context(AdminViewWidget)


    # G user
    def goto_gest_user(self):
        self.change_main_context(LoginManageWidget)

    #Aide
    def goto_help(self):
        self.open_dialog(HTMLEditor, modal=True)

    #About
    def goto_about(self):
        QMessageBox.about(self, u"À propos",
                                u""" <h2>{app_name}  version: {version} </h2>
                                <hr>
                                <h4><i>Logiciel de gestion d'archive.</i></h4>
                                <ul><li></li> <li><b>Developpeur</b>: {autor} </li>
                                <li><b>Adresse: </b>{adress} </li>
                                <li><b>Tel: </b> {phone} </li>
                                <li><b>E-mail: </b> {email} <br/></li>
                                <li>{org_out}</li>
                                <hr>
                                """.format(email=Config.EMAIL_AUT,
                                          app_name=Config.APP_NAME,
                                          adress=Config.ADRESS_AUT,
                                          autor=Config.AUTOR,
                                          version=Config.APP_VERSION,
                                          phone=Config.TEL_AUT,
                                          org_out=Config.ORG_AUT))
