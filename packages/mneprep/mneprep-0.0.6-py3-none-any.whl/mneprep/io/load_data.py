import os
from pathlib import Path

import mne
from PyQt5.QtWidgets import *

# === Code to Open Either File or Directory =================================================================

# subclass of QFileDialog to allow opening of either a file or a directory
# Code for this class taken from StackOverflow, Luke's answer (05/07/11)
# https://stackoverflow.com/questions/6484793/multiple-files-and-folder-selection-in-a-qfiledialog?noredirect=1&lq=1
# Accessed 27/07/20

class OpenFileOrDirDialog(QFileDialog):

    def __init__(self,*args):
        QFileDialog.__init__(self,*args)
        self.setOptions(QFileDialog.DontUseNativeDialog)
        self.setFileMode(QFileDialog.ExistingFile) # use QFileDialog.ExstingFiles if wanting to open multiple files/dirs
        buttons = self.findChildren(QPushButton)
        for button in buttons:
            if 'open' in str(button.text()).lower():
                self.openFileButton=button
        self.openFileButton.clicked.disconnect()
        self.openFileButton.clicked.connect(self.openClicked)
        self.tree= self.findChild(QTreeView)

    def openClicked(self):

        inds = self.tree.selectionModel().selectedIndexes()
        files = []
        for i in inds:
            if i.column()==0:
                files.append(os.path.join(str(self.directory().absolutePath()),str(i.data())))
        self.selectedFiles = files
        self.hide()


    def filesSelected(self):
        return self.selectedFiles[0]

# --- end of referenced code ---------------------------------------------------------------


def get_open_file_name(main_window):
    open_file_dialog = OpenFileOrDirDialog(main_window, "Open...") # creates an instance of the  file&dir QFileDialog
    open_file_dialog.exec_()  # opens it from the main window
    fpath = open_file_dialog.filesSelected()  # gets the file path of the file to read in
    return fpath


# === Code to Read Raw Data from Supported File Formats ==================================================

# Following code (supported dict and read_raw function) taken/modified from MNELAB source code (mnelab/io.readers.py)
# Authors: Clemens Brunner <clemens.brunner@gmail.com>
# License: BSD (3-clause)
# https://github.com/cbrnr/mnelab/blob/master/mnelab/io/readers.py Last Accessed 10/09/20

# dict of (some of) MNE's supported file formats with corresponding MNE read functions
supported = {".edf": mne.io.read_raw_edf,
             ".bdf": mne.io.read_raw_bdf,
             ".gdf": mne.io.read_raw_gdf,
             ".vhdr": mne.io.read_raw_brainvision,
             ".fif": mne.io.read_raw_fif,
             ".fif.gz": mne.io.read_raw_fif,
             ".set": mne.io.read_raw_eeglab,
             ".cnt": mne.io.read_raw_cnt,
             ".mff": mne.io.read_raw_egi,
             ".nxe": mne.io.read_raw_eximia,
             ".ds": mne.io.read_raw_ctf} # added as most CUBRIC users use .ds format


def read_raw(fname, *args, **kwargs):
    # This function supports reading raw data from different file formats.
    # The dict "supported" is used to dispatch the appropriate read function for a supported file type.
    # Parameter - fname(string): File name to load.
    # Returns - Raw object.

    ext = "".join(Path(fname).suffixes)
    if ext in supported:
        return supported[ext](fname, *args, **kwargs)


