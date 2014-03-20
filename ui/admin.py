#!usr/bin/env python
# -*- coding: utf8 -*-
#maintainer: Fad

from datetime import date
from PyQt4.QtGui import (QVBoxLayout, QTableWidgetItem, QGridLayout, QIcon,
                         QCheckBox, QMessageBox, QTextEdit)
from PyQt4.QtCore import QDate, Qt, SIGNAL

from model import Owner, Records, Settings
from Common.tabpane import tabbox
from Common.ui.util import (is_int, formatted_number, date_on, show_date,
                            date_end, raise_success, raise_error)
from Common.ui.table import F_TableWidget
from Common.ui.common import (F_Widget, F_PageTitle, LineEdit, Button,
                              Button_save, FormLabel, IntLineEdit)

from static import Constants


class AdminViewWidget(F_Widget):

    def __init__(self, parent=0, *args, **kwargs):
        super(AdminViewWidget, self).__init__(parent=parent, *args, **kwargs)

        self.parent = parent

        self.parentWidget().setWindowTitle(Constants.APP_NAME + u"    ADMINISTRATION")


        editbox = QGridLayout()
        table_config = QVBoxLayout()
        self.table_config = SettingsTableWidget(parent=self)
        table_config.addLayout(editbox)
        table_config.addWidget(self.table_config)

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
                            (table_config, _(u"Gestion de l'organisation")),
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
        # self.table_config.refresh_()


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

class SettingsTableWidget(F_Widget):

    def __init__(self, parent, *args, **kwargs):
        super(F_Widget, self).__init__(parent=parent, *args, **kwargs)

        self.organisation = Settings.get(id=1)
        self.parent = parent
        vbox = QVBoxLayout()
        # vbox.addWidget(F_PageTitle(u"Utilisateur: %s " % self.organisation.name_orga))

        self.checked = QCheckBox("Active")
        if self.organisation.login:
            self.checked.setCheckState(Qt.Checked)
        # self.setCellWidget(nb_rows, 2, checked)
        self.checked.setToolTip(u"""Cocher si vous voulez pour deactive
                                le login continue à utiliser le systeme""")
        self.name_orga = LineEdit(self.organisation.name_orga)
        self.phone = IntLineEdit(str(self.organisation.phone))
        self.bp = LineEdit(self.organisation.bp)
        self.adress_org = QTextEdit(self.organisation.adress_org)
        self.email_org = LineEdit(self.organisation.email_org)

        formbox = QVBoxLayout()
        editbox = QGridLayout()

        editbox.addWidget(FormLabel(u"Non de l'organisation: "), 0, 0)
        editbox.addWidget(self.name_orga, 0, 1)
        editbox.addWidget(FormLabel(u"Activer le login"), 1, 0)
        editbox.addWidget(self.checked, 1, 1)
        editbox.addWidget(FormLabel(u"B.P:"), 2, 0)
        editbox.addWidget(self.bp, 2, 1)
        editbox.addWidget(FormLabel(u"Tel:"), 3, 0)
        editbox.addWidget(self.phone, 3, 1)
        editbox.addWidget(FormLabel(u"E-mail:"), 4, 0)
        editbox.addWidget(self.email_org, 4, 1)
        editbox.addWidget(FormLabel(u"Adresse complete:"), 5, 0)
        editbox.addWidget(self.adress_org, 5, 1)

        butt = Button_save(u"Enregistrer")
        butt.clicked.connect(self.save_edit)
        editbox.addWidget(butt, 8, 1)

        formbox.addLayout(editbox)
        vbox.addLayout(formbox)
        self.setLayout(vbox)

    def save_edit(self):
        ''' add operation '''
        name_orga = unicode(self.name_orga.text())
        bp = unicode(self.bp.text())
        email_org = unicode(self.email_org.text())
        phone = unicode(self.phone.text())
        adress_org = unicode(self.adress_org.toPlainText())

        if self.check_impty:
            login = False
            org = Settings.get(id=self.organisation.id)
            if self.checked.checkState() == Qt.Checked:
                login = True
            org.phone = phone
            org.name_orga = name_orga
            org.email_org = email_org
            org.bp = bp
            org.adress_org = adress_org
            org.login = login
            org.save()
            raise_success(u"Confirmation", u"Le Compte %s "
                          u"a été mise à jour" % org.name_orga)
        else:
            raise_error(u"Error", u"Mot de passe pas correct")

    def check_impty(self):
        flag = True
        for field in [self.name_orga, self.phone, self.bp, self.email_org]:
            if field.text() == "":
                flag = False
        return flag


