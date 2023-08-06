from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from mneprep.popup_messages import alert_msg, confirm_close_window


class LineNoiseOptionsDialog(QWidget):

    def __init__(self, main_window, idx):
        super(LineNoiseOptionsDialog, self).__init__()

        self.setWindowTitle("Remove Power Line Noise")

        self.main_window = main_window  # provides a reference to the main window so that main_window.pipeline can be
        # accessed and updated

        self.process_idx = idx  # required to ensure the correct element of main_window.pipeline is accessed (i.e. the
        # element corresponding to the index of the combobox/options button which opened this dialog window)

        # === Create widgets for the dialog GUI ============================================

        self.info_lbl = QLabel("A notch filter will be used to suppress the frequencies at which line noise occurs.")
        self.info_lbl.setWordWrap(True)
        self.info_lbl.setStyleSheet("margin-bottom: 15px")

        self.method_lbl = QLabel("Notch filter type/method:")
        self.fir_rbtn = QRadioButton("FIR")
        self.iir_rbtn = QRadioButton("IIR")

        self.l_noise_lbl1 = QLabel("Line noise frequency(Hz):")
        self.l_noise_lbl2 = QLabel("(Harmonics can be included\neg 50, 100, 150)")
        self.l_noise_input = QLineEdit(self)
        self.l_noise_input.setFixedWidth(100)

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
        if process_name == "line_noise":

            # --- select the appropriate radiobutton (fir or iir) depending on which method was selected --------
            if process_params["method"] == "fir":
                self.fir_rbtn.setChecked(True)
                self.iir_rbtn.setChecked(False)

            elif process_params["method"] == "iir":
                self.fir_rbtn.setChecked(False)
                self.iir_rbtn.setChecked(True)

            # --- Set the frequency cut off QLineEdit widget to the specified value  -----------------------------

            # If no cut off value has been selected, the param will be None, in which case
            # populate the widget with an empty string
            if process_params["freqs"] is None:
                self.l_input.setText("")

            # if just one value provided eg 50 or (50) or (50,)
            elif type(process_params["freqs"]) == int:
                freqs_str = str(process_params["freqs"])  # convert to string
                self.l_noise_input.setText(freqs_str)

            else:  # multiple values in tuple eg (50, 100), (50, 100,)
                freqs_str = str(process_params["freqs"])[1:-1]  # [1:-1] to get rid of the tuple brackets
                self.l_noise_input.setText(freqs_str)

        # if selecting options for the first time, populate the widgets with default values
        else:
            self.fir_rbtn.setChecked(True)
            self.iir_rbtn.setChecked(False)
            self.l_noise_input.setText("50")

        # === Create/set layout for the main window GUI ==============================================

        layout = QGridLayout()
        layout.addWidget(self.info_lbl, 0, 0, 1, 2)
        layout.addWidget(self.method_lbl, 1, 0, 1, 2)
        layout.addWidget(self.fir_rbtn, 2, 0)
        layout.addWidget(self.iir_rbtn, 3, 0)
        layout.addWidget(self.l_noise_lbl1, 4, 0)
        layout.addWidget(self.l_noise_input, 4, 1)
        layout.addWidget(self.l_noise_lbl2, 5, 0, 1, 2)
        layout.addWidget(self.update_btn, 6, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 7, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        # === Get selected values for process params from GUI ======================================

        # --- get filter method from radiobuttons ----------------------------------------
        for r_btn in [self.fir_rbtn, self.iir_rbtn]:
            if r_btn.isChecked():
                method = r_btn.text().lower()

        # --- get freqs values(frequencies at which to notch filter) from l_noise_input QLineEdit widget ----------

        freqs_lst = []  # empty list to hold all frequencies to be removed with notch filter

        try:
            # if multiple values are provided in a tuple, split the tuple to get the individual values
            if ", " in self.l_noise_input.text():
                split = self.l_noise_input.text().split(", ")
                for value in split:
                    freqs_lst.append(int(value))  # convert from string to int and add to freqs_lst

            else:
                # if only one value provided (so no comma present in the tuple)
                freqs_lst.append(int(self.l_noise_input.text()))  # convert from string to int and add to freqs_lst

        except ValueError:  # if int conversion unsuccessful
            QMessageBox.warning(self, "Invalid Input", "Enter one or more integer values eg 50, 100, 150")
            self.l_noise_input.clear()
            return

        # === Use process name and params to update main_window.pipeline ===================================

        freqs = tuple(freqs_lst)
        process_name = "line_noise"
        process_params = {"freqs": freqs, "method": method}

        # update the appropriate step of the main_window.pipeline list with the process name and its options
        self.main_window.update_pipeline_process(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Line noise removal settings updated")  # confirm successful update

        self.close()
