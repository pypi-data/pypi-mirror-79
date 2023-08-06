from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from mneprep.popup_messages import alert_msg, confirm_close_window


class BaseLineOptionsDialog(QWidget):

    def __init__(self, main_window, idx):
        super(BaseLineOptionsDialog, self).__init__()

        self.setWindowTitle("Baseline")

        self.main_window = main_window  # provides a reference to the main window so that main_window.pipeline can be
        # accessed and updated

        self.process_idx = idx  # required to ensure the correct element of main_window.pipeline is accessed (i.e. the
        # element corresponding to the index of the combobox/options button which opened this dialog window)

        # === Create widgets for the dialog GUI ============================================

        self.baseline_lbl = QLabel("Interval over which to baseline:")

        self.a_lbl = QLabel("Start")
        self.a_input = QDoubleSpinBox()
        self.a_input.setMinimum(-10000)
        self.a_input.setSingleStep(0.1)

        self.b_lbl = QLabel("End")
        self.b_input = QDoubleSpinBox()
        self.b_input.setMinimum(-10000)
        self.b_input.setSingleStep(0.1)

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.setFixedWidth(150)
        self.update_btn.clicked.connect(self.update)

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
        if process_name == "baseline":
            interval = process_params["interval"]  # eg (a, b)
            self.a_input.setValue(interval[0])
            self.b_input.setValue(interval[1])

        # if selecting options for the first time, populate the widgets with default values
        else:
            self.a_input.setValue(-0.2)
            self.b_input.setValue(0)

        # === Create/set layout for the main window GUI ==============================================

        layout = QGridLayout()
        layout.addWidget(self.baseline_lbl, 0, 0, 1, 2)
        layout.addWidget(self.a_lbl, 1, 0)
        layout.addWidget(self.a_input, 1, 1)
        layout.addWidget(self.b_lbl, 2, 0)
        layout.addWidget(self.b_input, 2, 1)
        layout.addWidget(self.update_btn, 3, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 4, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        process_name = "baseline"
        process_params = {
            "interval": (self.a_input.value(), self.b_input.value())}  # get selected process params from GUI

        # update the appropriate step of the main_window.pipeline list with the process name and its options
        self.main_window.update_pipeline_process(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Baseline settings updated")  # confirm successful update

        self.close()
