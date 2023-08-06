from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from mneprep.popup_messages import alert_msg, confirm_close_window


class EpochOptionsDialog(QWidget):

    def __init__(self, main_window, idx):
        super(EpochOptionsDialog, self).__init__()

        self.setWindowTitle("Epoch")

        self.main_window = main_window  # provides a reference to the main window so that main_window.pipeline can be
        # accessed and updated

        self.process_idx = idx  # required to ensure the correct element of main_window.pipeline is accessed (i.e. the
        # element corresponding to the index of the combobox/options button which opened this dialog window)

        # === Create widgets for the dialog GUI ============================================

        self.fixed_length_rbtn = QRadioButton("Fixed length epochs")
        self.fixed_length_rbtn.clicked.connect(self.toggle_options)

        self.tstep_lbl = QLabel("Epoch interval")
        self.tstep_input = QDoubleSpinBox()
        self.tstep_input.setMinimum(0.1)
        self.tstep_input.setSingleStep(0.1)

        self.events_rbtn = QRadioButton("Epoch around events")
        self.events_rbtn.clicked.connect(self.toggle_options)

        self.tmin_lbl = QLabel("Tmin")
        self.tmin_input = QDoubleSpinBox()
        self.tmin_input.setMinimum(-10000)
        self.tmin_input.setSingleStep(0.1)

        self.tmax_lbl = QLabel("Tmax")
        self.tmax_input = QDoubleSpinBox()
        self.tmax_input.setMinimum(-10000)
        self.tmax_input.setSingleStep(0.1)

        self.autoreject_check = QCheckBox("Drop bad segments and epochs\nusing Autoreject thresholds")

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.setFixedWidth(150)
        self.update_btn.clicked.connect(self.update)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: confirm_close_window(self))

        # === Populate/configure the options widgets ==============================================================
        # If options have already been selected for this process at this step in the pipeline (i.e. the options
        # window is being re-opened), populate/configure widgets using the values previously selected.
        # Like 'saving' and re-accessing the selected options

        # check the name and params of the process currently selected at this step of the pipeline
        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        # if options have already been selected, use them to populate/configure the widgets
        if process_name == "epoch":

            if process_params["tmin"] is not None:  # if epoching around events

                # Set the radiobuttons so that epoching around events is selected if a stimulus channel has been
                # selected in the main window (meaning the data contains events), otherwise creating fixed epochs
                # is selected
                self.events_rbtn.setChecked(True)
                self.fixed_length_rbtn.setChecked(False)

                # Set values for the epoch interval widgets
                self.tmin_input.setValue(process_params["tmin"])
                self.tmax_input.setValue(process_params["tmax"])
                self.tstep_input.setValue(5.0)  # default value

            elif process_params["tstep"] is not None:  # if no events, therefore creating fixed-length epochs
                self.events_rbtn.setChecked(False)
                self.fixed_length_rbtn.setChecked(True)
                self.tstep_input.setValue(process_params["tstep"])
                self.tmin_input.setValue(-0.2)  # default value
                self.tmax_input.setValue(0.5)  # default value

            # call a function to check that the correct widgets are enabled/disabled depending on if epoching around
            # events or creating fixed length epochs)
            self.toggle_options()

            self.autoreject_check.setChecked(process_params["autoreject"])

        # if selecting options for the first time, populate the widgets with default values
        else:
            # Set default values for the epoch interval widgets
            self.tstep_input.setValue(5.0)
            self.tmin_input.setValue(-0.2)
            self.tmax_input.setValue(0.5)

            # Set the radiobuttons based on whether a stimulus channel has been selected in the main window. If so, the
            # data contains events, so epoching around events is selected. Otherwise, creating fixed epochs is selected.
            if self.main_window.no_stim_ch_rbtn.isChecked():
                self.fixed_length_rbtn.setChecked(True)
                self.events_rbtn.setChecked(False)
            elif self.main_window.stim_ch_rbtn.isChecked():
                self.fixed_length_rbtn.setChecked(False)
                self.events_rbtn.setChecked(True)

            # call a function to check that the correct widgets are enabled/disabled depending on if epoching around
            # events or creating fixed length epochs)
            self.toggle_options()

            self.autoreject_check.setChecked(True)

        # === Create/set layout for the main window GUI ==============================================

        layout = QGridLayout()
        layout.addWidget(self.fixed_length_rbtn, 0, 0, 1, 2)
        layout.addWidget(self.tstep_lbl, 1, 0)
        layout.addWidget(self.tstep_input, 1, 1)

        layout.addWidget(self.events_rbtn, 2, 0, 1, 2)
        layout.addWidget(self.tmin_lbl, 3, 0)
        layout.addWidget(self.tmin_input, 3, 1)
        layout.addWidget(self.tmax_lbl, 4, 0)
        layout.addWidget(self.tmax_input, 4, 1)

        layout.addWidget(self.autoreject_check, 5, 0, 1, 2)
        layout.addWidget(self.update_btn, 6, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 7, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        # === Error check for trying to epoch around events if no events present/no stim channel ==
        if self.main_window.no_stim_ch_rbtn.isChecked() & self.events_rbtn.isChecked():
            QMessageBox.warning(self, "No Stim Channel Selected",
                                "Stim channel must be selected in order to epoch around events")
            return

        # === Get selected values for process params from GUI ======================================

        if self.events_rbtn.isChecked():
            tmin = self.tmin_input.value()
            tmax = self.tmax_input.value()
            tstep = None

        elif self.fixed_length_rbtn.isChecked():
            tmin = None
            tmax = None
            tstep = self.tstep_input.value()

        # === Use process name and params to update main_window.pipeline ===================================

        process_name = "epoch"
        process_params = {"tmin": tmin, "tmax": tmax, "tstep": tstep,
                          "autoreject": self.autoreject_check.isChecked()}

        # update the appropriate step of the main_window.pipeline list with the process name and its options
        self.main_window.update_pipeline_process(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Epoch settings updated")  # confirm successful update

        self.close()

    def toggle_options(self):
        # This function check that the correct widgets are enabled/disabled depending on if epoching around
        # events or creating fixed length epochs)

        if self.events_rbtn.isChecked():  # if data contains events
            self.tmin_input.setDisabled(False)
            self.tmax_input.setDisabled(False)
            self.tstep_input.setDisabled(True)

        elif self.fixed_length_rbtn.isChecked():  # if data does not contain events
            self.tmin_input.setDisabled(True)
            self.tmax_input.setDisabled(True)
            self.tstep_input.setDisabled(False)
