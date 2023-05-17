import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile
from ui_mainwindow import Ui_MainWindow

### importing all modules here to ensure compatibility with Pyinstaller

#modules needed for UI
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

# modules needed for backend
import pandas as pd
import re
import time
from csv import writer
import re
import requests
from bs4 import BeautifulSoup
import locale


#import sys
#sys.path.insert(0, 'Libs and templates\\')

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.submit_button.clicked.connect(self.submit_liason)
        self.ui.exchange_space.addItems(self.getexchangelist())

    def submit_liason(self):
        exchange = self.ui.exchange_space.currentText()
        filepath = self.ui.file_space.toPlainText()
        ticker = self.ui.ticker_space.toPlainText()
        filecheck = self.ui.file_option.isChecked()
        filewrite = self.ui.file_write_option.isChecked()

        #basic error checks

        test=True
        output=''
        if ticker=="" and (filepath=='') and not filecheck:
            output="Enter a ticker, or enter a file path"
            test=False

        if not (filepath=='') and not filecheck and not filewrite:
            output=output+' File path provided,but no action required, please verify'

        #preparing executing code
        if test:
            if filepath=="":
                if not filecheck and not filewrite:
                    import stockscrapingclass
                    self.glibrary=stockscrapingclass.StockScraper()
                    returnval=self.glibrary.quotegetter(targets=exchange+':'+ticker)
                    output=output+"value is "+str(returnval[1])+" at time: "+str(returnval[0])
                else:
                    if filecheck:
                        import stockscrapingclass
                        self.glibrary = stockscrapingclass.StockScraper()
                        self.glibrary.filedata()
                        returnval=self.glibrary.quotegetter()
                        #print(returnval)
                        targets=self.glibrary.targets
                        #sprint(targets)
                        for count,items in enumerate(returnval):
                            if count==0:
                                output=output+" Time of verifying values is "+str(items)
                                continue
                            output=output+" value of target "+str(targets[count-1])+" is "+str(items)
                        if filewrite:
                            self.glibrary.filewriter(returnval)
                    else:
                        pass
                    # todo insert function to write data to file. call the filedata function on the file, append a
                    #  column, write to csv
            else:
                import os
                #from re import search,split
                csvtest=False
                filepath=filepath[:3]+'\\'+filepath[3:]
                #print(filepath)
                try:
                    #csvtest=search('.csv',filepath)==None
                    #print('triggered')
                    path=filepath[::-1]
                    path=path[:3]
                    if path=="vsc":
                        csvtest=True
                    #print(csvtest)
                except:
                    output=output+'enter a valid csv file, without any quotation marks'
                    #self.ui.output_space.setPlainText(output)
                if os.path.exists(filepath) and csvtest:
                    if filecheck:
                        import stockscrapingclass
                        self.glibrary = stockscrapingclass.StockScraper()
                        self.glibrary.filedata(path=filepath)
                        returnval = self.glibrary.quotegetter()
                        # print(returnval)
                        targets = self.glibrary.targets
                        # sprint(targets)
                        for count, items in enumerate(returnval):
                            if count == 0:
                                output = output + " Time of verifying values is " + str(items)
                                continue
                            output = output + " value of target " + str(targets[count - 1]) + " is " + str(items)
                        if filewrite:
                            self.glibrary.filewriter(returnval)
                else:
                    output=output+'replace all \\(backslash) with /(forwardslash)'

        self.ui.output_space.setPlainText(output)

    # method to get the list of exchange names
    def getexchangelist(self):
        import pandas as pd
        exchangedf = pd.read_csv("Exchangelisting.csv")
        exchangelist = exchangedf['Exchange_Code'].tolist()
        return exchangelist


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
