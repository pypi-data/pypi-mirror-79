import mne
import re

from PyQt5.QtWidgets import *

def get_valid_save_name(main_window):
    # This function opens a file dialog for the selection of a file name/path at which to save the results of a
    # pipeline. It checks if the file name/path is valid, and if so, returns it. Otherwise, returns -1

    # get file name/path to save file under from file dialog
    options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog
    fpath, _ = QFileDialog.getSaveFileName(main_window, "Save As...", "", "", options=options)

    # validate file name
    if fpath:
        fname = fpath.split("/")[-1]  # file name will be the last section of the file path

        # check for invalid characters (file name should contain alphanumeric characters and underscores only)
        invalid_char = re.findall(r"[\W\s]", fname)
        if len(invalid_char) > 0:
            QMessageBox.warning(main_window, "Invalid File Name", "Files names should only include letters, "
                                                                  "digits, and underscores")
            return -1

        else:
            return fpath

def write_fif(data, fpath):
    # This function adds an appropriate extension to the save file name depending on the data type, in accordance with
    # the MNE file naming conventions. It then uses an MNE function to save the data to file.

    if isinstance(data, mne.io.BaseRaw):
        save_fname = fpath + "-raw.fif"
        data.save(save_fname)

    elif isinstance(data, mne.BaseEpochs):
        save_fname = fpath + "-epo.fif"
        data.save(save_fname)
