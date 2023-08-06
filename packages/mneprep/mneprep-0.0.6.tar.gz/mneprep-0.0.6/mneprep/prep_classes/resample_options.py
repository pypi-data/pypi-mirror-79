from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from mneprep.popup_messages import alert_msg, confirm_close_window


class ResampleOptionsDialog(QWidget):

    def __init__(self, main_window, idx):
        super(ResampleOptionsDialog, self).__init__()

        self.setWindowTitle("Resample")

        self.main_window = main_window  # provides a reference to the main window so that main_window.pipeline can be
        # accessed and updated

        self.process_idx = idx  # required to ensure the correct element of main_window.pipeline is accessed (i.e. the
        # element corresponding to the index of the combobox/options button which opened this dialog window)

        # === Create widgets for the dialog GUI ============================================

        self.sfreq_spinbox_lbl = QLabel("New sampling frequency (Hz):")
        self.sfreq_spinbox = QSpinBox(self)
        self.sfreq_spinbox.setMaximum(9999)
        self.sfreq_spinbox.setFixedWidth(60)

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.clicked.connect(self.update)
        self.update_btn.setFixedWidth(150)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: confirm_close_window(self))

        # === Populate/configure the options widgets ==============================================================
        # If options have already been selected for this process at this step in the pipeline (i.e. the options
        # window is being re-opened), populate widgets using the values previously selected.
        # Like 'saving' and re-accessing the selected options

        # check the name and params of the process currently selected at this step of the pipeline
        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        # if options have already been selected, use them to populate the widgets
        if process_name == "resample":
            self.sfreq_spinbox.setValue(process_params["sfreq"])

        # if selecting options for the first time, populate the widgets with default values
        else:
            self.sfreq_spinbox.setValue(250)

        # === Create/set layout for the main window GUI ==============================================

        layout = QGridLayout()
        layout.addWidget(self.sfreq_spinbox_lbl, 0, 0)
        layout.addWidget(self.sfreq_spinbox, 0, 1)
        layout.addWidget(self.update_btn, 1, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 2, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        process_name = "resample"
        process_params = {"sfreq": int(self.sfreq_spinbox.value())}  # get selected process params from GUI

        # update the appropriate step of the main_window.pipeline list with the process name and its options
        self.main_window.update_pipeline_process(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Resampling settings updated")  # confirm successful update

        self.close()
