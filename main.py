import sys
import os
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import _recognizer as recognizer

# Globals
main_bg = "rgb(7,44,80)"
secondary_bg = "rgb(8,8,82)"
ternary_bg = "rgb(210,48,44)"


# Dialog Box
def dialog_box(ico, title, body):
    dialog = QMessageBox()
    dialog.setWindowTitle(title)
    dialog.setText(body)
    if ico == "error":
        dialog.setIcon(QMessageBox.Critical)
    elif ico == "warn":
        dialog.setIcon(QMessageBox.Warning)
    elif ico == "question":
        dialog.setIcon(QMessageBox.Question)
        dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    else:
        dialog.setIcon(QMessageBox.Information)
    return dialog.exec_()


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
class UserInterface(object):
    def __init__(self, main_window):
        self.central_widget = QtWidgets.QWidget(main_window)
        self.header = QtWidgets.QFrame(self.central_widget)
        self.body = QtWidgets.QFrame(self.central_widget)

        self.hamburger_btn = QtWidgets.QPushButton(self.header)
        self.leftPanel = QtWidgets.QFrame(self.body)
        self.content = QtWidgets.QFrame(self.body)

        self.home_button = QtWidgets.QPushButton(self.leftPanel)
        self.sketch_button = QtWidgets.QPushButton(self.leftPanel)
        self.emotion_button = QtWidgets.QPushButton(self.leftPanel)
        self.about_button = QtWidgets.QPushButton(self.leftPanel)

        self.stacked_widget = QtWidgets.QStackedWidget(self.content)

        self.home_page = QtWidgets.QWidget()
        self.home_head = QtWidgets.QLabel(self.home_page)
        self.home_body = QtWidgets.QLabel(self.home_page)
        self.upload = QtWidgets.QPushButton(self.home_page)
        self.quit = QtWidgets.QPushButton(self.home_page)

        self.sketch_page = QtWidgets.QWidget()
        self.sketch_head = QtWidgets.QLabel(self.sketch_page)
        self.sketch_browse_btn = QtWidgets.QPushButton(self.sketch_page)
        self.sketch_live_btn = QtWidgets.QPushButton(self.sketch_page)

        self.emotion_page = QtWidgets.QWidget()
        self.emotion_head = QtWidgets.QLabel(self.emotion_page)
        self.emotion_body = QtWidgets.QLabel(self.emotion_page)
        self.emotion_browse_btn = QtWidgets.QPushButton(self.emotion_page)
        self.emotion_live_btn = QtWidgets.QPushButton(self.emotion_page)

        self.about_page = QtWidgets.QWidget()
        self.about_head = QtWidgets.QLabel(self.about_page)
        self.about_body = QtWidgets.QLabel(self.about_page)

        self.animation = QPropertyAnimation(self.leftPanel, b"minimumWidth")
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.body)

    def ui_body(self, main_window):
        # Main window
        main_window.setFixedSize(800, 700)
        main_window.setWindowTitle("Sketch and Emotion Recognition")
        main_window.setObjectName("main_window")
        self.central_widget.setStyleSheet(f"background-color: {main_bg};")
        # Vertical Layout
        self.vertical_layout.setContentsMargins(0, 0, 0, 0)
        self.vertical_layout.setSpacing(0)
        self.vertical_layout.setObjectName("vertical_layout")

        # Header
        self.header.setMaximumSize(QtCore.QSize(16777215, 60))  # width, height
        self.header.setStyleSheet(f"background-color: {main_bg};")
        self.header.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.header.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header.setObjectName("header")
        # Hamburger Button
        self.hamburger_btn.setGeometry(QtCore.QRect(15, 15, 50, 250))
        self.hamburger_btn.setStyleSheet("background:url('static/ham.png') no-repeat; border: none;")
        self.hamburger_btn.clicked.connect(lambda: self.slide_left_panel())
        self.hamburger_btn.setObjectName("hamburger_btn")

        # Body
        self.body.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.body.setFrameShadow(QtWidgets.QFrame.Raised)
        self.body.setObjectName("body")
        # Horizontal Layout
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)
        self.horizontal_layout.setSpacing(0)
        self.horizontal_layout.setObjectName("horizontal_layout")
        # Left Panel
        self.leftPanel.setMaximumSize(QtCore.QSize(0, 16777215))
        self.leftPanel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.leftPanel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.leftPanel.setStyleSheet(f"background-color: {secondary_bg}; margin-top: 15px;")
        self.leftPanel.setObjectName("leftPanel")
        # Center of the body
        self.content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.content.setStyleSheet(f"background-color: {main_bg};")
        self.content.setObjectName("content")

        # Styling for Buttons
        btn_style_1 = f"QPushButton{{" \
                      f"color: rgb(255,255,255); " \
                      f"background-color: {secondary_bg}; " \
                      f"border-radius: 5px; font-size: 15px;" \
                      f"}}" \
                      f" QPushButton:hover{{" \
                      f"color: {secondary_bg}; " \
                      f"background-color: rgb(255,255,255);" \
                      f"}}"
        btn_style_2 = f"QPushButton{{" \
                      f"color: rgb(255,255,255); " \
                      f"background-color: {ternary_bg}; " \
                      f"border-radius: 20px; " \
                      f"font-size: 18px" \
                      f"}} " \
                      f"QPushButton:hover{{" \
                      f"color: {ternary_bg}; " \
                      f"background-color: rgb(255,255,255);" \
                      f"}}"

        # Button for HOME PAGE
        self.home_button.setGeometry(QtCore.QRect(10, 70, 95, 60))
        self.home_button.setStyleSheet(btn_style_1)
        self.home_button.setText("Home")
        self.home_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        self.home_button.setObjectName("home_button")
        # Home Page
        self.home_page.setStyleSheet(f"background-color: {main_bg};")
        self.home_page.setObjectName("home_page")
        # Home heading
        self.home_head.setGeometry(QtCore.QRect(150, 10, 571, 55))
        self.home_head.setStyleSheet(f"border:none; font-size:40px; color: rgb(255,255,0); font-variant: small-caps")
        self.home_head.setText("Sketch and Emotion Recognition")
        self.home_head.setObjectName("home_head")
        # Home Body
        self.home_body.setGeometry(QtCore.QRect(150, 80, 750, 200))
        self.home_body.setStyleSheet(f"border:none; font-size:18px; color: rgb(255,255,0);")
        self.home_body.setText("Welcome to Sketch and Emotion recognizer. "
                               "To recognize Sketch\nand Emotion choose from the Hamburger Menu."
                               "\n\nYou can upload an image into the database, upload a sketch to\nrecognize "
                               "or recognize form live cam")
        self.home_body.setObjectName("home_body")
        # Upload Image Button
        self.upload.setGeometry(QtCore.QRect(150, 280, 500, 50))
        self.upload.setStyleSheet(btn_style_2)
        self.upload.setText("UPLOAD AN IMAGE INTO THE DATABASE")
        self.upload.clicked.connect(lambda: move_to_database())
        self.upload.setObjectName("upload")
        # Exit Button
        self.quit.setGeometry(QtCore.QRect(150, 350, 500, 50))
        self.quit.setStyleSheet(btn_style_2)
        self.quit.setText("EXIT THE APPLICATION")
        self.quit.clicked.connect(lambda: QtCore.QCoreApplication.instance().quit())
        self.quit.setObjectName("quit")

        # Button for SKETCH PAGE
        self.sketch_button.setGeometry(QtCore.QRect(10, 140, 95, 60))
        self.sketch_button.setStyleSheet(btn_style_1)
        self.sketch_button.setText("Sketch\nRecognition")
        self.sketch_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.sketch_page))
        self.sketch_button.setObjectName("sketch_button")
        # Sketch Page
        self.sketch_page.setStyleSheet(f"background-color: {main_bg};")
        self.sketch_page.setObjectName("sketch_page")
        # Sketch Head
        self.sketch_head.setGeometry(QtCore.QRect(250, 10, 571, 51))
        self.sketch_head.setStyleSheet(f"border:none; font-size:40px; color: rgb(255,255,0); font-variant: small-caps")
        self.sketch_head.setText("Sketch Recognition")
        self.sketch_head.setObjectName("sketch_head")
        # Sketch Browse Button
        self.sketch_browse_btn.setGeometry(QtCore.QRect(300, 140, 171, 41))
        self.sketch_browse_btn.setStyleSheet(btn_style_2)
        self.sketch_browse_btn.setText("BROWSE")
        self.sketch_browse_btn.clicked.connect(lambda: get_img())
        self.sketch_browse_btn.setObjectName("sketch_browse_btn")
        # Sketch Live Button
        self.sketch_live_btn.setGeometry(QtCore.QRect(300, 320, 171, 41))
        self.sketch_live_btn.setStyleSheet(btn_style_2)
        self.sketch_live_btn.setText("LIVE")
        self.sketch_live_btn.clicked.connect(lambda: get_img())
        self.sketch_live_btn.setObjectName("sketch_live_btn")

        # Button for EMOTION PAGE
        self.emotion_button.setGeometry(QtCore.QRect(10, 210, 95, 60))
        self.emotion_button.setStyleSheet(btn_style_1)
        self.emotion_button.setText("Emotion\nRecognition")
        self.emotion_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.emotion_page))
        self.emotion_button.setObjectName("emotion_button")
        # Emotion Page
        self.emotion_page.setStyleSheet(f"background-color: {main_bg});")
        self.emotion_page.setObjectName("emotion_page")
        # Emotion heading
        self.emotion_head.setGeometry(QtCore.QRect(250, 10, 571, 55))
        self.emotion_head.setStyleSheet(f"border:none; font-size:40px; color: rgb(255,255,0); font-variant: small-caps")
        self.emotion_head.setText("Emotion Recognition")
        self.emotion_head.setObjectName("emotion_head")
        # Emotion body
        self.emotion_body.setGeometry(QtCore.QRect(150, 80, 750, 200))
        self.emotion_body.setStyleSheet(f"border:none; font-size:18px; color: rgb(255,255,0);")
        self.emotion_body.setText("To recognize the emotion of a Human in an image, click on\nBrowse Image."
                                  "\nTo recognize emotions Live, click on LIVE Recognition.\n  ")
        self.emotion_body.setObjectName("emotion_body")
        # Emotion Browse Button
        self.emotion_browse_btn.setGeometry(QtCore.QRect(150, 280, 500, 50))
        self.emotion_browse_btn.setStyleSheet(btn_style_2)
        self.emotion_browse_btn.setText("BROWSE IMAGE TO RECOGNIZE EMOTION")
        self.emotion_browse_btn.clicked.connect(lambda: recognizer.image_emotion_recognizer(get_img()))
        self.emotion_browse_btn.setObjectName("emotion_browse_btn")
        # Emotion Live Button
        self.emotion_live_btn.setGeometry(QtCore.QRect(150, 350, 500, 50))
        self.emotion_live_btn.setStyleSheet(btn_style_2)
        self.emotion_live_btn.setText("LIVE RECOGNITION")
        self.emotion_live_btn.clicked.connect(lambda: recognizer.live_emotion_recognizer())
        self.emotion_live_btn.setObjectName("emotion_live_btn")

        # Button for ABOUT PAGE
        self.about_button.setGeometry(QtCore.QRect(10, 450, 95, 50))
        self.about_button.setStyleSheet(btn_style_1)
        self.about_button.setText("About")
        self.about_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.about_page))
        self.about_button.setObjectName("about_button")
        # About Page
        self.about_page.setStyleSheet(f"background-color: {main_bg};")
        self.about_page.setObjectName("about_page")
        # About Title
        self.about_head.setGeometry(QtCore.QRect(80, 0, 571, 55))
        self.about_head.setStyleSheet(f"border:none; font-size:40px; color: rgb(255,255,0); font-variant: small-caps;")
        self.about_head.setText("About Us")
        self.about_head.setObjectName("home_head")
        # About Body
        self.about_body.setGeometry(QtCore.QRect(80, 70, 600, 400))
        self.about_body.setStyleSheet(f"border:none; font-size:20px; color: rgb(255,255,255);")
        self.about_body.setText("This application is a University Project developed by "
                                "the Students\nof Presidency University."
                                "\n\nThis application can be used to recognize the Human in a given\nsketch"
                                " and can also be used to recognize the emotion of a Human."
                                "\n\nTo recognize sketch use the SKETCH RECOGNITION menu."
                                "\nTo recognize emotion use the EMOTION RECOGNITION menu."
                                "\n\nThis appliation is built using OpenCv, PyQT and DLib."
                                "\n\nAuthors: Prakyath S Arya\n\tPrathyaksh NP\n\tPrajwal Gowda S\n\t"
                                "Pasang Gurung\n\tPreetham CD")
        self.about_body.setObjectName("home_body")

        # Add widgets into Vertical Layout
        self.vertical_layout.addWidget(self.header)
        self.vertical_layout.addWidget(self.body)

        # Add widgets into Horizontal Layout
        self.horizontal_layout.addWidget(self.leftPanel)
        self.horizontal_layout.addWidget(self.content)

        # Add Window into Central Layout
        main_window.setCentralWidget(self.central_widget)




        # Stack Pages
        self.stacked_widget.setGeometry(QtCore.QRect(-1, 9, 681, 461))
        self.stacked_widget.setCurrentWidget(self.home_page)
        self.stacked_widget.setObjectName("stacked_widget")
        self.stacked_widget.setCurrentWidget(self.home_page)
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.sketch_page)
        self.stacked_widget.addWidget(self.emotion_page)
        self.stacked_widget.addWidget(self.about_page)
        self.stacked_widget.setCurrentIndex(0)

        # Apply everything on Main Window
        QtCore.QMetaObject.connectSlotsByName(main_window)

    # Left Panel Animation
    def slide_left_panel(self):
        width = self.leftPanel.width()

        if width == 0:
            new_width = 110
        else:
            new_width = 0

        self.animation.setDuration(600)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
        self.animation.start()


if __name__ == "__main__":
    # Create App
    app = QtWidgets.QApplication(sys.argv)
    # Add Icon
    icon = QtGui.QIcon()
    icon.addFile("static/icon.png")
    app.setWindowIcon(icon)
    # Create Main Window
    MainWindow = QtWidgets.QMainWindow()
    # Create UI
    ui = UserInterface(MainWindow)
    # Add UI into Main Window
    ui.ui_body(MainWindow)
    # Display the App
    MainWindow.show()
    sys.exit(app.exec_())
