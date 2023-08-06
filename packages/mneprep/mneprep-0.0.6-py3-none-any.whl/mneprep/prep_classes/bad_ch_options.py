from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from mneprep.popup_messages import alert_msg, confirm_close_window


class ChannelOptionsDialog(QWidget):

    def __init__(self, main_window, idx):
        super(ChannelOptionsDialog, self).__init__()

        self.setWindowTitle("Mark Bad Channels")

        self.main_window = main_window  # provides a reference to the main window so that main_window.pipeline can be
        # accessed and updated

        self.process_idx = idx  # required to ensure the correct element of main_window.pipeline is accessed (i.e. the
        # element corresponding to the index of the combobox/options button which opened this dialog window)

        # === Create widgets for the dialog GUI ============================================

        self.info_lbl = QLabel("At this step in the pipeline the channels \n"
                               "will be plotted, allowing you to identify \n"
                               "and select bad channels from the plots.\n\n"
                               "These channels will not be removed \n"
                               "from the data, but will be excluded from \n"
                               "subsequent processes unless they are \n"
                               "interpolated.")
        self.info_lbl.setWordWrap(True)

        self.interp_check = QCheckBox("Interpolate bad channels")
        self.interp_check.setStyleSheet("margin: 15px, 0")

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

        # if options have already been selected, use them to populate/confiure the widgets
        if process_name == "channels":
            self.interp_check.setChecked(process_params["interpolate"])

        # if selecting options for the first time, populate the widgets with default values
        else:
            self.interp_check.setChecked(True)

        # === Create/set layout for the main window GUI ==============================================

        layout = QVBoxLayout()
        layout.addWidget(self.info_lbl)
        layout.addWidget(self.interp_check)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
        layout.setAlignment(self.update_btn, Qt.AlignHCenter)
        layout.setAlignment(self.cancel_btn, Qt.AlignHCenter)
        self.setLayout(layout)

    def update(self):

        process_name = "channels"
        process_params = {"interpolate": self.interp_check.isChecked()}  # get selected process params from GUI

        # update the appropriate step of the main_window.pipeline list with the process name and its options
        self.main_window.update_pipeline_process(self.process_idx, process_name, process_params)

        alert_msg(self, "Update Successful", "Bad channel settings updated")  # confirm successful update

        self.close()

