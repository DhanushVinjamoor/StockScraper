# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main_V0.ui'
##
## Created by: Qt User Interface Compiler version 6.5.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGridLayout,
    QLabel, QLayout, QMainWindow, QMenuBar,
    QPushButton, QSizePolicy, QStatusBar, QTextBrowser,
    QTextEdit, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(446, 504)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(10, 20, 311, 31))
        self.gridLayoutWidget = QWidget(self.centralwidget)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(20, 60, 401, 175))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.ticker_space = QTextEdit(self.gridLayoutWidget)
        self.ticker_space.setObjectName(u"ticker_space")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ticker_space.sizePolicy().hasHeightForWidth())
        self.ticker_space.setSizePolicy(sizePolicy)
        self.ticker_space.setMaximumSize(QSize(200, 50))
        self.ticker_space.setToolTipDuration(-1)

        self.gridLayout.addWidget(self.ticker_space, 1, 1, 1, 1)

        self.label_2 = QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName(u"label_2")

        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)

        self.exchange_space = QComboBox(self.gridLayoutWidget)
        self.exchange_space.setObjectName(u"exchange_space")

        self.gridLayout.addWidget(self.exchange_space, 0, 1, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setMaximumSize(QSize(16777215, 150))

        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.file_space = QTextEdit(self.gridLayoutWidget)
        self.file_space.setObjectName(u"file_space")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.file_space.sizePolicy().hasHeightForWidth())
        self.file_space.setSizePolicy(sizePolicy1)
        self.file_space.setMaximumSize(QSize(200, 50))

        self.gridLayout.addWidget(self.file_space, 2, 1, 1, 1)

        self.verticalLayoutWidget_2 = QWidget(self.centralwidget)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 290, 160, 80))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.file_option = QCheckBox(self.verticalLayoutWidget_2)
        self.file_option.setObjectName(u"file_option")
        self.file_option.setMaximumSize(QSize(200, 50))
        self.file_option.setProperty("setWordWrap", True)

        self.verticalLayout_2.addWidget(self.file_option)

        self.file_write_option = QCheckBox(self.verticalLayoutWidget_2)
        self.file_write_option.setObjectName(u"file_write_option")
        self.file_write_option.setMaximumSize(QSize(200, 50))
        self.file_write_option.setProperty("setWordWrap", True)

        self.verticalLayout_2.addWidget(self.file_write_option)

        self.submit_button = QPushButton(self.centralwidget)
        self.submit_button.setObjectName(u"submit_button")
        self.submit_button.setGeometry(QRect(310, 290, 91, 31))
        self.output_space = QTextBrowser(self.centralwidget)
        self.output_space.setObjectName(u"output_space")
        self.output_space.setGeometry(QRect(10, 390, 421, 61))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 446, 26))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"StockScraper V0.01", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Welcome to StockScraper V0.01", None))
#if QT_CONFIG(tooltip)
        self.ticker_space.setToolTip(QCoreApplication.translate("MainWindow", u"Enter the official ticker label of the share in question", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Choose Exchange name", None))
#if QT_CONFIG(tooltip)
        self.exchange_space.setToolTip(QCoreApplication.translate("MainWindow", u"Refer documentation for list of names", None))
#endif // QT_CONFIG(tooltip)
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Enter ticker", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Enter File location(optional)", None))
        self.file_option.setText(QCoreApplication.translate("MainWindow", u"Scrape from file?", None))
        self.file_write_option.setText(QCoreApplication.translate("MainWindow", u"Write to file?'", None))
        self.submit_button.setText(QCoreApplication.translate("MainWindow", u"Submit?", None))
    # retranslateUi

