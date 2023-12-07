import sys, PyQt5, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUi # Import all PyQt5 Widgets

##print('basename:    ', os.path.basename(__file__))
##print('dirname:     ', os.path.dirname(__file__))

def tryexcept(func):
    def x(*args, **kwargs):
        try: return(func(*args, **kwargs))
        except Exception as e: print(func.__name__,":", "'{}'".format(e))
    return x

        
class MainWindow(QMainWindow): # Create a 'mainWindow' class that inherits from the PyQt equivalent
    def __init__(self, *args): 
        super().__init__(*args) # Pass the window arguments to the Qt Class - we don't need it
        self.setWindowFlags(
        QtCore.Qt.Window |
        QtCore.Qt.CustomizeWindowHint |
        QtCore.Qt.WindowTitleHint |
        QtCore.Qt.WindowCloseButtonHint |
        QtCore.Qt.WindowStaysOnTopHint
        )

        self.commander = None
        
        self.center()
        self.StartPage()
        self.show()
##        self.activateWindow()
##        self.test()
        


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().topLeft()
        qr.moveTopLeft(cp)
        self.move(qr.topLeft())

        
    @tryexcept
    def StartPage(self):
        loadUi("gui.ui", self)
        self.setTableData(self.tableWidget,len(rLabels),3,rLabels,["DATE"])#,"LONGASSNAME","LONGASSNAME2"])
        
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)

    @tryexcept
    def setTableData(self,table,rCount,cCount,rLabels,cLabels):
        table.setRowCount(rCount)
        table.setColumnCount(cCount)
        for i in range(rCount):
            table.setItem(i,0,QTableWidgetItem(rLabels[i]))
##            table.item(i,1).setTextAlignment(AlignCenter)
##            table.item(i,2).setTextAlignment(AlignCenter)
        table.setHorizontalHeaderLabels(cLabels)
##        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.resizeColumnsToContents()

    def updateHeaders(self,headers):
        print("applying:",headers)
        try:
            self.tableWidget.setHorizontalHeaderLabels(headers)
        except Exception as e: print("headers",e)

    def updateSum(self):
##        print("hereaaaaaaa")
        headers, homeColumn, awayColumn = self.getTableData()
##        print(homeColumn,awayColumn)
        homeTotal = float(0.00)
        awayTotal = float(0.00)
        for x in homeColumn:
            try:
                homeTotal += float(x)
            except ValueError: pass
            except Exception as e: print("sum count home error",e)
        for x in awayColumn:
            try:
                awayTotal += float(x)
            except ValueError: pass
            except Exception as e: print("sum count away error",e)
        
##        print(homeTotal,awayTotal)
            
        self.tableWidget.setItem(35,1,QTableWidgetItem(str("{:.2f}".format(homeTotal))))
        self.tableWidget.item(35,1).setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setItem(35,2,QTableWidgetItem(str("{:.2f}".format(awayTotal))))
        self.tableWidget.item(35,2).setTextAlignment(QtCore.Qt.AlignCenter)

    def getTableData(self):
        headers = [self.tableWidget.horizontalHeaderItem(0).text(),
                   self.tableWidget.horizontalHeaderItem(1).text(),
                   self.tableWidget.horizontalHeaderItem(1).text()]
        homeColumn = []
        awayColumn = []
        for i in range(self.tableWidget.rowCount()-1):
            try:
                homeColumn.append(self.tableWidget.item(i,1).text())
##                print(homeColumn[-1])
            except AttributeError: pass
            except Exception as e: print("home value",e)
            try:
                awayColumn.append(self.tableWidget.item(i,2).text())
##                print(awayColumn[-1])
            except AttributeError: pass
            except Exception as e: print("away value",e)
            

##        print(date,homeColumn,awayColumn)
        return headers, homeColumn, awayColumn
        
            
        

    def test(self):
##        self.tableWidget.setItem()
        print(dir(self.tableWidget.item(1,0).setTextAlignment(QtCore.Qt.AlignCenter)))




        
rLabels = ["H2H",
"H2H Home and Away Goals",
"Last 5 Games",
"Goals in last 5",
"Conceded in last 5",
"Clean sheets in last 5",
"Last 10 Games",
"Goals in last 10",
"Conceded in last 10",
"Clean sheets in last 10",
"Players above 7 rating",
"Players under 6.5 Rating",
"Players above 7 rating Home/Away",
"Players under 6.5 Rating Home/Away",
"Ammount of Strength",
"Ammount of weaknesses",
"Total Goals",
"Total Conceded",
"Place in League",
"Goals Home/ Away",
"Conceded Home/ Away",
"PPG Home and Away",
"XG Home and Away (For)",
"XG Home and Away (Against)",
"Scored / Match Home and Away",
"Conceded / Match Home and Away",
"Points on weekend games",
"Goals on weekend games",
"Goals conceded on weekend games",
"Weekend Game wins",
"Weekend game loses",
"Win ratio against opposition",
"Total wins against opp",
"Total Draws against opp",
"Total Loses against opp",
"Sum"]


if __name__ == "__main__":
    app = QApplication(sys.argv) # Create a PyQt app
    main = MainWindow() # Initialise the MainWindow
    sys.exit(app.exec_())
    

