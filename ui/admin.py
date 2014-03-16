#!usr/bin/env python
# -*- coding: utf8 -*-
#maintainer: Fad

from datetime import date
from PyQt4.QtGui import (QVBoxLayout, QTableWidgetItem, QGridLayout, QIcon,
                         QCheckBox, QMessageBox)
from PyQt4.QtCore import QDate, Qt, SIGNAL

from model import Owner, Records
from Common.tabpane import tabbox
from Common.ui.util import is_int, formatted_number, date_on, show_date, date_end
from Common.ui.table import F_TableWidget
from Common.ui.edit_owner import EditOwnerViewWidget
from Common.ui.common import (F_Widget, F_PageTitle, LineEdit, FormatDate,
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

        self.bttrestor = Button(_(u"Restaurer"))
        self.bttrestor.clicked.connect(self.restorseleted)
        self.bttrestor.setEnabled(False)
        self.bttempty = Button(_(u"Vide"))
        self.bttempty.clicked.connect(self.deletedseleted)
        self.bttempty.setEnabled(False)
        # Grid
        gridbox = QGridLayout()
        gridbox.addWidget(self.bttrestor, 0 , 1)
        gridbox.addWidget(self.bttempty, 0 , 2)
        table_trash = QVBoxLayout()

        self.table_trash = TrashTableWidget(parent=self)
        table_trash.addLayout(gridbox)
        table_trash.addWidget(self.table_trash)

        tab_widget = tabbox((table_trash, _(u"Corbeille")),
                            (table_owner, _(u"Gestion d'utilisateurs")),
                            )

        vbox = QVBoxLayout()
        vbox.addWidget(tab_widget)
        self.setLayout(vbox)

    def enablebtt(self):
        self.bttrestor.setEnabled(True)
        self.bttempty.setEnabled(True)

    def restorseleted(self):
        for doc in self.table_trash.getSelectTableItems():
            doc.isnottrash()
            self.table_trash.refresh_()

    def deletedseleted(self):
        reply = QMessageBox.question(self, 'Suppression definitive',
                self.tr("Voulez vous vraiment le supprimer? "),
                 QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for doc in self.table_trash.getSelectTableItems():
                doc.remove_doc()
                self.table_trash.refresh_()

    def goto_new_user(self):
        from Common.ui.new_user import NewUserViewWidget

        self.parent.open_dialog(NewUserViewWidget, modal=True, go_home=False)
        # self.table_owner.refresh_()


class TrashTableWidget(F_TableWidget):

    def __init__(self, parent, *args, **kwargs):

        F_TableWidget.__init__(self, parent=parent, *args, **kwargs)

        self.parent = parent

        self.hheaders = [_(u"Selection"),_(u"Date"), _(u"categorie"), _(u"Description")]
        self.stretch_columns = [0]
        self.align_map = {0: 'l'}
        self.ecart = -5
        self.display_vheaders = False
        self.display_fixed = True

        self.refresh_()

    def refresh_(self):
        self._reset()
        self.set_data_for()
        self.refresh()

    def set_data_for(self):
        self.data = [("", record.date, record.category, record.description)
                     for record in Records.select().where(Records.trash==True).order_by(Records.category.asc())]

    def getSelectTableItems(self):
        n = self.rowCount()
        ldata = []
        for i in range(n):
            item = self.cellWidget(i, 0)
            if not item:
                pass
            elif item.checkState() == Qt.Checked:
                ldata.append(Records.filter(description=str(self.item(i, 3).text())).get())
        return ldata

    def _item_for_data(self, row, column, data, context=None):
        if column == 0:
            # create check box as our editor.
            editor = QCheckBox()
            if data == 2:
                editor.setCheckState(2)
            self.connect(editor, SIGNAL('stateChanged(int)'), self.parent.enablebtt)
            return editor
        return super(TrashTableWidget, self)._item_for_data(row, column,
                                                             data, context)

    def click_item(self, row, column, *args):
        pass

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
                     for ow in Owner.select().where((Owner.group=="user") | (Owner.group=="admin"))]

    def _item_for_data(self, row, column, data, context=None):

        if column == 3 and self.data[row][3] == 1:
            return QTableWidgetItem(QIcon.fromTheme('user-available', QIcon('')), u"")
        if column == 3 and self.data[row][3] == 0:
            return QTableWidgetItem(QIcon.fromTheme('user-offline', QIcon('')), u"")
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
