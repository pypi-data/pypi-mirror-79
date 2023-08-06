from PyQt5.QtWidgets import *
from matplotlib import pyplot as plt


class PSDTab(QWidget):

    def __init__(self, plot_window):
        super(PSDTab, self).__init__()

        self.plot_window = plot_window # provides a reference to the plot window to access plot window attributes
        # (data_list) and method (get_data_updated_chs)

        # === create widgets for the tab GUI ====================================================================

        self.average_check = QCheckBox("Plot average of channels")

        self.plot_btn = QPushButton("Plot power spectral density")
        self.plot_btn.clicked.connect(self.plot)

        # === create/set layout for tab GUI ======================================================================

        layout = QVBoxLayout()
        layout.addWidget(self.average_check)
        layout.addWidget(self.plot_btn)
        self.setLayout(layout)

    def plot(self):

        # check that the first data file has been loaded in (so that there is definitely data to plot)
        if len(self.plot_window.data_list[0]) == 0:  # if the first data file has not been loaded
            QMessageBox.warning(self, "File 1 Required", "Ensure a data file has been selected for File 1")
            return

        else:

            average = self.average_check.isChecked()  # True if plotting average, False if plotting individual channels

            try:
                # get data to be plotted ( i.e. data with updated/selected channels)
                self.plot_data_list = self.plot_window.get_data_updated_chs()

                # plot psd for data in self.plot_data_list
                for i in range(len(self.plot_data_list)):  # for each data object to be plotted...
                    plot_data = self.plot_data_list[i]  # get data to be plotted
                    data_name = self.plot_window.data_list[i][1]  # get file name for data to be plotted
                    # Call MNE function to plot psd of data. Don't show figure initally so if there are multiple
                    # figures, they can be shown simultaneously once they have both been generated.
                    fig = plot_data.plot_psd(show=False, average=average)
                    fig.canvas.set_window_title(data_name)  # set data file name as plot window title

                plt.show()  # show figure(s)

            except ValueError:  # if channel type present in file/data 1 but not file/data 2
                QMessageBox.warning(self, "Channel Error", "Selected channels not present in both data files")
                self.plot_window.select_chs_cbox.setCurrentIndex(0)  # reset to "all channels"
                return

