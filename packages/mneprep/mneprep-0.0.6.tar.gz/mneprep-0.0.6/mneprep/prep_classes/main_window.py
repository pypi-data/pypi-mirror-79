import os
import sys

from matplotlib import pyplot as plt
import mne
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from mneprep.io.save_data import get_valid_save_name, write_fif
from mneprep.io.load_data import get_open_file_name, read_raw

from mneprep.plot_classes.plot_window import PlotWindow
from mneprep.prep_classes.bad_ch_options import ChannelOptionsDialog
from mneprep.prep_classes.baseline_options import BaseLineOptionsDialog
from mneprep.prep_classes.epochs_options import EpochOptionsDialog
from mneprep.prep_classes.filter_options import FilterOptionsDialog
from mneprep.prep_classes.ica_options import ICAOptionsDialog
from mneprep.prep_classes.line_noise_options import LineNoiseOptionsDialog
from mneprep.prep_classes.resample_options import ResampleOptionsDialog

from mneprep.prep_functions.bad_chs import interp_bad_chs
from mneprep.prep_functions.baseline import baseline
from mneprep.prep_functions.check_channel_types import check_for_ch_type
from mneprep.prep_functions.epochs import epoch, drop_bad_epochs
from mneprep.prep_functions.filters import apply_filter, apply_notch_filter
from mneprep.prep_functions.ica import generate_ica, fit_ica_no_autoreject, \
    fit_ica_with_autoreject, reject_eog_eeg_comps, reject_comps_manual, apply_ica
from mneprep.prep_functions.pipeline_dicts import get_preset_pipeline
from mneprep.prep_functions.resample import resample_data, resample_data_and_events_func
from mneprep.prep_functions.reference import set_reference

from mneprep.popup_messages import alert_msg


class MainWindow(QMainWindow):

    def __init__(self, app):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Preprocessing Window")

        self.app = app  # provides a reference to the application within the window - used later
        # to update the GUI during long processes

        self.pipeline = [["", {}] for i in range(10)]  # list to be populated with pipeline processes

        self.create_menubar()

        self.create_cboxes_and_options_btns()

        # === create other widgets for the main window GUI ============================================

        self.fname_lbl = QLabel("Data file:")
        self.fname_lbl.setWordWrap(True)

        self.no_stim_ch_rbtn = QRadioButton("No stimulus channel")
        self.no_stim_ch_rbtn.clicked.connect(self.toggle_options)

        self.stim_ch_rbtn = QRadioButton("Select stimulus channel")
        self.stim_ch_rbtn.clicked.connect(self.toggle_options)

        self.stim_chan_select = QComboBox(self)
        self.stim_chan_select.activated[str].connect(lambda: self.get_stim_ch_and_events(self.data))
        self.stim_chan_select.setMinimumWidth(100)

        self.confirm_btn = QPushButton("Run pipeline and save results", self)
        self.confirm_btn.clicked.connect(self.run_pipeline)

        # === create/set layout for the main window GUI ==============================================

        grid_layout = QGridLayout()  # create grid layout

        # add widgets to layout
        grid_layout.addWidget(self.fname_lbl, 0, 0, 1, 2)
        grid_layout.addWidget(self.no_stim_ch_rbtn, 1, 0)
        grid_layout.addWidget(self.stim_ch_rbtn, 2, 0)
        grid_layout.addWidget(self.stim_chan_select, 2, 1)

        for i in range(10):  # add comboboxes and options buttons
            grid_layout.addWidget(self.process_cboxes[i], i + 3, 0)
            grid_layout.addWidget(self.options_btns[i], i + 3, 1)

        grid_layout.addWidget(self.confirm_btn, 14, 0)

        # set layout as central widget in main window
        widget = QWidget()
        widget.setLayout(grid_layout)
        self.setCentralWidget(widget)

        # === disable widgets relating to preprocessing to prevent pipelines being created/run before data is loaded

        self.g_pipeline_act.setDisabled(True)
        self.m_pipeline_act.setDisabled(True)
        self.l_pipeline_act.setDisabled(True)
        self.r_pipeline_act.setDisabled(True)
        self.stim_ch_rbtn.setDisabled(True)
        self.no_stim_ch_rbtn.setDisabled(True)
        self.stim_chan_select.setDisabled(True)
        for i in range(10):
            self.options_btns[i].setDisabled(True)
            self.process_cboxes[i].setDisabled(True)
        self.confirm_btn.setDisabled(True)

    def create_menubar(self):

        # create menubar
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)  # prevents menubar from acting differently in Mac OS

        # add menus to menubar
        file_menu = menubar.addMenu('&File')
        plot_menu = menubar.addMenu("&Plot")
        pipeline_menu = menubar.addMenu("&Load Pipeline")

        # create actions to add to menus: (i.e. connects menu option to appropriate function)

        # - action to open file/load in data
        open_act = QAction(QIcon('open.png'), '&Open...', self)  # create action
        open_act.triggered.connect(self.load_raw_data)  # connect to appropriate function

        # - action to download example data
        load_example_data_act = QAction("&Download MNE Sample Data", self)
        load_example_data_act.triggered.connect(self.load_mne_sample_data)

        # - action to open plot window
        plot_act = QAction('&Open Plot Window', self)
        plot_act.triggered.connect(self.plot_data)

        # - actions for loading pre-set pipelines
        self.g_pipeline_act = QAction('&Gramfort ERP Pipeline', self)
        self.g_pipeline_act.triggered.connect(lambda: self.load_preset_pipeline("gramfort"))

        self.m_pipeline_act = QAction('&Makoto ERP Pipeline', self)
        self.m_pipeline_act.triggered.connect(lambda: self.load_preset_pipeline("makoto"))

        self.l_pipeline_act = QAction('&Luck ERP Pipeline', self)
        self.l_pipeline_act.triggered.connect(lambda: self.load_preset_pipeline("luck"))

        self.r_pipeline_act = QAction('&Resting State Pipeline', self)
        self.r_pipeline_act.triggered.connect(lambda: self.load_preset_pipeline("resting"))

        # Add actions to menus
        file_menu.addAction(open_act)
        file_menu.addAction(load_example_data_act)
        plot_menu.addAction(plot_act)
        pipeline_menu.addAction(self.g_pipeline_act)
        pipeline_menu.addAction(self.m_pipeline_act)
        pipeline_menu.addAction(self.l_pipeline_act)
        pipeline_menu.addAction(self.r_pipeline_act)

    def create_cboxes_and_options_btns(self):

        # create comboboxes and options buttons
        self.options_btns = [QPushButton("Options", self) for i in range(10)]
        self.process_cboxes = [QComboBox(self) for i in range(10)]

        # list of process names to populate comboboxes with
        process_names = ["None", "Filter", "Resample", "Remove Power Line Noise",
                         "Set Reference (to Average)", "ICA",
                         "Mark Bad Channels", "Epoch", "Baseline Correct Epochs"]

        # set up comboboxes
        for i in range(10):
            self.process_cboxes[i].addItems(process_names)  # populate with process names
            self.process_cboxes[i].setMaximumWidth(200)  # set min width to ensure whole process names are visible

        # Set comboboxes so when a process is selected, the options window for that process will be opened.
        # Process is determined by getting current text from combobox
        # Pass index to open_options function to identify which number step in the pipeline is being edited
        # Note: lambda function does not store the value of each cbox, therefore each cbox must be connected to
        #       open_options individually rather than in a loop
        self.process_cboxes[0].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[0].currentText(), 0))
        self.process_cboxes[1].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[1].currentText(), 1))
        self.process_cboxes[2].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[2].currentText(), 2))
        self.process_cboxes[3].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[3].currentText(), 3))
        self.process_cboxes[4].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[4].currentText(), 4))
        self.process_cboxes[5].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[5].currentText(), 5))
        self.process_cboxes[6].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[6].currentText(), 6))
        self.process_cboxes[7].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[7].currentText(), 7))
        self.process_cboxes[8].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[8].currentText(), 8))
        self.process_cboxes[9].activated[str].connect(
            lambda: self.open_options(self.process_cboxes[9].currentText(), 9))

        # Set options buttons to the options window for the process in the combobox with corresponding index
        #   (i.e. the adjacent combobox). Process is determined by getting current text from coresponding combobox
        # Pass index to open_options function to identify which number step in the pipeline is being edited
        # Note: lambda function does not store the value of each button, therefore each button must be connected to
        #       open_options individually rather than in a loop
        self.options_btns[0].clicked.connect(lambda: self.open_options(self.process_cboxes[0].currentText(), 0))
        self.options_btns[1].clicked.connect(lambda: self.open_options(self.process_cboxes[1].currentText(), 1))
        self.options_btns[2].clicked.connect(lambda: self.open_options(self.process_cboxes[2].currentText(), 2))
        self.options_btns[3].clicked.connect(lambda: self.open_options(self.process_cboxes[3].currentText(), 3))
        self.options_btns[4].clicked.connect(lambda: self.open_options(self.process_cboxes[4].currentText(), 4))
        self.options_btns[5].clicked.connect(lambda: self.open_options(self.process_cboxes[5].currentText(), 5))
        self.options_btns[6].clicked.connect(lambda: self.open_options(self.process_cboxes[6].currentText(), 6))
        self.options_btns[7].clicked.connect(lambda: self.open_options(self.process_cboxes[7].currentText(), 7))
        self.options_btns[8].clicked.connect(lambda: self.open_options(self.process_cboxes[8].currentText(), 8))
        self.options_btns[9].clicked.connect(lambda: self.open_options(self.process_cboxes[9].currentText(), 9))

    def load_raw_data(self):

        # get path of file to load
        try:
            file_path = get_open_file_name(self)  # call function to get file name. Returns absolute file path

        except TypeError:  # thrown if a file is double clicked rather than clicked on then "open" button clicked
            alert_msg(self, "Alert", "Please select file or directory then click open, rather than double clicking")
            return

        if file_path != "":
            try:
                self.data = read_raw(file_path)  # call function to read raw data from file_path

                # set label to reflect opened file. Assuming file path is long (contains "/"), display only the
                # last part of the file path as the file name.
                if "/" in file_path:
                    fname = file_path.split("/")[-1]
                else:  # if the file path is short/does not contain "/"
                    fname = file_path
                self.fname_lbl.setText("Data File: " + fname)

                # resize the label widget dynamically to ensure it is large enough for the string
                new_size = self.fname_lbl.sizeHint()
                self.fname_lbl.setMinimumSize(new_size)

                # since data is loaded, enable radio buttons for selecting if data contains a stimulus channel or not
                self.stim_ch_rbtn.setDisabled(False)
                self.no_stim_ch_rbtn.setDisabled(False)

            except ValueError:
                QMessageBox.warning(self, "Error", "Error reading file in to MNE. Check that file contains raw data "
                                                   "only and that file type is supported")
                return

    def load_mne_sample_data(self):
        # Downloads the publicly available sample MNE dataset to a chosen directory and loads in the file
        # "sample_audvis_raw.fif".
        # Sample MNE dataset details taken from MNE documentation. Last accessed 02/08/2020.
        # https://mne.tools/stable/generated/mne.datasets.sample.data_path.html

        # open file dialog to select a directory to save the sample data set in
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        dir_name = QFileDialog.getExistingDirectory(self, "Save example data in...", "", options=options)

        if dir_name != "":  # if directory name selected
            try:
                # download sample data set
                sample_data_folder = mne.datasets.sample.data_path(dir_name)
                sample_data_raw_file = os.path.join(sample_data_folder, 'MEG', 'sample',
                                                    'sample_audvis_raw.fif')
                fileName = sample_data_raw_file

                # load sample data file
                self.data = read_raw(fileName)

                # set label to show file name
                fname = "sample_audvis_raw.fif"

                # since data is loaded, enable radio buttons for selecting if data contains a stimulus channel or not
                self.stim_ch_rbtn.setDisabled(False)
                self.no_stim_ch_rbtn.setDisabled(False)
            except ValueError:
                QMessageBox.warning(self, "Error", "Problem reading file in to MNE.")
                return

    def get_stim_ch_and_events(self, data):

        # get name of stim channel selected in GUI combobox
        stim_channel = self.stim_chan_select.currentText()
        # call MNE function to get list of events from stim channel
        data.events = mne.find_events(data, stim_channel=stim_channel)

        if len(data.events) == 0:  # if channel chosen from stim channel does not contain events
            QMessageBox.warning(self, "Error", "Selected stim channel does not contain any events")
            return

        # once events have been successfully read, make rest of GUI live so pipelines can be built and run
        for i in range(10):
            self.options_btns[i].setDisabled(False)
            self.process_cboxes[i].setDisabled(False)
        self.confirm_btn.setDisabled(False)
        self.g_pipeline_act.setDisabled(False)
        self.m_pipeline_act.setDisabled(False)
        self.l_pipeline_act.setDisabled(False)
        self.r_pipeline_act.setDisabled(False)

    def toggle_options(self):

        # Toggles disabling widgets relating to pre-processing pipelines on/off so that functionality is only available
        # if the data does not contain events, or if the data does contain events and the events have been read in.
        # This ensures events are read in (if they are required) before a pipeline can be built or run.

        if self.stim_ch_rbtn.isChecked():  # if data contains events

            # enable the combobox to select stim channel
            self.stim_chan_select.setDisabled(False)

            # populate with channel names
            self.stim_chan_select.clear()
            self.stim_chan_select.addItems(self.data.info["ch_names"])

            # disable the rest of the GUI until events are successfully loaded
            for i in range(10):
                self.options_btns[i].setDisabled(True)
                self.process_cboxes[i].setDisabled(True)
            self.confirm_btn.setDisabled(True)
            self.r_pipeline_act.setDisabled(True)

        if self.no_stim_ch_rbtn.isChecked():  # data does not contain events
            self.stim_chan_select.setDisabled(True)  # ensure combobox to select stim chan is disabled as not required
            self.data.events = []  # empty list as no events in data

            # disable ERP preset pipelines as not suitable for data without events
            self.g_pipeline_act.setDisabled(True)
            self.m_pipeline_act.setDisabled(True)
            self.l_pipeline_act.setDisabled(True)

            # make rest of GUI live so pre-processing functionality that doesnt require events can be used
            for i in range(10):
                self.options_btns[i].setDisabled(False)
                self.process_cboxes[i].setDisabled(False)
            self.confirm_btn.setDisabled(False)
            self.r_pipeline_act.setDisabled(False)  # enable resting state preset pipeline

    def open_options(self, process_str, idx):
        # gets the process currently selected in a combobox and opens the options window for that process

        # dict containing process and their corresponding options windows
        options_window_dict = {
            "Filter": FilterOptionsDialog(self, idx),
            "Resample": ResampleOptionsDialog(self, idx),
            "Mark Bad Channels": ChannelOptionsDialog(self, idx),
            "Remove Power Line Noise": LineNoiseOptionsDialog(self, idx),
            "Epoch": EpochOptionsDialog(self, idx),
            "ICA": ICAOptionsDialog(self, idx),
            "Baseline Correct Epochs": BaseLineOptionsDialog(self, idx)
        }

        if process_str == "None":
            self.pipeline[idx] = ["", {}]  # reset in case a process was chosen then reset to None
            alert_msg(self, "Options", "No options")
            return

        elif process_str == "Set Reference (to Average)":
            # No options for this process therefore no options window needed, just directly update the pipeline list
            self.pipeline[idx] = ["set_reference", {"ref_channels": "average"}]
            alert_msg(self, "Set Reference Options", "No options required for this process")
            return

        else:
            options_window = options_window_dict[process_str]  # look up the options window for the process
            options_window.show()

    def load_preset_pipeline(self, pipeline_name):
        # load in a pre-set pipeline to populate the pipeline list with, and set the GUI comboboxes so they reflect
        # the processes in the pre-set pipeline, as if the user had built the pipeline themselves.

        # populate the pipeline list using a preset pipeline
        self.pipeline = get_preset_pipeline(pipeline_name, self.data)

        # dict containing the process names and their corresponding indices in the list used to populate the GUI cboxes
        process_list_idx_lookup = {
            "": 0,  #
            "filter": 1,  #
            "resample": 2,  #
            "line_noise": 3,  #
            "set_reference": 4,  #
            "ICA": 5,
            "channels": 6,  #
            "epoch": 7,  #
            "baseline": 8  #
        }

        # update the GUI comboboxes
        for i in range(len(self.pipeline)):  # for each step in the pipeline
            process_idx = process_list_idx_lookup[self.pipeline[i][0]]  # look up process name to get its index
            self.process_cboxes[i].setCurrentIndex(process_idx)  # use the index to set the value of the cbox for that
                                                                    # step to the correct process

    def update_pipeline_process(self, idx, process, process_params):
        # set the process and params at a given index of the pipeline list
        self.pipeline[idx][0] = process
        self.pipeline[idx][1] = process_params

    def run_pipeline(self):

        # === get filename to save file once pre-processing pipeline is complete ==================================
        save_name = get_valid_save_name(self)
        if save_name == -1:  # if no valid save name
            return

        # if valid save name, continue to pre-processing

        # === Note: Updating the GUI status bar during the pipeline ===================================================
        # Because the this function currently has control rather than the Qt event loop, GUI does not update while
        # the pre-processing pipeline is running. app.processEvents is used here to work around this issue.
        # This is not the best solution (best practice would likely be to run the function in a worker thread), but is
        # used now as a placeholder throughout this function so that the functionality can be experienced.
        # Further development of this is required.

        self.statusBar().showMessage('Running pipeline...')  # set status bar text
        self.app.processEvents()  # pass control back to the main UI Qt event loop to update status bar

        # ============================================================================================================

        data = self.data.copy()  # direct copy of the raw data to be pre-processed. The data variable is overwritten
        # with the processed data after each step to minimise memory usage

        # At this point, if the data contains events, they will have been read and stored in data.events
        # Otherwise, data.events will be an empty list

        # === Run pipeline ==========================================================================================

        for i in range(len(self.pipeline)): # for each step in the pipeline

            if self.pipeline[i] != ["", {}]: # if a process has been selected for that step

                data.load_data()  # load data into RAM - needed for some of the pre-processing functions
                process_name = self.pipeline[i][0]
                process_params = self.pipeline[i][1]

                if process_name == "filter":

                    self.statusBar().showMessage('Applying filter...')  # update GUI status bar
                    self.app.processEvents()

                    data_filtered = apply_filter(data, process_params)  # call function to carry out the filtering

                    data = data_filtered  # overwrite data variable
                    del data_filtered  # delete to free up RAM

                    print("filtering finished \n")  # console output to follow pipeline progress in console

                elif process_name == "resample":
                    self.statusBar().showMessage('Resampling...')  # update GUI status bar
                    self.app.processEvents()

                    if len(data.events) == 0:  # no events/stim channel, therefore only resample data
                        data_resampled = resample_data(data, process_params) # call function to carry out the resampling

                    else:  # events need to be resampled as well as data
                        # call function to carry resample data and events
                        data_resampled, events_resampled = resample_data_and_events_func(data, process_params)
                        data_resampled.events = events_resampled  # overwrite/update existing events

                    data = data_resampled  # overwrite data variable
                    del data_resampled  # delete to free up RAM

                    print("resampling finished \n")  # console output to follow pipeline progress in console

                elif process_name == "line_noise":

                    self.statusBar().showMessage('Removing line noise...')  # update GUI status bar
                    self.app.processEvents()

                    if isinstance(data, mne.io.BaseRaw): # check data type is raw (notch filter can only be applied to raw data)
                        data_notched = apply_notch_filter(data, process_params)  # call function to carry out the notch filtering

                        data = data_notched  # overwrite data variable
                        del data_notched  # delete to free up RAM

                        print("notch filter finished \n")  # console output to follow pipeline progress in console

                    else:
                        QMessageBox.warning(self, "Error", "Notch filter can only be applied to raw data")
                        self.statusBar().showMessage("")  # clear status bar since exiting pipeline
                        return

                elif process_name == "set_reference":

                    self.statusBar().showMessage('Setting EEG reference...')  # update GUI status bar
                    self.app.processEvents()

                    if check_for_ch_type(data, ["EEG"]):  # check that data contains EEG channels

                        data_ref_to_av = set_reference(data, process_params)  # call function to set reference channel

                        data = data_ref_to_av  # overwrite data varable
                        del data_ref_to_av  # delete to free up RAM

                        print("set reference finished \n")  # console output to follow pipeline progress in console

                    else:
                        QMessageBox.warning(self, "Error", "No EEG channels found")
                        self.statusBar().showMessage("")  # clear status bar since exiting pipeline
                        return

                elif process_name == "channels":

                    # This function uses mne's interactive time series plot to mark bad channels.
                    # Channels marked as bad in the plot are automatically included in data.info["bads"],
                    # which is mne's way of recording/marking bad channels for a data object

                    self.statusBar().showMessage('Marking bad channels...')  # update GUI status bar
                    self.app.processEvents()

                    fig = data.plot()  # plot interactive time series of data to select bad channels from
                    fig.subplots_adjust(top=0.9) # format plot to set informative title
                    plt.suptitle("1) Click on a channel to mark it as bad. \n" 
                                 "2) To continue, exit this plot", fontsize=12)

                    # pause pipeline for selection of bad channels until plot window is exited
                    while plt.fignum_exists(fig.number):
                        plt.pause(0.1)

                    if process_params["interpolate"]:  # if interpolating bad channels

                        self.statusBar().showMessage('Interpolating bad channels...')  # update GUI status bar
                        self.app.processEvents()

                        data_bads_interp = interp_bad_chs(data)  # call function to interpolate bad channels

                        data = data_bads_interp  # overwrite data variable
                        del data_bads_interp  # delete to free up RAM

                        print("Bad channels interpolation finished \n")  # console output to follow pipeline progress in console

                    else: # if bad channels marked but not interpolated
                        print("Bad channels marked \n")  # console output to follow pipeline progress in console

                elif process_name == "epoch":

                    if isinstance(data, mne.io.BaseRaw): # check data type is raw - only raw data can be epoched

                        if process_params["autoreject"]: # if dropping bad epochs using Autoreject (automated)

                            self.statusBar().showMessage('Epoching (and dropping bad epochs)...')  # update GUI status bar
                            self.app.processEvents()

                            # call function to create epochs, dropping bad epochs in the process
                            epochs_drop_bad = drop_bad_epochs(data, process_params)

                            data = epochs_drop_bad  # overwrite data variable
                            del epochs_drop_bad  # delete to free up RAM

                        else:  # if not dropping bad epochs

                            self.statusBar().showMessage('Epoching...') # update GUI status bar
                            self.app.processEvents()

                            # call function to create epochs without dropping bad epochs in the process
                            epochs = epoch(data, process_params)

                            data = epochs  # overwrite data variable
                            del epochs  # delete to free up RAM

                        print("Epoching finished \n") # console output to follow pipeline progress in console

                    else:
                        QMessageBox.warning(self, "Error", "Epoching can only be applied to raw data")
                        self.statusBar().showMessage("")  # clear status bar since exiting pipeline
                        return

                elif process_name == "baseline":

                    self.statusBar().showMessage('Applying baseline...') # update GUI status bar
                    self.app.processEvents()

                    try:
                        epochs_baselined = baseline(data, process_params) # call function to apply baseline

                    except ValueError as VE:  # if baseline interval is outside of epoch interval limits
                        QMessageBox.warning(self, "Error", str(VE)) #  messagebox displays ValueError message
                        self.statusBar().showMessage("")  # clear status bar since exiting pipeline
                        return

                    except AttributeError as AE:  # if data type is other than epoch or evoked (i.e. raw)
                        QMessageBox.warning(self, "Error", "Baseline can only be applied to epoched or evoked data")
                        self.statusBar().showMessage("")  # clear status bar since exiting pipeline
                        return

                    data = epochs_baselined  # overwrite data variable
                    del epochs_baselined  # delete to free up RAM

                    print("Baselining finished \n")  # console output to follow pipeline progress in console

                elif process_name == "ICA":

                    self.statusBar().showMessage('Performing ICA (may take a while)...')  # update GUI status bar
                    self.app.processEvents()

                    if isinstance(data, mne.io.BaseRaw) or isinstance(data, mne.BaseEpochs):

                        # 1) --- generate ICA ----------------------------------------------
                        self.statusBar().showMessage('Generating ICA (may take a while)...') # update GUI status bar
                        self.app.processEvents()

                        self.ica = generate_ica(data, process_params, self)  # call function to generate ICA

                        # 2) --- fit ICA ---------------------------------------------------
                        self.statusBar().showMessage('Fitting ICA (may take a while)...') # update GUI status bar
                        self.app.processEvents()

                        if process_params["autoreject"]:
                            fit_ica_with_autoreject(self.ica, data)  # call function to fit ICA using Autoreject to
                                                                     # create a rejetion threshold for bad data segments
                        else:
                            fit_ica_no_autoreject(self.ica, data)  # call function to fit ICA

                        # 3) --- exclude components -----------------------------------------
                        self.statusBar().showMessage('Excluding components (may take a while)...') # update GUI status bar
                        self.app.processEvents()

                        if process_params["rejection_method"] == "ecg_eog": # if automated rejection of ocular and cardiac artifacts
                            # check that EOG and ECG/MEG channels are present in data
                            if check_for_ch_type(data, ["ECG", "EOG"]) \
                                    or check_for_ch_type(data, ["MAG", "EOG"]) \
                                    or check_for_ch_type(data, ["GRAD", "EOG"]):
                                reject_eog_eeg_comps(self.ica, data)  # call function for automated rejection of components
                            else:
                                QMessageBox.warning(self, "Automated Rejection Error",
                                                    "EOG and/or ECG channels not found. Defaulting to manual rejection")
                                reject_comps_manual(self.ica, data)  # call function for manual rejection of components

                        else:  # if manual selection of ICA components to exclude
                            reject_comps_manual(self.ica, data)  # call function for manual rejection of components

                        # 4) --- apply ICA ---------------------------------------------------
                        self.statusBar().showMessage('Applying ICA...') # update GUI status bar
                        self.app.processEvents()

                        reconst_data = apply_ica(self.ica, data)  # call function to apply ICA to data

                        # 5) --- save results -------------------------------------------------
                        data = reconst_data  # overwrite data variable
                        del reconst_data  # delete to free up RAM

                        print("ICA finished \n")  # console output to follow pipeline progress in console

                    else:
                        QMessageBox.warning(self, "Error",
                                            "ICA is currently only available for raw or epoched data types.")
                        self.statusBar().showMessage("")  # clear status bar since exiting pipeline
                        return

        # === Save results ==========================================================================================

        try:
            self.statusBar().showMessage('Saving...')  # update GUI status bar
            print("Saving...")  # console output to follow pipeline progress in console

            write_fif(data, save_name)  # call function to save data
            alert_msg(self, "Pipeline Successful", "Pipeline run and data saved successfully")

        except Exception:  # no specific exception for now as not sure what exceptions could be raised here
            alert_msg(self, "Save Unsuccessful", "Problem saving data")  # console output to follow pipeline progress in console

        finally:
            self.statusBar().clearMessage()  # clear the status bar now that the pipeline has finished

    def plot_data(self):
        # open the plot window containing the visualisation functionality
        plot_dialog = PlotWindow()
        plot_dialog.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow(app)
    main_window.show()
    sys.exit(app.exec_())
