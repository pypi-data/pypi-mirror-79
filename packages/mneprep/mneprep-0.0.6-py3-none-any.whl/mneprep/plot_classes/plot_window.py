import mne

from PyQt5.QtWidgets import *

from mneprep.plot_classes.pick_chs_dialog import PickChannelsDialog
from mneprep.plot_classes.time_series_tab import TimeSeriesTab
from mneprep.plot_classes.psd_tab import PSDTab
from mneprep.plot_classes.epo_evoked_tab import TopoEpochsEvokedTab


class PlotWindow(QWidget):

    def __init__(self):
        super(PlotWindow, self).__init__()

        self.setWindowTitle("Plot Options")

        # list to be populated with data later by the load_raw_data function eg [(data_obj1, file_name1), ...]
        self.data_list = [(),()]

        # list to be populated with channel names later by the pick_chs_dialog window if user wishes to select the
        # channels to be plotted
        self.picks = []

        # === create widgets for the plot window GUI ============================================

        self.title_lbl = QLabel("Select up to two FIF files to visualise.\n \n"
                                "Both files must contain the same channels and events,\n"
                                " e.g. the results of two different preprocessing pipelines \n"
                                "run on the same raw data. \n \n"
                                "If you only wish to visualise one file, please \n"
                                "select it as File 1, not File 2. \n")

        self.open1_btn = QPushButton("Load 1st Data File")
        self.open1_btn.clicked.connect(lambda: self.load_in_data(1))
        self.file1_lbl = QLabel("File 1: No file loaded yet ")

        self.open2_btn = QPushButton("Load 2nd Data File")
        self.open2_btn.clicked.connect(lambda: self.load_in_data(2))
        self.file2_lbl = QLabel("File 2: No file loaded yet")

        self.select_chs_lbl = QLabel("Select channels to plot:")
        self.select_chs_cbox = QComboBox()
        self.select_chs_cbox.activated[str].connect(self.pick_channels)
        self.select_chs_cbox.setFixedWidth(150)

        self.time_series_tab = TimeSeriesTab(self)
        self.psd_tab = PSDTab(self)
        self.topo_epoch_evoked_tab = TopoEpochsEvokedTab(self)
        self.topo_epoch_evoked_tab.setDisabled(True) # disable this tab initially, enable later once data has been
        # confirmed to be Epochs, not Raw type

        self.tabs = QTabWidget()
        self.tabs.addTab(self.time_series_tab, "Time Series")
        self.tabs.addTab(self.psd_tab, "PSD")
        self.tabs.addTab(self.topo_epoch_evoked_tab, "Epochs and Evoked Responses")

        # === create/set layout for the plot window GUI ==============================================

        layout = QGridLayout()
        layout.addWidget(self.title_lbl, 1, 0, 1, 3)
        layout.addWidget(self.open1_btn, 2, 0)
        layout.addWidget(self.file1_lbl, 3, 0, 1, 3)
        layout.addWidget(self.open2_btn, 4, 0)
        layout.addWidget(self.file2_lbl, 5, 0, 1, 3)
        layout.addWidget(self.select_chs_lbl, 6, 0)
        layout.addWidget(self.select_chs_cbox, 6, 1)
        layout.addWidget(self.tabs, 8, 0, 1, 3)
        self.setLayout(layout)

    def load_in_data(self, data_num):
        # This function opens a file dialog for the selection of a file to read data from
        # The parameter data_num is an integer (1 or 2),reflecting whether data file 1 or 2 is being loaded

        # Get name/path of file to load from file dialog. Only show/support .fif files as all results from pipelines
        # are saved in .fif format
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Open...", "",
                                                  "(*.fif)", options=options)  # only show .fif files

        if file_path != "":
            try:
                # Get the file name (the last part of the file path if the file path is long/contains "/")
                if "/" in file_path:
                    file_name = file_path.split("/")[-1]
                else:  # if the file path is short/does not contain "/"
                    file_name = file_path

                # call the appropriate MNE function to read in the data depending on its type (Raw vs Epoch),
                # then call a function to populate the GUI and data attributes of the class using the data
                if file_path.endswith("raw.fif"):
                    data = mne.io.read_raw_fif(file_path)
                    self.populate_data_and_widgets(data, file_name, data_num)
                elif file_path.endswith("epo.fif"):
                    data = mne.read_epochs(file_path)
                    self.populate_data_and_widgets(data, file_name, data_num)

            except ValueError:
                QMessageBox.warning(self, "Error", "Problem reading file in to MNE.")
                return

    def populate_data_and_widgets(self, data, file_name, data_num):
        # This function is called when a data object (passed to the function as the parameter data) is read in from a file.
        # It stores the data object in the data.list variable and updates the GUI file labels to show the name of the
        # file from which the data object was loaded
        # The parameter data_num is an integer (1 or 2),reflecting whether it was data file 1 or 2 that was loaded in
        # If data 1, the combobox in the GUI from which the types of channels to be plotted is also updated using the
        # channel types present in data 1.

        if data_num == 1:

            self.data_list[0] = (data, file_name)  # populate the first element in self.data_list

            self.file1_lbl.setText("File 1: " + file_name)  # set the GUI label to reflect the file name

            # clear and repopulate the combobox with the channel types present in data 1.
            self.select_chs_cbox.clear()

            # "All data channels" and "Pick channels" included by default for all data objects
            self.select_chs_cbox.addItems(["All data channels", "Pick channels"])

            # "EEG only" and "MEG only" only included as options if MEG/EEG channels are present in the data respectively
            if "eeg" in data:
                self.select_chs_cbox.addItem("EEG only")
            if "meg" in data:
                self.select_chs_cbox.addItem("MEG only")

            if isinstance(data, mne.BaseEpochs):
                # populate topo_epoch_evoked_tab combobox with keys from event_id dict
                # both sets of data should have the same events if they are the results of different
                # pipelines run on the same data, so just take the event ids from the first set of data
                event_dict = data.event_id
                event_ids = [i for i in event_dict.keys()]
                self.topo_epoch_evoked_tab.populate_events_cbox(event_ids)

        elif data_num == 2:

            self.data_list[1] = (data, file_name)  # populate the second element in self.data_list

            self.file2_lbl.setText("File 2: " + file_name)  # set the GUI label to reflect the file name

        # Fianlly, call function to update if the Epochs and Evoked Responses Tab is enabled depending on the data that has just
        # been loaded in
        self.toggle_enabled_plots()

    def get_data_updated_chs(self):
        # This function creates a list of data to be plotted by taking the data objects that have been
        # loaded in and making copies of them which contain only the channels selected to be plotted.
        # The list is then returned.

        # check that the first data file has been loaded in (so that there is definitely data to plot)
        if len(self.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        else:

            plot_data_list = [] # empty list to populate with the data to be plotted (ie with the channels selected)

            for i in range(len(self.data_list)):  # for each element in data_list

                if len(self.data_list[i]) != 0:  # check if data has been loaded for that element
                    data = self.data_list[i][0]  # if so, store it in the variable "data"

                    # Create a copy of the data which contains only the channels that were selected to be plotted,
                    # and add it to plot_data_list:

                    if self.select_chs_cbox.currentText() == "All data channels":
                        plot_data = data.load_data().copy().pick_types(meg=True, eeg=True, stim=False, eog=False, exclude=[])
                        plot_data_list.append(plot_data)

                    elif self.select_chs_cbox.currentText() == "MEG only":
                        plot_data = data.load_data().copy().pick_types(meg=True, eeg=False, stim=False, eog=False, exclude=[])
                        plot_data_list.append(plot_data)

                    elif self.select_chs_cbox.currentText() == "EEG only":
                        plot_data = data.load_data().copy().pick_types(meg=False, eeg=True, stim=False, eog=False, exclude=[])
                        plot_data_list.append(plot_data)

                    elif self.select_chs_cbox.currentText() == "Pick channels":
                        plot_data = data.load_data().copy().pick_types(meg=False, eeg=False, stim=False, eog=False,
                                                                       include=self.picks, exclude=[])
                        plot_data_list.append(plot_data)

            return plot_data_list

    def pick_channels(self):
        # This function is called any time a value is selected in the "select channels to plot" combobox.
        # If "pick channels" has been selected, the dialog window in which the channels can be picked is opened.

        # Ensure that the first data file has been loaded in (so there is definitely data to pick channels from)
        if len(self.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        # if the user has selected to pick specific channels to plot...
        if self.select_chs_cbox.currentText() == "Pick channels":
            pick_channels_dialog = PickChannelsDialog(self)  # create an instance of the PickChannelsDialog window
            pick_channels_dialog.show()  # open it

    def toggle_enabled_plots(self):
        # This function enables the epoch_and_evoked tab if:
        # 1) only file 1 is loaded and it is epoched data
        # 2) both files are loaded and both files are epoched data
        # This prevents errrors bu ensuring that the plots in this tab (which are only suitable for Epoch data)
        # are not attempted for Raw data

        # Get the data items from data_list. If a data object has been loaded, the data_list element in which it is
        # stored will appear as so: (data object, file name). If no data object has been loaded for an element of
        # data_list, it will contain an empty tuple ()
        data_item1 = self.data_list[0]
        data_item2 = self.data_list[1]

        # if only data 1 is loaded and it is epoched data, enable the tab
        if len(data_item1) != 0 and isinstance(data_item1[0], mne.BaseEpochs) and len(data_item2) == 0:
            self.topo_epoch_evoked_tab.setDisabled(False)

        # if both data objects are epoched, enable the tab
        elif len(data_item1) != 0 and len(data_item2) != 0 and isinstance(data_item1[0], mne.BaseEpochs) and isinstance(
                data_item2[0], mne.BaseEpochs):
            self.topo_epoch_evoked_tab.setDisabled(False)

        # if raw data as been loaded in, disable the tab
        else:
            self.topo_epoch_evoked_tab.setDisabled(True)



