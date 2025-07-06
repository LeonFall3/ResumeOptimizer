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
    QMessageBox, QFileDialog
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
        
        #Main layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        
        #toolbar
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        #setup button
        setup_action = QAction("Run Setup", self)
        setup_action.setStatusTip("Click to run setup")
        setup_action.triggered.connect(self.on_setup_button_click)
        toolbar.addAction(setup_action)

        #update documents button
        update_documents_action = QAction("Update Documents", self)
        update_documents_action.setStatusTip("Click to update documents")
        update_documents_action.triggered.connect(self.on_documents_button_click)
        toolbar.addAction(update_documents_action)

        self.setStatusBar(QStatusBar(self))  # Set a status bar for the main window


    def on_setup_button_click(self):
        print("Setup clicked!")
        self.setup_window = SetupWindow()
        self.setup_window.show()

    def on_documents_button_click(self):
        print("Update Documents clicked!")

        # Check for user_info.json before setting up the UI
        try:
            with open("user_info.json", "r", encoding="utf-8") as f:
                user_info = json.load(f)
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", "User info file not found. Please run setup first.")
            return
        self.update_documents_window = UpdateDocumentsWindow()
        self.update_documents_window.show()

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

        self.cover_letter_checkbox = QCheckBox("Do want to optimize your cover letter as well?")
        layout.addWidget(self.cover_letter_checkbox)

        self.multiple_jobs_checkbox = QCheckBox("Applying for multiple job types?")
        self.multiple_jobs_checkbox.stateChanged.connect(self.toggle_job_types_input)
        layout.addWidget(self.multiple_jobs_checkbox)

        # Job types input (hidden by default)
        self.job_types_input = QLineEdit()
        self.job_types_input.setPlaceholderText("Job types (comma separated)")
        self.job_types_label = QLabel("Job Types:")
        self.job_types_input.hide()
        self.job_types_label.hide()
        layout.addWidget(self.job_types_label)
        layout.addWidget(self.job_types_input)
        

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_user_info)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def toggle_job_types_input(self, state):
        if state == Qt.CheckState.Checked.value:
            self.job_types_input.show()
            self.job_types_label.show()
        else:
            self.job_types_input.hide()
            self.job_types_label.hide()

    def save_user_info(self):
        subprocess.Popen([sys.executable, "SetUp.py"])
        first_name = self.first_name_input.text().capitalize()
        last_name = self.last_name_input.text().capitalize()
        user = first_name + last_name
        multiple_jobs = self.multiple_jobs_checkbox.isChecked()
        cover_letter = self.cover_letter_checkbox.isChecked()
        if multiple_jobs:
            job_types = [jt.strip() for jt in self.job_types_input.text().split(",") if jt.strip()]
            job_types.append("general")  # Ensure 'General' is always included
        else:
            job_types = ["general"]

        user_info = {
            "user": user,
            "cover_letter": cover_letter,
            "multiple_jobs": multiple_jobs,
            "job_types": job_types
        }
        with open("user_info.json", "w", encoding="utf-8") as user_info_json:
            json.dump(user_info, user_info_json, indent=4)
        QMessageBox.information(self, "Saved", "User info saved successfully!")
        self.close()

class UpdateDocumentsWindow(QWidget):
    def __init__(self):
        

        
        super().__init__()
        self.setWindowTitle("Update Documents")
        self.setFixedSize(QSize(350, 250))
        with open("user_info.json", "r", encoding="utf-8") as f:
            user_info = json.load(f)
        layout = QVBoxLayout()
        
        # check if user wants to optimize cover letter
        if user_info.get("cover_letter") is True:
            cover_letter_upload_button = QPushButton("Upload Cover Letter")
            cover_letter_upload_button.clicked.connect(self.upload_documents)
            layout.addWidget(cover_letter_upload_button)

        self.setLayout(layout)

        #check for multiple jobs
        if user_info.get("multiple_jobs") is True:
            print("Multiple jobs is enabled!")
            job_types = user_info.get("job_types", [])
            for job_type in job_types:
                job_button = QPushButton(f"Upload Resume for {job_type.capitalize()}")
                job_button.clicked.connect(lambda checked, jt=job_type: self.upload_job_resume(jt))
                layout.addWidget(job_button)
        else:
            print("Multiple jobs is not enabled.")


    def upload_documents(self):
        resume_path, _ = QFileDialog.getOpenFileName(self, "Select Resume File", "", "PDF Files (*.pdf);;All Files (*)")
        cover_letter_path, _ = QFileDialog.getOpenFileName(self, "Select Cover Letter File", "", "Markdown Files (*.md);;PDF Files (*.pdf);;All Files (*)")

        if resume_path:
            # self.resume_file_input.setText(resume_path)
            print(f"Selected resume file: {resume_path}")
        if cover_letter_path:
            print(f"Selected cover letter file: {cover_letter_path}")
            # self.cover_letter_file_input.setText(cover_letter_path)
        


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

