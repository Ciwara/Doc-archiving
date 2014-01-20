#!/usr/bin/env python
# -*- coding: utf8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu
# maintainer: Fad
from __future__ import (unicode_literals, absolute_import, division, print_function)

import os, sys; sys.path.append(os.path.abspath('../'))
import locale
import gettext, gettext_windows

from PyQt4.QtGui import QApplication

from Common.ui.window import F_Window
from ui.mainwindow import MainWindow

from database import setup


def main():
    """  """
    setup()

    gettext_windows.setup_env()
    locale.setlocale(locale.LC_ALL, '')
    gettext.install('main_mb', localedir='locale', unicode=True)

    app = QApplication(sys.argv)
    window = MainWindow()
    setattr(F_Window, 'window', window)
    # window.show()
    window.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
