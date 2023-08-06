from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from mneprep.popup_messages import alert_msg, confirm_close_window


class FilterOptionsDialog(QWidget):

    def __init__(self, main_window, idx):
        super(FilterOptionsDialog, self).__init__()

        self.setWindowTitle("Filter")

        self.main_window = main_window  # provides a reference to the main window so that main_window.pipeline can be
        # accessed and updated

        self.process_idx = idx  # required to ensure the correct element of main_window.pipeline is accessed (i.e. the
        # element corresponding to the index of the combobox/options button which opened this dialog window)

        # === Create widgets for the dialog GUI ============================================

        self.method_lbl = QLabel("Filter type/method:")
        self.fir_rbtn = QRadioButton("FIR")
        self.iir_rbtn = QRadioButton("IIR")

        self.filter_info_lbl = QLabel("For a band-pass filter, enter both a high and low cutoff. "
                                      "For a high-pass or low-pass filter, enter the appropriate "
                                      "cutoff and leave the other blank.")
        self.filter_info_lbl.setWordWrap(True)

        self.l_input_lbl = QLabel("Low cutoff frequency(Hz):")
        self.l_input = QLineEdit(self)
        self.l_input.setFixedWidth(60)

        self.h_input_lbl = QLabel("High cutoff frequency(Hz):")
        self.h_input = QLineEdit(self)
        self.h_input.setFixedWidth(60)

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
        if process_name == "filter":

            # select the appropriate radiobutton (fir or iir) depending on which method was selected
            if process_params["method"] == "fir":
                self.fir_rbtn.setChecked(True)
                self.iir_rbtn.setChecked(False)

            elif process_params["method"] == "iir":
                self.fir_rbtn.setChecked(False)
                self.iir_rbtn.setChecked(True)

            # Set the frequency cut off QLineEdit widgets to the specified values.
            # If no cut off value has been selected, the param will be None, in which case
            # populate the widget with an empty string
            if process_params["l_freq"] is None:
                self.l_input.setText("")
            else:
                self.l_input.setText(str(process_params["l_freq"]))

            if process_params["h_freq"] is None:
                self.h_input.setText("")
            else:
                self.h_input.setText(str(process_params["h_freq"]))

        # if selecting options for the first time, populate the widgets with default values
        else:
            self.fir_rbtn.setChecked(True)
            # QLineEdit entry boxes for h_freq and l_freq will be blank by default

        # === Create/set layout for the main window GUI ==============================================

        layout = QGridLayout()
        layout.addWidget(self.method_lbl, 0, 0, 1, 2)
        layout.addWidget(self.fir_rbtn, 1, 0)
        layout.addWidget(self.iir_rbtn, 2, 0)
        layout.addWidget(self.filter_info_lbl, 3, 0, 1, 2)
        layout.addWidget(self.l_input_lbl, 4, 0)
        layout.addWidget(self.l_input, 4, 1)
        layout.addWidget(self.h_input_lbl, 5, 0)
        layout.addWidget(self.h_input, 5, 1)
        layout.addWidget(self.update_btn, 6, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 7, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        # === Get selected values for process params from GUI ======================================

        # --- get filter method from radiobuttons ----------------------------------------
        for r_btn in [self.fir_rbtn, self.iir_rbtn]:
            if r_btn.isChecked():
                method = r_btn.text().lower()

        # --- get l_freq value from l_input QLineEdit widget-------------------------------
        # the only acceptable non-numeric value for this parameter is None, which is selected by leaving the
        # l_input blank (so l_input.text is an empty string)
        if self.l_input.text() == "":
            l_cutoff = None
        else:
            try:
                # QLineEdit values are text/strings, therefore convert to a float
                l_cutoff = float(self.l_input.text())

            except ValueError:  # if float conversion unsuccessful
                QMessageBox.warning(self, "Invalid Input", "Low cutoff frequency must be a number")
                self.l_input.clear()
                return

        # --- get h_freq value from h_input QLineEdit widget --------------------------------
        # the only acceptable non-numeric value for this parameter is None, which is selected by leaving the
        # h_input blank (so h_input.text is an empty string)
        if self.h_input.text() == "":
            h_cutoff = None
        else:
            try:
                # QLineEdit values are text/strings, therefore convert to a float
                h_cutoff = float(self.h_input.text())

            except ValueError:  # if float conversion unsuccessful
                QMessageBox.warning(self, "Invalid Input", "High cutoff frequency must be a number")
                self.h_input.clear()
                return

        # === Use process name and params to update main_window.pipeline ===================================

        process_name = "filter"
        process_params = {"l_freq": l_cutoff, "h_freq": h_cutoff, "method": method}

        # update the appropriate step of the main_window.pipeline list with the process name and its options
        self.main_window.update_pipeline_process(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Filter settings updated")  # confirm successful update

        self.close()
