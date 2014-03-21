#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import (QHBoxLayout, QGridLayout, QGroupBox, QIcon, QTextEdit,
                         QPixmap)

from model import Owner, SettingsAdmin
from Common.check_mac import get_mac
from static import Constants
from configuration import Config
from Common.ui.util import SystemTrayIcon, raise_success, raise_error
from Common.ui.common import (F_Widget, F_PageTitle, FormLabel, PyTextViewer,
                              Button_menu, F_PageTitle, F_Label, Button, LineEdit,
                              Button_save)
from ui.admin import AdminViewWidget
from ui.records import RecordsViewWidget
from ui.record_consultation import RecordConsultationViewWidget


class HomeViewWidget(F_Widget):
    """ Shows the home page  """

    def __init__(self, parent=0, *args, **kwargs):
        super(HomeViewWidget, self).__init__(parent=parent, *args, **kwargs)
        self.parent = parent
        self.root_permission = [u"admin", u"superuser"]

        blanck = 3 * " "
        self.parentWidget().setWindowTitle(Constants.APP_NAME + blanck + "MENU GENERAL")

        self.title = F_PageTitle(u"{} MENU GENERAL {}".format(blanck, blanck))
        self.title.setStyleSheet("background: url({}) no-repeat scroll 20px 50px #fff;"
                                 "border-radius: 14px 14px 4px 4px;"
                                 "font: 15pt 'URW Bookman L';".format(Constants.APP_LOGO))

        self.consultation = Button_menu(_("Consultation"))
        self.consultation.clicked.connect(self.goto_consultation)
        self.consultation.setIcon(QIcon.fromTheme('save', QIcon(u"{}archive.png".format(Constants.img_media))))

        self.add_archiv = Button_menu(_("Archivage"))
        # Affiche sur le commentaire sur le status bar
        # add_archiv.setStatusTip("hhhhhh")
        self.add_archiv.setIcon(QIcon.fromTheme('save', QIcon(u"{}archive_add.png".format(Constants.img_media))))
        self.add_archiv.clicked.connect(self.goto_archi)

        self.admin = Button_menu(_("Administration"))
        self.admin.clicked.connect(self.goto_admin)
        self.admin.setIcon(QIcon.fromTheme('save', QIcon(u"{}admin.png".format(Constants.img_media))))
        self.label = F_Label(self)
        self.label.setStyleSheet("background: url('{}center.png') no-repeat scroll 0 0;"
                                 "height: 50px;width:50px; margin: 0; padding: 0;".format(Constants.img_media))

        # editbox.setColumnStretch(50, 2)

        vbox = QHBoxLayout(self)
        vbox.addWidget(self.title)
        # vbox.addLayout(editbox)
        self.sttg = SettingsAdmin().select().where(SettingsAdmin.id==1).get()
        if self.sttg.can_use():
            self.createMenuMStockGroupBox()
            vbox.addWidget(self.mstockgbox)
        else:
            self.activationGroupBox()
            vbox.addWidget(self.topLeftGroupBoxBtt)
        self.setLayout(vbox)

    def activationGroupBox(self):
        self.topLeftGroupBoxBtt = QGroupBox(self.tr("Nouvelle license"))
        self.setWindowTitle(u"License")
        self.parentWidget().setWindowTitle(u"Activation de la license")

        self.code_field = PyTextViewer(u"""Vous avez besoin du code ci desous
                                           pour l'activation:<hr> <b>{code}</b><hr>
                                           <h4>Contacts:</h4>{contact}"""
                                        .format(code=SettingsAdmin().select().get().clean_mac,
                                         contact=Constants.TEL_AUT))
        self.name_field = LineEdit()
        self.license_field = QTextEdit()
        self.pixmap = QPixmap("")
        self.image = F_Label(self)
        self.image.setPixmap(self.pixmap)

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.add_lience)

        editbox = QGridLayout()
        editbox.addWidget(F_Label(u"Nom: "), 0, 0)
        editbox.addWidget(self.name_field, 0, 1)
        editbox.addWidget(F_Label(u"License: "), 1, 0)
        editbox.addWidget(self.license_field, 1, 1)
        editbox.addWidget(self.code_field, 1, 2)
        editbox.addWidget(self.image, 5, 1)
        editbox.addWidget(butt, 6, 1)

        self.topLeftGroupBoxBtt.setLayout(editbox)
    def createErroMsGroupBox(self):
        self.chow_ms_err = QGroupBox()

        ms_err = PyTextViewer(u"<h3>Vous n'avez pas le droit d'utiliser ce \
                              logiciel sur cette machine, veuillez me contacté \
                              </h3> <ul><li><b>Tel:</b> {phone}</li>\
                              <li><b>{adress}</b></li><li><b>E-mail:</b> \
                              {email}</li></ul></br></br>{mac} \
                              ".format(email=Constants.EMAIL_AUT,
                                       adress=Constants.ADRESS_AUT,
                                       phone=Constants.TEL_AUT,
                                       mac=get_mac().replace(":", ":")))

        gridbox = QGridLayout()
        gridbox.addWidget(F_PageTitle(_("Erreur de permission")), 0, 2)
        gridbox.addWidget(ms_err, 1, 2)
        self.chow_ms_err.setLayout(gridbox)

    def createMenuMStockGroupBox(self):
        self.mstockgbox = QGroupBox()

        editbox = QGridLayout()
        editbox.addWidget(self.consultation, 0, 1, 1, 1)
        editbox.addWidget(self.label, 1, 1, 1, 1)
        editbox.addWidget(self.admin, 1, 2, 1, 1)
        editbox.addWidget(self.add_archiv, 0, 3, 1, 1)
        self.mstockgbox.setLayout(editbox)


    def check_log(self, page, permiss=None):

        if not Config.LOGIN:
            self.parent.active_menu_ad()
            SystemTrayIcon((_(u"Avertissement de Securité"),
                            "({}) Il est vivement souhaité de securiser son "
                            "application".format(Constants.APP_NAME)), parent=self)
        else:
            try:
                owner = Owner.get(islog=True)
                self.parent.active_menu_ad()
            except:
                return False
        self.change_main_context(page)

    def goto_consultation(self):
        self.check_log(RecordConsultationViewWidget)

    def goto_archi(self):
        self.check_log(RecordsViewWidget)

    def goto_admin(self):
        self.check_log(AdminViewWidget)

    def check_license(self, license):

        self.flog = False

        if (SettingsAdmin().is_valide_mac(license)):
            self.pixmap = QPixmap(u"{}accept.png".format(Constants.img_cmedia))
            self.image.setToolTip("License correct")
            self.flog = True
        else:
            self.pixmap = QPixmap(u"{}decline.png".format(Constants.img_cmedia))
            self.image.setToolTip("License incorrect")
        self.image.setPixmap(self.pixmap)

    def add_lience(self):
        """ add User """
        name = unicode(self.name_field.text()).strip()
        license = unicode(self.license_field.toPlainText())
        self.check_license(license)

        if self.flog:
            sttg = self.sttg
            sttg.user = name
            sttg.license = license
            sttg.save()
            raise_success(u"Confirmation",
                          u"""La license (<b>{}</b>) à éte bien enregistré pour cette
                           machine.\n
                           Elle doit être bien gardé""".format(license))
            self.goto_archi()
