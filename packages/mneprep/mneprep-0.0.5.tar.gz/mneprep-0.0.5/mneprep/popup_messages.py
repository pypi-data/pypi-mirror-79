from PyQt5.QtWidgets import QMessageBox

# Functions related to message boxes used throughout the code.
# Stored in this module to minimise code replication

# function to allow easy creation and configuration of alert message boxes
def alert_msg(window, title, msg):
    alert = QMessageBox(window)
    alert.setWindowTitle(title)
    alert.setText(msg)
    alert.exec_()

# function to confirm exit from a window, such as an options window.
# confirmation message box has two options, "OK" and "Cancel. Default behaviour is set so that if enter button is
# clicked, QMessgaeBox.Cancel is selected
def confirm_close_window(dialog_window):
    reply = QMessageBox.question(dialog_window, 'Confirm',
                                       "Are you sure you want to close this window? Any unsaved changes will be lost",
                                       QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
    if reply == QMessageBox.Ok:
        dialog_window.close()
    else: # reply == QMessageBox.Cancel
        return
