from PyQt5.QtWidgets import *
from mne.io.pick import get_channel_type_constants, channel_type
from mneprep.popup_messages import confirm_close_window


class PickChannelsDialog(QWidget):

    def __init__(self, plot_window):
        super(PickChannelsDialog, self).__init__()

        self.plot_window = plot_window  # provides a reference to the plot window, used later to access plot_window
        # attributes (data_list and picks)

        self.setWindowTitle("Pick Channels to Plot")

        info = self.plot_window.data_list[0][0].info  # get info from first data object in plot_window.data_list

        # === create & popluate list widgets of available channels in data ============================================

        # create list widget
        self.channels_view = QListWidget()
        self.channels_view.setSpacing(7)
        self.channels_view.setSelectionMode(QListWidget.ExtendedSelection) # allows selection of multiple channels

        # populate list widget with names and types of all data channels (ie not stim/misc channels)
        for index, ch in enumerate(info["chs"]):
            ch_type = channel_type(info, index).upper()
            ch_name = ch["ch_name"]
            item = QListWidgetItem(ch_name + "    " + ch_type)
            self.channels_view.addItem(item)

            # If channels have already been picked (i.e. are already in plot_window.picks), set them as selected in the
            # list widget. Like 'saving' previously picked channels
            if ch_name in plot_window.picks:
                item.setSelected(True)

        # === create other widgets for the main window GUI ============================================

        self.update_btn = QPushButton('Update', self)
        self.update_btn.clicked.connect(self.update)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(lambda: confirm_close_window(self))

        # === create/set layout for the main window GUI ==============================================

        layout = QVBoxLayout()
        layout.addWidget(self.channels_view)
        layout.addWidget(self.update_btn)
        layout.addWidget(self.cancel_btn)
        self.setLayout(layout)

    def update(self):

        for item in self.channels_view.selectedItems():  # for each channel selected in the list widget
            ch_name = item.text().split("   ")[0]  # get the name of the channel
            self.plot_window.picks.append(ch_name)  # append it to the picks list

        # check that channels have been picked before closing the window
        if len(self.plot_window.picks) > 0:
            self.close()
        else:
            QMessageBox.warning(self, "No Channels Selected", "Please select at least one channel")

