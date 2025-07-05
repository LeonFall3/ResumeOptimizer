from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon, QKeySequence
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QMessageBox,
)

# Only needed for access to command line arguments
import sys
import json
import subprocess

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resume and Cover Letter Optimizer")
        self.setGeometry(100, 100, 800, 600)  # Set the position and size of the window
        self.setFixedSize(QSize(400, 300))  # Set a fixed size for the window

        # label = QLabel("Setup")
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # self.setCentralWidget(label)  # Set the label as the central widget

        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        button_action = QAction("Run Setup", self)
        button_action.setStatusTip("Click to run setup")
        button_action.triggered.connect(self.on_setup_button_click)
        toolbar.addAction(button_action)

        self.setStatusBar(QStatusBar(self))  # Set a status bar for the main window

    def on_setup_button_click(self):
        print("Setup clicked!")
        self.setup_window = SetupWindow()
        self.setup_window.show()

class SetupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Setup User Info")
        self.setFixedSize(QSize(350, 250))

        layout = QVBoxLayout()

        self.first_name_input = QLineEdit()
        self.first_name_input.setPlaceholderText("First Name")
        layout.addWidget(QLabel("First Name:"))
        layout.addWidget(self.first_name_input)

        self.last_name_input = QLineEdit()
        self.last_name_input.setPlaceholderText("Last Name")
        layout.addWidget(QLabel("Last Name:"))
        layout.addWidget(self.last_name_input)

        self.multiple_jobs_checkbox = QCheckBox("Applying for multiple job types?")
        layout.addWidget(self.multiple_jobs_checkbox)

        self.job_types_input = QLineEdit()
        self.job_types_input.setPlaceholderText("Job types (comma separated)")
        layout.addWidget(QLabel("Job Types:"))
        layout.addWidget(self.job_types_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_user_info)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_user_info(self):
        subprocess.Popen([sys.executable, "SetUp.py"])
        first_name = self.first_name_input.text().capitalize()
        last_name = self.last_name_input.text().capitalize()
        user = first_name + last_name
        multiple_jobs = self.multiple_jobs_checkbox.isChecked()
        job_types = [jt.strip() for jt in self.job_types_input.text().split(",") if jt.strip()]
        job_types.append("general")  # Ensure 'General' is always included
        if not job_types:
            job_types = ["general"]

        user_info = {
            "user": user,
            "multiple_jobs": multiple_jobs,
            "job_types": job_types
        }
        with open("user_info.json", "w", encoding="utf-8") as user_info_json:
            json.dump(user_info, user_info_json, indent=4)
        QMessageBox.information(self, "Saved", "User info saved successfully!")
        self.close()


        


# You need one (and only one) QApplication instance per application.
# Pass in sys.argv to allow command line arguments for your app.
# If you know you won't use command line arguments QApplication([]) works too.
app = QApplication(sys.argv)

# window = QWidget()  # Create a window. This is the main window of your application.
# window = QPushButton("Push me!")
window = MainWindow()  # Create a main window. This is the main window of your application.
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()

