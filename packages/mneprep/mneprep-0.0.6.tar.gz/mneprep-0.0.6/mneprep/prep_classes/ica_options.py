from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from mne import pick_types

from mneprep.popup_messages import alert_msg, confirm_close_window


class ICAOptionsDialog(QWidget):

    def __init__(self, main_window, idx):
        super(ICAOptionsDialog, self).__init__()

        self.setWindowTitle("ICA")

        self.main_window = main_window  # provides a reference to the main window so that main_window.pipeline can be
        # accessed and updated

        self.process_idx = idx  # required to ensure the correct element of main_window.pipeline is accessed (i.e. the
        # element corresponding to the index of the combobox/options button which opened this dialog window)

        ica_methods = ["FastICA", "Infomax", "Picard"]  # list of available ICA methods

        # calculate number of data channels (i.e. meg & eeg) in data. Used later to populate widget for n_comps
        picks = pick_types(self.main_window.data.info, meg=True, eeg=True, eog=False, ecg=False)
        num_data_chs = len(picks)

        # === Create widgets for the dialog GUI ============================================

        # --- Widgets to select ICA method ---------------------------------
        self.method_lbl = QLabel("Method:")

        self.method_select = QComboBox()
        self.method_select.addItems(ica_methods)
        self.method_select.activated[str].connect(self.toggle_extended_option)

        self.extended_lbl = QLabel("Extended:")  # extended option available for Infomax and Picard methods
        self.extended = QCheckBox()

        # --- Widgets to select number of components ------------------------
        self.n_comps_lbl = QLabel("Set number of components by:")

        # user supplies specific number of components to be generated
        self.n_comps_rbtn = QRadioButton("Number of components:")
        self.n_comps_rbtn.clicked.connect(self.toggle_n_comp_options)
        self.n_comps = QSpinBox()
        self.n_comps.setRange(1, num_data_chs)  # max possible num of components = number of channels in data

        # number of components calculated to explain a specified fraction of variance
        self.n_comps_var_rbtn = QRadioButton("Cumulative explained variance:")
        self.n_comps_var_rbtn.clicked.connect(self.toggle_n_comp_options)
        self.n_components_var = QDoubleSpinBox()
        self.n_components_var.setRange(0.01, 0.99)
        self.n_components_var.setSingleStep(0.01)

        # button group separates these radiobuttons from the rejection method radiobuttons below
        self.n_comps_btns = QButtonGroup()
        self.n_comps_btns.addButton(self.n_comps_rbtn)
        self.n_comps_btns.addButton(self.n_comps_var_rbtn)

        # --- Widgets to exclude bad data segments/epochs during ICA -------
        self.exclude_bad_segments_lbl = QLabel("Exclude bad segments\n (determined by Autoreject threshold):")
        self.exclude_bad_segments = QCheckBox()

        # --- Widgets to select method for rejecting ICA components ---------------
        self.rejection_method_lbl = QLabel("Method for rejecting ICA components:")

        self.manual_rbtn = QRadioButton("Manually")
        self.ecg_eog_rbtn = QRadioButton("Automatically using EOG and ECG")

        # button group separates these radiobuttons from the n_comps radiobuttons above
        self.exclusion_methods_btns = QButtonGroup()
        self.exclusion_methods_btns.addButton(self.manual_rbtn)
        self.exclusion_methods_btns.addButton(self.ecg_eog_rbtn)

        self.update_btn = QPushButton('Update Settings', self)
        self.update_btn.setFixedWidth(150)
        self.update_btn.clicked.connect(self.update)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.setFixedWidth(150)
        self.cancel_btn.clicked.connect(lambda: confirm_close_window(self))

        self.toggle_extended_option()

        # === Populate/configure the options widgets ==============================================================
        # If options have already been selected for this process at this step in the pipeline (i.e. the options
        # window is being re-opened), populate/configure widgets using the values previously selected.
        # Like 'saving' and re-accessing the selected options

        # check the name and params of the process currently selected at this step of the pipeline
        process_name = main_window.pipeline[idx][0]
        process_params = main_window.pipeline[idx][1]

        # if options have already been selected, use them to populate/configure the widgets
        if process_name == "ICA":

            # --- Set ICA method ----------------------------------------------------
            for i in range(len(ica_methods)):
                if process_params["ica_method"] == ica_methods[i].lower():
                    self.method_select.setCurrentIndex(i)

            # --- Set if ICA method "extended" selected -----------------------------
            self.extended.setChecked(process_params["extended"])

            # --- Set number of ICA components --------------------------------------
            if process_params["n_comps"] >= 1:  # if num components
                self.n_comps_rbtn.setChecked(True)
                self.n_comps.setDisabled(False)
                self.n_comps.setValue(process_params["n_comps"])
                self.n_comps_var_rbtn.setChecked(False)
                self.n_components_var.setValue(0.95)  # default value
                self.n_components_var.setDisabled(True)

            elif process_params["n_comps"] < 1:  # if variance explained
                self.n_comps_var_rbtn.setChecked(True)
                self.n_components_var.setDisabled(False)
                self.n_components_var.setValue(process_params["n_comps"])
                self.n_comps.setDisabled(True)
                self.n_comps.setValue(num_data_chs)  # default value
                self.n_comps_rbtn.setChecked(False)

            # --- Ensure appropriate widgets are enabled/disabled based on the -----
            # --- selections for ICA method and number of components ---------------
            self.toggle_n_comp_options()
            self.toggle_extended_option()

            # --- Set if automatically rejecting bad segments/epochs ----------------
            self.exclude_bad_segments.setChecked(process_params["autoreject"])

            # --- Set method for component rejection --------------------------------
            if process_params["rejection_method"] == "manual":
                self.manual_rbtn.setChecked(True)
                self.ecg_eog_rbtn.setChecked(False)

            elif process_params["rejection_method"] == "ecg_eog":
                self.manual_rbtn.setChecked(False)
                self.ecg_eog_rbtn.setChecked(True)

        # If selecting options for the first time, populate the widgets with default values
        else:
            self.n_comps_rbtn.setChecked(True)
            self.n_comps.setValue(num_data_chs)
            self.n_components_var.setDisabled(True)
            self.n_components_var.setValue(0.95)
            self.exclude_bad_segments.setChecked(True)
            self.manual_rbtn.setChecked(True)
            self.ecg_eog_rbtn.setChecked(False)

        # === Create/set layout for the main window GUI ==============================================

        layout = QGridLayout()
        layout.addWidget(self.method_lbl, 0, 0)
        layout.addWidget(self.method_select, 0, 1)
        layout.addWidget(self.extended_lbl, 1, 0)
        layout.addWidget(self.extended, 1, 1)
        layout.addWidget(self.n_comps_lbl, 3, 0)
        layout.addWidget(self.n_comps_rbtn, 4, 0)
        layout.addWidget(self.n_comps, 4, 1)
        layout.addWidget(self.n_comps_var_rbtn, 5, 0)
        layout.addWidget(self.n_components_var, 5, 1)
        layout.addWidget(self.exclude_bad_segments_lbl, 6, 0)
        layout.addWidget(self.exclude_bad_segments, 6, 1)
        layout.addWidget(self.rejection_method_lbl, 7, 0, 1, 2)
        layout.addWidget(self.manual_rbtn, 8, 0)
        layout.addWidget(self.ecg_eog_rbtn, 9, 0, 1, 2)
        layout.addWidget(self.update_btn, 10, 0, 1, 2, Qt.AlignHCenter)
        layout.addWidget(self.cancel_btn, 11, 0, 1, 2, Qt.AlignHCenter)
        self.setLayout(layout)

    def toggle_extended_option(self):
        # This function toggles if the extended option is available depending on the ICA method selected

        if self.method_select.currentText() == "FastICA":  # disable and uncheck extended
            self.extended_lbl.setEnabled(False)
            self.extended.setChecked(False)
            self.extended.setEnabled(False)

        else:  # if Picard or Infomax, enable extended
            self.extended_lbl.setEnabled(True)
            self.extended.setEnabled(True)

    def toggle_n_comp_options(self):
        # This function enables/disables the options relating to number of ICA components
        # depending on if the user specifies the number of components to be generated or
        # the variance to be explained

        if self.n_comps_rbtn.isChecked():  # if number of components to be generated
            self.n_comps.setDisabled(False)
            self.n_components_var.setDisabled(True)

        elif self.n_comps_var_rbtn.isChecked():  # if variance to be explained
            self.n_comps.setDisabled(True)
            self.n_components_var.setDisabled(False)

    def update(self):

        # === Get selected values for process params from GUI ======================================

        # --- Get ICA method
        if self.manual_rbtn.isChecked():
            rej_method = "manual"
        elif self.ecg_eog_rbtn.isChecked():
            rej_method = "ecg_eog"

        # --- Get value for number of components to be generated
        if self.n_comps_rbtn.isChecked():
            n_components = self.n_comps.value()
        elif self.n_comps_var_rbtn.isChecked():
            n_components = self.n_components_var.value()

        # === Use process name and params to update main_window.pipeline ===================================

        process_name = "ICA"
        process_params = {"n_comps": n_components,
                          "ica_method": self.method_select.currentText().lower(),
                          "extended": self.extended.isChecked(),
                          "autoreject": self.exclude_bad_segments.isChecked(),
                          "rejection_method": rej_method}

        # update the appropriate step of the main_window.pipeline list with the process name and its options
        self.main_window.update_pipeline_process(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "ICA settings updated")  # confirm successful update

        self.close()
