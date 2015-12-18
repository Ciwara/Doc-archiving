#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad

from __future__ import (
    unicode_literals, absolute_import, division, print_function)

import os
import sys
import locale
import gettext
import gettext_windows
sys.path.append(os.path.abspath('../'))

from PyQt4.QtGui import QApplication

from database import setup
from Common.ui.window import FWindow
from Common.cmain import cmain
from Common.ui.cstyle import CSS

from ui.mainwindow import MainWindow
app = QApplication(sys.argv)


def main():

    gettext_windows.setup_env()
    locale.setlocale(locale.LC_ALL, '')
    gettext.install('min_record', localedir='locale')
    window = MainWindow()
    setattr(FWindow, 'window', window)
    window.show()
    # window.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    setup()
    if cmain():
        main()
