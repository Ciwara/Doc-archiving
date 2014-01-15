#!/usr/bin/env python
# encoding=utf-8
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

from PyQt4.QtGui import QIcon

from common.ui.login import LoginWidget
from common.ui.common import FMainWindow

from model import Owner
from configuration import Config

from ui.menubar import MenuBar
from ui.statusbar import GStatusBar
from ui.records import RecordsViewWidget
from ui.record_consultation import RecordConsultationViewWidget


class MainWindow(FMainWindow):
    def __init__(self):
        FMainWindow.__init__(self)

        self.setWindowIcon(QIcon.fromTheme('logo', QIcon(u"{}archive_.png".format(Config.img_media))))
        self.statusbar = GStatusBar(self)
        self.setStatusBar(self.statusbar)

        if Config.LOGIN:
            self.page = LoginWidget

        # self.page = RecordsViewWidget
        # self.page = RecordConsultationViewWidget

        self.change_context(self.page)


    def exit(self):
        self.logout()
        self.close()

    def active_menu(self):
        self.menubar = MenuBar(self)
        self.setMenuBar(self.menubar)

    def active_menu_ad(self):
        self.menubar = MenuBar(self, admin=True)
        self.setMenuBar(self.menubar)

    def logout(self):
        try:
            self.menubar.setEnabled(False)
        except:
            pass

        for ur in Owner.all():
            ur.islog = False
            ur.save()
