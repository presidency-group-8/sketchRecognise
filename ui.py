import sys
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog

# To store the directory path folderPath is used..its made global
folderPath = ""


# Function to show files when sketch to be uploaded btn is clicked
def getFolder():
    file = str(QFileDialog.getExistingDirectory(None, "Select Directory"))  #opening the directory and storing
    global folderPath
    folderPath = file  #assigning path to global variable

def getFile():
    file = str(QFileDialog.getOpenFileNames(None, "Select Directory"))  # opening the file and storing
    global folderPath
    folderPath = file  # assigning path to global variable

#Outer Frame
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        #Size of the window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("background-color: rgb(0, 0, 0);") #colors..
        self.centralwidget.setObjectName("centralwidget") #some typical pyqt5 widgets
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header = QtWidgets.QFrame(self.centralwidget)

        # Title bar
        self.header.setMaximumSize(QtCore.QSize(16777215, 50))  #width, height
        self.header.setStyleSheet("")
        self.header.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header.setObjectName("header")

        #block which holds ham btn
        self.hamHolder = QtWidgets.QFrame(self.header)
        self.hamHolder.setGeometry(QtCore.QRect(0, 0, 111, 51))  #size co ordinates
        self.hamHolder.setStyleSheet("")
        self.hamHolder.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.hamHolder.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hamHolder.setObjectName("hamHolder")


        self.hamburgerBtn = QtWidgets.QPushButton(self.hamHolder)
        self.hamburgerBtn.setGeometry(QtCore.QRect(10, 10, 51, 28))
        self.hamburgerBtn.setStyleSheet("background-color: rgb(0,0,0);")

        #when ham is clicked slideLeftMenu is called
        self.hamburgerBtn.clicked.connect(lambda : self.slideLeftMenu())
        self.hamburgerBtn.setText("")


        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/menu.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.hamburgerBtn.setIcon(icon)
        self.hamburgerBtn.setIconSize(QtCore.QSize(16, 16))
        self.hamburgerBtn.setObjectName("hamburgerBtn")
        self.verticalLayout.addWidget(self.header)

        #body parts
        self.body = QtWidgets.QFrame(self.centralwidget)
        self.body.setStyleSheet("")
        self.body.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.body.setFrameShadow(QtWidgets.QFrame.Raised)
        self.body.setObjectName("body")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.body)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Left side panel which opens up, width is 10 for slideLeftMenu to run properly.
        self.leftPanel = QtWidgets.QFrame(self.body)
        self.leftPanel.setMaximumSize(QtCore.QSize(10, 16777215))
        self.leftPanel.setStyleSheet("background-color: rgb(0,0,0);\n"
"")
        self.leftPanel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.leftPanel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftPanel.setObjectName("leftPanel")


        # pushButton is for HOME PAGE
        self.pushButton = QtWidgets.QPushButton(self.leftPanel)
        self.pushButton.setGeometry(QtCore.QRect(10, 40, 93, 28))
        self.pushButton.setStyleSheet("QPushButton\n"
        "{\n"
        "    color:rgb(255,255,255);\n"
        "    background-color: rgb(0, 0, 0);\n"
        "    border-radius:10;\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{\n"
        "    background-color: rgb(255,255,255);\n"
        "    color:rgb(0,0,0);\n"
        "}")

        #on clicking this button it takes to home page
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.homePage))
        self.pushButton.setObjectName("pushButton")


        # For SKETCH PAGE
        self.pushButton_2 = QtWidgets.QPushButton(self.leftPanel)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 100, 93, 28))
        self.pushButton_2.setStyleSheet("QPushButton\n"
        "{\n"
        "    color:rgb(255,255,255);\n"
        "    background-color: rgb(0, 0, 0);\n"
        "    border-radius:10;\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{\n"
        "    background-color: rgb(255,255,255);\n"
        "    color:rgb(0,0,0);\n"
        "}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.sketchPage))


        # For EMOTION PAGE
        self.pushButton_3 = QtWidgets.QPushButton(self.leftPanel)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 160, 93, 28))
        self.pushButton_3.setStyleSheet("QPushButton\n"
        "{\n"
        "    color:rgb(255,255,255);\n"
        "    background-color: rgb(0, 0, 0);\n"
        "    border-radius:10;\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{\n"
        "    background-color: rgb(255,255,255);\n"
        "    color:rgb(0,0,0);\n"
        "}")
        self.pushButton_3.clicked.connect(lambda : self.stackedWidget.setCurrentWidget(self.emotionPage))
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.leftPanel)


        self.content = QtWidgets.QFrame(self.body)
        self.content.setStyleSheet("")
        self.content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content.setObjectName("content")

        self.homePage = QtWidgets.QWidget()
        self.homePage.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.homePage.setObjectName("homePage")


        self.stackedWidget = QtWidgets.QStackedWidget(self.content)
        self.stackedWidget.setGeometry(QtCore.QRect(-1, 9, 681, 461))
        self.stackedWidget.setCurrentWidget(self.homePage)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setCurrentWidget(self.homePage)



        self.textEdit = QtWidgets.QTextEdit(self.homePage)
        self.textEdit.setGeometry(QtCore.QRect(110, 10, 571, 51))
        self.textEdit.setObjectName("textEdit")
        self.stackedWidget.addWidget(self.homePage)
        self.emotionPage = QtWidgets.QWidget()
        self.emotionPage.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.emotionPage.setObjectName("emotionPage")
        self.textEdit_2 = QtWidgets.QTextEdit(self.emotionPage)
        self.textEdit_2.setGeometry(QtCore.QRect(100, 20, 581, 51))
        self.textEdit_2.setObjectName("textEdit_2")
        self.emotionUploadFrame = QtWidgets.QFrame(self.emotionPage)
        self.emotionUploadFrame.setGeometry(QtCore.QRect(100, 100, 281, 361))
        self.emotionUploadFrame.setStyleSheet("background-color: rgb(255, 255, 255);\n"
        "border-radius : 30px;")
        self.emotionUploadFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.emotionUploadFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.emotionUploadFrame.setObjectName("emotionUploadFrame")

        #the variable name itself tells what are what.
        self.emotionBrowseBtn = QtWidgets.QPushButton(self.emotionUploadFrame)
        self.emotionBrowseBtn.setGeometry(QtCore.QRect(60, 80, 171, 41))
        self.emotionBrowseBtn.setStyleSheet("QPushButton\n"
        "{\n"
        "    border-radius : 20px;\n"
        "    border : 2px solid red;\n"
        "    color: white;\n"
        "    background-color : rgb(255,0,0);\n"
        "    font-size : 18px;\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{\n"
        "    border: 2px solid white;\n"
        "    color : white;\n"
        "    background-color : rgb(0,0,0);\n"
        "    font-size : 18px;\n"
        "}")
        self.emotionBrowseBtn.clicked.connect(lambda : getFolder())
        self.emotionBrowseBtn.setObjectName("emotionBrowseBtn")


        self.emotionStartBtn = QtWidgets.QPushButton(self.emotionUploadFrame)
        self.emotionStartBtn.setGeometry(QtCore.QRect(60, 200, 171, 41))
        self.emotionStartBtn.setStyleSheet("QPushButton\n"
        "{\n"
        "    border-radius : 20px;\n"
        "    border : 2px solid black;\n"
        "    color: black;\n"
        "    background-color : rgb(255,255,255);\n"
        "    font-size : 18px;\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{\n"
        "    border: 2px solid white;\n"
        "    color : white;\n"
        "    background-color : rgb(0,0,0);\n"
        "    font-size : 18px;\n"
        "}")
        self.emotionStartBtn.setObjectName("emotionStartBtn")


        self.emotionLiveFrame = QtWidgets.QFrame(self.emotionPage)
        self.emotionLiveFrame.setGeometry(QtCore.QRect(395, 100, 281, 361))
        self.emotionLiveFrame.setStyleSheet("background-color: rgb(255, 0, 0);\n"
"border-radius : 30px;")
        self.emotionLiveFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.emotionLiveFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.emotionLiveFrame.setObjectName("emotionLiveFrame")
        self.emotionLiveBtn = QtWidgets.QPushButton(self.emotionLiveFrame)
        self.emotionLiveBtn.setGeometry(QtCore.QRect(60, 150, 171, 41))
        self.emotionLiveBtn.setStyleSheet("QPushButton\n"
        "{\n"
        "    border-radius : 20px;\n"
        "    border : 2px solid black;\n"
        "    background-color : rgba(0,0,0);\n"
        "    color: white;\n"
        "    font-size : 18px;\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{\n"
        "    border: 2px solid black;\n"
        "    color : black;\n"
        "    background-color : rgb(255,255,255);\n"
        "    font-size : 18px;\n"
        "}")
        self.emotionLiveBtn.setObjectName("emotionLiveBtn")


        self.stackedWidget.addWidget(self.emotionPage)
        self.sketchPage = QtWidgets.QWidget()
        self.sketchPage.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.sketchPage.setObjectName("sketchPage")
        self.sketchBrowseBtn = QtWidgets.QPushButton(self.sketchPage)
        self.sketchBrowseBtn.setGeometry(QtCore.QRect(300, 140, 171, 41))
        self.sketchBrowseBtn.setStyleSheet("QPushButton\n"
        "{\n"
        "    border-radius : 20px;\n"
        "    border : 2px solid red;\n"
        "    color: white;\n"
        "    font-size : 18px;\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{\n"
        "    border: 1px solid black;\n"
        "    color : white;\n"
        "    background-color : rgb(255,0,0,0.8);\n"
        "    font-size : 18px;\n"
        "}")
        self.sketchBrowseBtn.clicked.connect(lambda : getFolder())
        self.sketchBrowseBtn.setObjectName("sketchBrowseBtn")


        self.sketchUploadBtn = QtWidgets.QPushButton(self.sketchPage)
        self.sketchUploadBtn.setGeometry(QtCore.QRect(300, 230, 171, 41))
        self.sketchUploadBtn.setStyleSheet("QPushButton\n"
        "{\n"
        "    border-radius : 20px;\n"
        "    border : 2px solid red;\n"
        "    color: white;\n"
        "    font-size : 18px;\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{\n"
        "    border: 1px solid black;\n"
        "    color : white;\n"
        "    background-color : rgb(255,0,0,0.8);\n"
        "    font-size : 18px;\n"
        "}")
        self.sketchUploadBtn.clicked.connect(lambda : getFile())
        self.sketchUploadBtn.setObjectName("sketchUploadBtn")


        self.sketchStartBtn = QtWidgets.QPushButton(self.sketchPage)
        self.sketchStartBtn.setGeometry(QtCore.QRect(300, 320, 171, 41))
        self.sketchStartBtn.setStyleSheet("QPushButton\n"
        "{\n"
        "    border-radius : 20px;\n"
        "    border : 2px solid red;\n"
        "    color: white;\n"
        "    font-size : 18px;\n"
        "}\n"
        "\n"
        "QPushButton:hover\n"
        "{\n"
        "    border: 1px solid black;\n"
        "    color : white;\n"
        "    background-color : rgb(255,0,0,0.8);\n"
        "    font-size : 18px;\n"
        "}")
        self.sketchStartBtn.setObjectName("sketchStartBtn")


        self.textEdit_3 = QtWidgets.QTextEdit(self.sketchPage)
        self.textEdit_3.setGeometry(QtCore.QRect(100, 20, 581, 51))
        self.textEdit_3.setObjectName("textEdit_3")
        self.stackedWidget.addWidget(self.sketchPage)
        self.horizontalLayout.addWidget(self.content)
        self.verticalLayout.addWidget(self.body)
        self.footer = QtWidgets.QFrame(self.centralwidget)
        self.footer.setMaximumSize(QtCore.QSize(16777215, 50))
        self.footer.setStyleSheet("")
        self.footer.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.footer.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer.setObjectName("footer")
        self.verticalLayout.addWidget(self.footer)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0) # stack of pages...index makes the given page to show up first

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "HOME"))
        self.pushButton_2.setText(_translate("MainWindow", "SKETCH"))
        self.pushButton_3.setText(_translate("MainWindow", "EMOTION"))
        self.textEdit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:14pt; color:#ffffff;\"> SKETCH BASED FACIAL AND EMTION DETECTOR</span></p></body></html>"))
        self.textEdit_2.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; color:#ffffff;\"> EMOTION BASED RECOGNITION</span></p></body></html>"))
        self.emotionBrowseBtn.setText(_translate("MainWindow", "BROWSE"))
        self.emotionStartBtn.setText(_translate("MainWindow", "START"))
        self.emotionLiveBtn.setText(_translate("MainWindow", "LIVE CAMERA"))
        self.sketchBrowseBtn.setText(_translate("MainWindow", "BROWSE"))
        self.sketchUploadBtn.setText(_translate("MainWindow", "SKETCH"))
        self.sketchStartBtn.setText(_translate("MainWindow", "START"))
        self.textEdit_3.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:18pt; color:#ffffff;\"> SKETCH BASED RECOGNITION</span></p></body></html>"))




    #code for left panel animation
    def slideLeftMenu(self):
        width = self.leftPanel.width()

        if width == 10:
            newWidth = 110
        else:
            newWidth = 10

        self.animation = QPropertyAnimation(self.leftPanel, b"minimumWidth")  # Animate minimumWidth
        self.animation.setDuration(250)
        self.animation.setStartValue(width)  # Start value is the current menu width
        self.animation.setEndValue(newWidth)  # end value is the new menu width
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


# Main
app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
