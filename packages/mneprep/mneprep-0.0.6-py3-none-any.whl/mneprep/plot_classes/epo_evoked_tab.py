from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

import mne

from matplotlib import pyplot as plt


class TopoEpochsEvokedTab(QWidget):

    def __init__(self, plot_window):
        super(TopoEpochsEvokedTab, self).__init__()

        self.plot_window = plot_window  # provides a reference to the plot window to access plot window attributes
        # (data_list) and method (get_data_updated_chs)

        # === create widgets for the tab GUI ====================================================================

        # combobox in which to select event ID - epochs containing events with this ID will be plotted
        self.event_select = QComboBox()
        self.event_select_lbl1 = QLabel("Select event ID")
        self.event_select_lbl2 = QLabel("Only epochs/evoked responses containing this event \nwill be plotted")

        # bold font to use for titles:
        bold_font = QFont()
        bold_font.setBold(True)

        # button to generate/show epochs image plot, and labels describing plot/giving info
        self.plot_epochs_title_lbl = QLabel("Epochs Image Map")
        self.plot_epochs_title_lbl.setFont(bold_font)
        self.plot_epochs_info_lbl = QLabel("A topographical map showing one image for each sensor.\n"
                                           "Each image shows all the epochs for that sensor, with each\n"
                                           "row of pixels representing a single epoch and colour scale\n"
                                           "respresenting the signal value at each time point.")
        self.plot_epochs_btn = QPushButton("Plot epoch images")
        self.plot_epochs_btn.clicked.connect(self.plot_epochs)

        # button to generate/show evoked responses plot, and labels describing plot/giving info
        self.plot_evoked_title_lbl = QLabel("Evoked Responses Map")
        self.plot_evoked_title_lbl.setFont(bold_font)
        self.plot_evoked_info_lbl = QLabel("A topographical map showing one image for each sensor.\n"
                                           "Each image shows the evoked response at that sensor.\n"
                                           "If two data files have been loaded,their equivalent\n"
                                           "evoked responses are compared on each plot.\n"
                                           "Note: plotting with 'All channels' or 'MEG only' selected\n "
                                           "will plot MEG channels. Select 'EEG only' to plot EEG channels")
        self.plot_evoked_btn = QPushButton("Plot evoked responses")
        self.plot_evoked_btn.clicked.connect(self.plot_evoked)

        # === create/set layout for tab GUI ======================================================================

        layout = QGridLayout()
        layout.addWidget(self.event_select_lbl1, 0, 0)
        layout.addWidget(self.event_select, 0, 1, Qt.AlignLeft)
        layout.addWidget(self.event_select_lbl2, 1, 0, 1, 2)
        layout.addWidget(self.plot_epochs_title_lbl, 2, 0, 1, 2)
        layout.addWidget(self.plot_epochs_info_lbl, 3, 0, 1, 2)
        layout.addWidget(self.plot_epochs_btn, 4, 0, 1, 2)
        layout.addWidget(self.plot_evoked_title_lbl, 5, 0, 1, 2)
        layout.addWidget(self.plot_evoked_info_lbl, 6, 0, 1, 2)
        layout.addWidget(self.plot_evoked_btn, 7, 0, 1, 2)
        self.setLayout(layout)

    def populate_events_cbox(self, id_lst):
        self.event_select.clear() # clear/reset events combobox
        self.event_select.addItems(id_lst) # populate with the parameter id_list (a list of all event IDs present in the data)

    def plot_epochs(self):

        # check that the first data file has been loaded in (so that there is definitely data to plot)
        if len(self.plot_window.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        else:

            try:
                event_id = self.event_select.currentText()  # get the event ID to be plotted

                # get data to be plotted ( i.e. data with updated/selected channels)
                self.plot_data_list = self.plot_window.get_data_updated_chs()

                # Plot topographical epochs images for each data object in self.plot_data_list.
                # Plots separate figures for the channel types "eeg", "mag" and "grad" in each data object (if present)

                for i in range(len(self.plot_data_list)):  # for each data object to be plotted...
                    plot_data = self.plot_data_list[i]  # get data to be plotted
                    data_name = self.plot_window.data_list[i][1]  # get file name for data to be plotted

                    if "mag" in plot_data:
                        layout = mne.channels.find_layout(plot_data.info, ch_type='mag')  # get mag ch layout/locations

                        # create informative plot window title - data file name, channel type and event ID
                        title = data_name + ": Magnetometers, Event ID: " + event_id

                        # Call MNE function to plot epochs image. Don't show figure initially so if there are
                        # multiple figures, they can be shown simultaneously once they have all been generated.
                        fig = plot_data[event_id].plot_topo_image(layout=layout, fig_facecolor='w',
                                                               font_color='k', sigma=1, title=title, show=False)
                        fig.canvas.set_window_title(data_name)  # set informative plot window title

                    if "grad" in plot_data:
                        layout = mne.channels.find_layout(plot_data.info, ch_type='grad')
                        title = data_name + ": Gradiometers, Event ID: " + event_id
                        fig = plot_data[event_id].plot_topo_image(layout=layout, fig_facecolor='w',
                                                              font_color='k', sigma=1, title=title, show=False)
                        fig.canvas.set_window_title(data_name)

                    if "eeg" in plot_data:
                        layout = mne.channels.find_layout(plot_data.info, ch_type='eeg')
                        title = data_name + ": Electrodes, Event ID: " + event_id
                        fig = plot_data[event_id].plot_topo_image(layout=layout, fig_facecolor='w',
                                                              font_color='k', sigma=1, title=title, show=False)
                        fig.canvas.set_window_title(data_name)

                plt.show()  # show figure(s)

            except KeyError: # if event_id is not present in file/data 1 but not file/data 2
                QMessageBox.warning(self, "Event Error", "Selected event is not present in both data files")
                return

            except ValueError:  # if channel type present in file/data 1 but not file/data 2
                QMessageBox.warning(self, "Channel Error", "Selected channels not present in both data files")
                self.plot_window.select_chs_cbox.setCurrentIndex(0)  # reset to "all channels"
                return

    def plot_evoked(self):

        # check that the first data file has been loaded in (so that there is definitely data to plot)
        if len(self.plot_window.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        else:
            event_id = self.event_select.currentText()  # get the event ID to be plotted
            evokeds = []  # empty list - populate with evoked data to plot

            try:
                # get data to be plotted ( i.e. data with updated/selected channels)
                self.plot_data_list = self.plot_window.get_data_updated_chs()

                for i in range(len(self.plot_data_list)):  # for each data object to be plotted...
                    plot_data = self.plot_data_list[i]  # get data to be plotted
                    data_name = self.plot_window.data_list[i][1]  # get file name for data to be plotted

                    # create a list of all event IDs present in the data
                    event_dict = plot_data.event_id
                    data_ids = [i for i in event_dict.keys()]

                    # Check if the event ID selected to be plotted is present in the data. If so, generate the evoked
                    # response for that event ID and add it to the evokeds list

                    if event_id in data_ids: # if event ID present in the data
                        evoked = plot_data[event_id].average()  # average epochs with that event ID to create an evoked response
                        evoked.comment = data_name + " - Event ID " + event_id  # set the evoked response's label/name
                        evokeds.append(evoked)  # add to evokeds list

                    else:  # if event_id is not present in file/data 1 but not file/data 2
                        QMessageBox.warning(self, "Event Error", "Selected event is not present in both data files")
                        return

                mne.viz.plot_evoked_topo(evokeds)

            except ValueError:  # if channel type present in file/data 1 but not file/data 2
                QMessageBox.warning(self, "Channel Error", "Selected channels not present in both data files")
                return



