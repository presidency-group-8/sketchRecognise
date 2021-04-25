import sys
import os
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import _faceRecog as face_recog

# Globals
main_bg = "rgb(7,44,80)"
secondary_bg = "rgb(8,8,82)"
terneray_bg = "rgb(210,48,44)"


# Dialog Box
def dialog_box(icon, title, body):
    dbox = QMessageBox()
    dbox.setWindowTitle(title)
    dbox.setText(body)
    if icon == "error":
        dbox.setIcon(QMessageBox.Critical)
    elif icon == "warn":
        dbox.setIcon(QMessageBox.Warning)
    elif icon == "question":
        dbox.setIcon(QMessageBox.Question)
        dbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    else:
        dbox.setIcon(QMessageBox.Information)
    return dbox.exec_()


def get_img():
    img_format = ["jpg", "jpeg", "png", "jfif", "bmp", "ico"]
    img = list(QFileDialog.getOpenFileNames(None, "Select image", r"C:/Users/aryap/Downloads/"))
    source = str(img[0])[2:-2]
    # Error if file is not an Image
    if source.split(".")[-1] not in img_format:
        dialog_box("error", "Invalid File !", "Please choose an image of .jpg, .jpeg, .jfif, .png, .bmp, or .ico only")
        return None
    return source


def move_to_database():
    source = get_img()
    if source:
        database = "C:/Users/aryap/Documents/Python Scripts/sketchRecognise/knownImages/"
        source, database = source.replace("/", "\\"), database.replace("/", "\\")
        sure = dialog_box("question", "Sure ?", "Do you want to upload your selection?")
        if sure == 16384:
            error = os.system(f'copy "{source}" "{database}"')
            if not error:
                dialog_box("success", "Success !", "The image has been uploaded into the database successfully")
            else:
                dialog_box("error", "Error !", "There was some error while accessing the database")
    return


# Main Class
class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        # Main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(800, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet(f"background-color: {main_bg};")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.header = QtWidgets.QFrame(self.centralwidget)

        # Title bar
        self.header.setMaximumSize(QtCore.QSize(16777215, 50))  # width, height
        self.header.setStyleSheet(f"background-color: {main_bg};")
        self.header.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header.setObjectName("header")

        # Body
        self.body = QtWidgets.QFrame(self.centralwidget)
        self.body.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.body.setFrameShadow(QtWidgets.QFrame.Raised)
        self.body.setObjectName("body")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.body)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Center of the body
        self.content = QtWidgets.QFrame(self.body)
        self.content.setStyleSheet(f"background-color: {main_bg};")
        self.content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content.setObjectName("content")

        # Hamburger Menu
        self.hamHolder = QtWidgets.QFrame(self.header)
        self.hamHolder.setGeometry(QtCore.QRect(0, 0, 80, 51))  # size co ordinates
        self.hamHolder.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.hamHolder.setFrameShadow(QtWidgets.QFrame.Raised)
        self.hamHolder.setObjectName("hamHolder")
        # Hamburger Button
        self.hamburgerBtn = QtWidgets.QPushButton(self.hamHolder)
        self.hamburgerBtn.setGeometry(QtCore.QRect(10, 10, 50, 250))
        self.hamburgerBtn.setStyleSheet("background-image: url('static/ham.png'); border: none;")
        self.hamburgerBtn.setObjectName("hamburgerBtn")
        self.verticalLayout.addWidget(self.header)
        # Hamburger onClick()
        self.hamburgerBtn.clicked.connect(lambda: self.slideLeftMenu())

        # Left Panel
        self.leftPanel = QtWidgets.QFrame(self.body)
        self.leftPanel.setMaximumSize(QtCore.QSize(10, 16777215))
        self.leftPanel.setStyleSheet(f"background-color: {secondary_bg}; margin-top: 15px;")
        self.leftPanel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.leftPanel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftPanel.setObjectName("leftPanel")

        # Styling for Buttons
        btn_style_1 = f"QPushButton{{color: rgb(255,255,255); background-color: {secondary_bg}; border-radius: 5px; font-size: 15px;}} QPushButton:hover{{color: {secondary_bg}; background-color: rgb(255,255,255);}}"
        btn_style_2 = f"QPushButton{{color: rgb(255,255,255); background-color: {terneray_bg}; border-radius: 20px; font-size: 18px}} QPushButton:hover{{color: {terneray_bg}; background-color: rgb(255,255,255);}}"


        # PushButton for HOME PAGE
        self.pushButton = QtWidgets.QPushButton(self.leftPanel)
        self.pushButton.setGeometry(QtCore.QRect(10, 70, 95, 60))
        self.pushButton.setStyleSheet(btn_style_1)
        self.pushButton.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.home_page))
        self.pushButton.setObjectName("pushButton")
        # Home Page
        self.home_page = QtWidgets.QWidget()
        self.home_page.setStyleSheet(f"background-color: {main_bg};")
        self.home_page.setObjectName("home_page")
        self.stackedWidget = QtWidgets.QStackedWidget(self.content)
        self.stackedWidget.setGeometry(QtCore.QRect(-1, 9, 681, 461))
        self.stackedWidget.setCurrentWidget(self.home_page)
        self.stackedWidget.setObjectName("stackedWidget")
        self.stackedWidget.setCurrentWidget(self.home_page)
        self.stackedWidget.addWidget(self.home_page)
        # Home heading
        self.home_head = QtWidgets.QLabel(self.home_page)
        self.home_head.setStyleSheet(f"border:none; font-size:40px; color: rgb(255,255,0); font-variant: small-caps")
        self.home_head.setText("Sketch and Emotion Recognition")
        self.home_head.setGeometry(QtCore.QRect(150, 10, 571, 55))
        self.home_head.setObjectName("home_head")
        # Home Body
        self.home_body = QtWidgets.QLabel(self.home_page)
        self.home_body.setStyleSheet(f"border:none; font-size:18px; color: rgb(255,255,0);")
        self.home_body.setText("Welcome to Sketch and Emotion recognizer. To recognize Sketch\nand Emotion choose from the Hamburger Menu.\n\nYou can upload an image into the database, upload a sketch to\nrecognize or recognize form live cam")
        self.home_body.setGeometry(QtCore.QRect(150, 80, 750, 200))
        self.home_body.setObjectName("home_body")
        # Upload Image Button
        self.upload = QtWidgets.QPushButton(self.home_page)
        self.upload.setGeometry(QtCore.QRect(150, 280, 500, 50))
        self.upload.setStyleSheet(btn_style_2)
        self.upload.clicked.connect(lambda: move_to_database())
        self.upload.setObjectName("upload")
        # Exit Button
        self.quit = QtWidgets.QPushButton(self.home_page)
        self.quit.setGeometry(QtCore.QRect(150, 350, 500, 50))
        self.quit.setStyleSheet(btn_style_2)
        self.quit.clicked.connect(lambda: QtCore.QCoreApplication.instance().quit())
        self.quit.setObjectName("quit")


        # PushButton for  SKETCH PAGE
        self.pushButton_2 = QtWidgets.QPushButton(self.leftPanel)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 140, 95, 60))
        self.pushButton_2.setStyleSheet(btn_style_1)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.sketch_page))
        # Sketch Page
        self.sketch_page = QtWidgets.QWidget()
        self.sketch_page.setStyleSheet(f"background-color: {main_bg};")
        self.sketch_page.setObjectName("sketch_page")
        self.sketch_head = QtWidgets.QLabel(self.sketch_page)
        self.sketch_head.setStyleSheet(f"border:none; font-size:40px; color: rgb(255,255,0); font-variant: small-caps")
        self.sketch_head.setText("Sketch Recognition")
        self.sketch_head.setGeometry(QtCore.QRect(250, 10, 571, 51))
        self.sketch_head.setObjectName("sketch_head")
        self.stackedWidget.addWidget(self.sketch_page)
        # Browse Button
        self.sketchBrowseBtn = QtWidgets.QPushButton(self.sketch_page)
        self.sketchBrowseBtn.setGeometry(QtCore.QRect(300, 140, 171, 41))
        self.sketchBrowseBtn.setStyleSheet(btn_style_2)
        self.sketchBrowseBtn.clicked.connect(lambda: get_img())
        self.sketchBrowseBtn.setObjectName("sketchBrowseBtn")
        # Sketch Upload Button
        self.sketchUploadBtn = QtWidgets.QPushButton(self.sketch_page)
        self.sketchUploadBtn.setGeometry(QtCore.QRect(300, 230, 171, 41))
        self.sketchUploadBtn.setStyleSheet(btn_style_2)
        self.sketchUploadBtn.clicked.connect(lambda: getFile())
        self.sketchUploadBtn.setObjectName("sketchUploadBtn")
        # Start Button
        self.sketchStartBtn = QtWidgets.QPushButton(self.sketch_page)
        self.sketchStartBtn.setGeometry(QtCore.QRect(300, 320, 171, 41))
        self.sketchStartBtn.setStyleSheet(btn_style_2)
        self.sketchStartBtn.setObjectName("sketchStartBtn")


        # PushButton for EMOTION PAGE
        self.pushButton_3 = QtWidgets.QPushButton(self.leftPanel)
        self.pushButton_3.setGeometry(QtCore.QRect(10, 210, 95, 60))
        self.pushButton_3.setStyleSheet(btn_style_1)
        self.pushButton_3.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.emotion_page))
        self.pushButton_3.setObjectName("pushButton_3")
        # Emotion Page
        self.emotion_page = QtWidgets.QWidget()
        self.emotion_page.setStyleSheet(f"background-color: {main_bg});")
        self.emotion_page.setObjectName("emotion_page")
        self.stackedWidget.addWidget(self.emotion_page)
        # Emotion heading
        self.emotion_head = QtWidgets.QLabel(self.emotion_page)
        self.emotion_head.setStyleSheet(f"border:none; font-size:40px; color: rgb(255,255,0); font-variant: small-caps")
        self.emotion_head.setText("Emotion Recognition")
        self.emotion_head.setGeometry(QtCore.QRect(250, 10, 571, 55))
        self.emotion_head.setObjectName("emotion_head")
        # Emotion body
        self.emotion_body = QtWidgets.QLabel(self.emotion_page)
        self.emotion_body.setStyleSheet(f"border:none; font-size:18px; color: rgb(255,255,0);")
        self.emotion_body.setText("To recognize the emotion of a Human in an image, click on\nBrowse Image.\nTo recognize emotions Live, click on LIVE Recognition.\n  ")
        self.emotion_body.setGeometry(QtCore.QRect(150, 80, 750, 200))
        self.emotion_body.setObjectName("emotion_body")
        # Browse Button
        self.emotion_browse_btn = QtWidgets.QPushButton(self.emotion_page)
        self.emotion_browse_btn.setGeometry(QtCore.QRect(150, 280, 500, 50))
        self.emotion_browse_btn.setStyleSheet(btn_style_2)
        self.emotion_browse_btn.clicked.connect(lambda: face_recog.image_emotion_recognizer(get_img()))
        self.emotion_browse_btn.setObjectName("emotion_browse_btn")
        # Open Cam Button
        self.emotion_live_btn = QtWidgets.QPushButton(self.emotion_page)
        self.emotion_live_btn.setGeometry(QtCore.QRect(150, 350, 500, 50))
        self.emotion_live_btn.setStyleSheet(btn_style_2)
        self.emotion_live_btn.clicked.connect(lambda: face_recog.live_emotion_recognizer())
        self.emotion_live_btn.setObjectName("emotion_live_btn")
        self.stackedWidget.addWidget(self.emotion_page)

        # PushButton for ABOUT PAGE
        self.pushButton_4 = QtWidgets.QPushButton(self.leftPanel)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 450, 95, 50))
        self.pushButton_4.setStyleSheet(btn_style_1)
        self.pushButton_4.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.about_page))
        self.pushButton_4.setObjectName("pushButton_4")
        # About Page
        self.about_page = QtWidgets.QWidget()
        self.about_page.setStyleSheet(f"background-color: {main_bg};")
        self.about_page.setObjectName("about_page")
        # About Title
        self.about_head = QtWidgets.QLabel(self.about_page)
        self.about_head.setStyleSheet(f"border:none; font-size:40px; color: rgb(255,255,0); font-variant: small-caps;")
        self.about_head.setText("About Us")
        self.about_head.setGeometry(QtCore.QRect(80, 0, 571, 55))
        self.about_head.setObjectName("home_head")
        # About Body
        self.about_body = QtWidgets.QLabel(self.about_page)
        self.about_body.setStyleSheet(f"border:none; font-size:20px; color: rgb(255,255,255);")
        self.about_body.setText(
            "This application is a University Project developed by the Students\nof Presidency University.\n\nThis application can be used to recognize the Human in a given\nsketch and can also be used to recognize the emotion of a Human.\n\nTo recognize sketch use the SKETCH RECOGNITION menu.\nTo recognize emotion use the EMOTION RECOGNITION menu.\n\nThis appliation is built using OpenCv, PyQT and DLib.\n\nAuthors: Prakyath S Arya\n\tPrathyaksh NP\n\tPrajwal Gowda S\n\tPasang Gurung\n\tPreetham CD")
        self.about_body.setGeometry(QtCore.QRect(80, 70, 600, 400))
        self.about_body.setObjectName("home_body")
        self.stackedWidget.addWidget(self.about_page)

        # Add all panel buttons to panel
        self.horizontalLayout.addWidget(self.leftPanel)
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
        self.stackedWidget.setCurrentIndex(0)  # stack of pages...index makes the given page to show up first
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Set Names
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        # Set App Title
        MainWindow.setWindowTitle(_translate("MainWindow", "Sketch and Emotion Recognition"))

        # Set Left Panel Button Names
        self.pushButton.setText(_translate("MainWindow", "Home"))
        self.pushButton_2.setText(_translate("MainWindow", "Sketch\nRecognition"))
        self.pushButton_3.setText(_translate("MainWindow", "Emotion\nRecognition"))
        self.pushButton_4.setText(_translate("MainWindow", "About"))

        # Set HOME PAGE Button Names
        self.upload.setText(_translate("MainWindow", "UPLOAD AN IMAGE INTO THE DATABASE"))
        self.quit.setText(_translate("MainWindow", "EXIT THE APPLICATION"))

        # Set SKETCH PAGE Button Names
        self.sketchBrowseBtn.setText(_translate("MainWindow", "BROWSE"))
        self.sketchUploadBtn.setText(_translate("MainWindow", "SKETCH"))
        self.sketchStartBtn.setText(_translate("MainWindow", "START"))

        # Set EMOTION PAGE Button Names
        self.emotion_browse_btn.setText(_translate("MainWindow", "BROWSE IMAGE TO RECOGNIZE EMOTION"))
        self.emotion_live_btn.setText(_translate("MainWindow", "LIVE RECOGNITION"))


    # Left Panel Animation
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
icon = QtGui.QIcon()
icon.addFile("static/icon.png")
app.setWindowIcon(icon)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
