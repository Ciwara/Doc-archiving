#!usr/bin/env python
# -*- coding: utf8 -*-
#maintainer: Fad

from datetime import date
from PyQt4.QtGui import (QVBoxLayout, QTableWidgetItem, QGridLayout, QIcon)
from PyQt4.QtCore import QDate, Qt

from model import Owner
from common.peewee import Q
from common.tabpane import tabbox
from common.ui.util import is_int, formatted_number, date_on, show_date, date_end
from common.ui.table import F_TableWidget
from common.ui.edit_owner import EditOwnerViewWidget
from common.ui.common import (F_Widget, F_PageTitle, LineEdit, FormatDate,
                              Button, Button_export, FormLabel)

from configuration import Config


class AdminViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(AdminViewWidget, self).__init__(parent=parent, *args, **kwargs)

        self.parent = parent

        self.parentWidget().setWindowTitle(Config.APP_NAME + u"    ADMINISTRATION")

        butt = Button(_(u"Créer un nouvel utilisateur"))
        butt.setIcon(QIcon.fromTheme('save',
                                     QIcon(u"{}user_add.png".format(Config.img_cmedia))))
        butt.clicked.connect(self.goto_new_user)

        editbox = QGridLayout()
        editbox.addWidget(butt, 0, 1, 1, 1)
        table_owner = QVBoxLayout()
        self.title_owner = F_PageTitle(_(u"Les utilisateurs "))
        self.table_owner = OwnerTableWidget(parent=self)
        table_owner.addWidget(self.title_owner)
        table_owner.addLayout(editbox)
        table_owner.addWidget(self.table_owner)

        tab_widget = tabbox((table_owner, _(u"Gestion d'utilisateurs")))

        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)

    def goto_new_user(self):
        from common.ui.new_user import NewUserViewWidget

        self.parent.open_dialog(NewUserViewWidget, modal=True, go_home=False)
        # self.table_owner.refresh_()


class OwnerTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):
        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)
        self.hheaders = [_(u"Nom d'utilisateur"), _(u"Tel."), _(u"Groupe"),
                         _(u"Status"), _(u"Modification")]
        self.parent = parent
        self.set_data_for()
        self.stretch_columns = [0]
        self.align_map = {0: 'l'}
        self.max_rows = 100
        self.refresh()

    def refresh_(self):
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [(ow.username, ow.phone, ow.group, ow.isactive, "")
                     for ow in Owner.filter(Q(group="user") | Q(group="admin"))]

    def _item_for_data(self, row, column, data, context=None):

        if column == 3 and self.data[row][3] == 1:
            return QTableWidgetItem(QIcon(u"{}accept.png".format(Config.img_cmedia)), u"")
        if column == 3 and self.data[row][3] == 0:
            return QTableWidgetItem(QIcon(u"{}decline.png".format(Config.img_cmedia)), u"")
        if column == 4:
            return QTableWidgetItem(QIcon(u"{}edit_user.png".format(Config.img_cmedia)), u"")

        return super(OwnerTableWidget, self)._item_for_data(row, column,
                                                            data, context)

    def click_item(self, row, column, *args):
        column_ = 4
        if column == column_:
            self.parent.open_dialog(EditOwnerViewWidget, modal=True,
                                    owner=Owner.get(username=self.data[row][0]))
        else:
            return
