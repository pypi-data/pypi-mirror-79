import mne
from PyQt5.QtWidgets import QMessageBox
from autoreject import get_rejection_threshold
from matplotlib import pyplot as plt


def generate_ica(data, process_params, parent_window):
    # This function takes an MNE data object (Raw or Epochs) and generates an ICA solution object for that data using
    # MNE's ICA class constructor. A check is performed to ensure that the ICA is not instructed to generate a greater
    # number of components than the rank of the data, to avoid artifacts from incorrect data dimensionality. The ICA
    # object is then returned

    # console output to follow pipeline progress in console
    print("\n------------------GENERATING ICA ---------------\n")

    # === check num of components/max_pca_components ===============================================================

    # Set max_pca_components to the lesser value of either the process param "n_comps" or the rank of the data,
    # to avoid artifacts from incorrect data dimensionality

    n_components = process_params["n_comps"]

    # get dict containing rank of each channel type
    data_rank_dict = mne.compute_rank(data, info=data.info, verbose=False)

    # calculate overall rank of data
    data_rank = sum(data_rank_dict.values())

    # set maximum number of components (i.e. the number of principal components from the PCA step that are retained
    # for signal reconstruction later) to the rank of the data
    max_pca_components = data_rank

    # check if n_comps is not greater than data rank, if so, set n_comps equal to data rank
    if n_components > data_rank:
        QMessageBox.warning(parent_window, "Updating Number of Components",
                            "Number of components is greater than rank of data. Calculated rank (" + str(data_rank)
                            + ") will be used as number of components instead")
        n_components = data_rank

    print("n components: ", n_components)  # console output to follow pipeline progress in console

    # === generate ICA==========================================================================================
    method = process_params["ica_method"]
    fit_params = None
    if process_params["extended"]:
        fit_params = {"extended": True}
    ica = mne.preprocessing.ICA(n_components=n_components, max_pca_components=max_pca_components, random_state=97,
                                method=method, fit_params=fit_params)
    return ica


def fit_ica_with_autoreject(ica, data):
    # This function uses autoreject to create global rejection thresholds for the data and uses it to reject bad data
    # segments/epochs (depending on data type) before ICA is fitted to the data.
    # see autoreject docs for details: https://autoreject.github.io/faq.html

    # console output to follow pipeline progress in console
    print("\n------------------FITTING ICA WITH AUTOREJECT---------------\n")

    # if data is Raw, create epochs in order to generate autoreject rejection thresholds
    if isinstance(data, mne.io.BaseRaw):
        # Autoreject only works on epoched data, so these steps are needed for raw data:
        # see autoreject docs for details: https://autoreject.github.io/faq.html
        tstep = 1.0
        events = mne.make_fixed_length_events(data, duration=tstep)
        epochs = mne.Epochs(data, events=events, tmin=0.0, tmax=tstep, baseline=(0, 0))
        reject = get_rejection_threshold(epochs)

        ica.fit(epochs, reject=reject, tstep=tstep) # fit ICA (with rejection thresholds) to data (all data channels)

    elif isinstance(data, mne.BaseEpochs):
        # drop bad channels to calculate rejection thresholds from good channels only
        epochs_no_bads = data.copy().drop_channels(data.info["bads"])
        # get rejection thresholds
        reject = get_rejection_threshold(epochs_no_bads)
        # fit ICA (with rejection thresholds) to data (all data channels)
        ica.fit(data, reject=reject)


def fit_ica_no_autoreject(ica, data):
    # console output to follow pipeline progress in console
    print("\n------------------FITTING ICA ---------------\n")

    # fit ica to data with no rejection thresholds
    reject = None
    ica.fit(data, reject=reject)


def reject_eog_eeg_comps(ica, data):
    # This function uses MNE functions to remove ocular and cardiac artifacts from the data by identifying and excluding
    # ICA components that are related to EOG and ECG channels (if present)

    # console output to follow pipeline progress in console
    print("\n------------------ REJECTING ECG AND EOG COMPONENTS ---------------\n")

    # Select and remove components that match the EOG and ECG channels (i.e. ocular and cardiac artifact removal)
    ica.exclude = []
    eog_indices, eog_scores = ica.find_bads_eog(data)  # find which ICs match the EOG pattern
    ecg_indices, ecg_scores = ica.find_bads_ecg(data, method='correlation')  # find which ICs match the ECG pattern

    # exclude the identified components
    ica.exclude += eog_indices
    ica.exclude += ecg_indices

    print("ica.exclude= ", ica.exclude)  # console output to follow pipeline progress in console


def reject_comps_manual(ica, data):
    # This function uses mne's interactive ica sources plot for manual selection of components to exclude.
    # Components selected in the plot are automatically included in the ica.exclude list,
    # which is mne's way of recording ICA components to be excluded.

    # console output to follow pipeline progress in console
    print("\n------------------ REJECTING COMPONENTS MANUALLY ------------------\n")

    # plot interactive time series of components in which to select components for exclusion
    fig = ica.plot_sources(data)

    # format plot to set informative title
    fig.subplots_adjust(top=0.9)
    plt.suptitle("1) Select components to be removed by clicking on their time series. \n"
                 "Clicking on the name of each component will show its topographic plot. \n"
                 "2) To continue, exit this plot", fontsize=12)

    # pause pipeline for selection of components to exclude until plot window is exited
    while plt.fignum_exists(fig.number):
        plt.pause(0.1)


def apply_ica(ica, data):
    # This function uses an MNE function to make a copy of the data and reconstruct it by applying the ICA.
    # Components included in the ica.exclude list are excluded from the reconstruction.
    # The reconstructed data is then returned.

    # console output to follow pipeline progress in console
    print("\n------------------ APPLYING ICA ---------------\n")

    reconst_data = data.copy()
    ica.apply(reconst_data)
    return reconst_data
