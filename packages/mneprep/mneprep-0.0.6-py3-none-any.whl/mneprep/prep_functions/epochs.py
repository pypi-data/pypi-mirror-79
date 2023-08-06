import mne
from autoreject import get_rejection_threshold

# This function takes an MNE Raw data object and process params, passes them to MNE Epochs class constructor to create
# epochs from the data, then returns the epochs. If events are present in the data, these are epoched around. The epochs
# are then returned.
# If no events present in data, fixes-length events are created and epoched around to create fixed-length epochs
# Process params:
#   tmin: start time for epoch interval if epoching around events. If no events present in data, tmin should be None
#   tmax: end time for epoch interval if epoching around events. If no events present in data, tmax should be None
#   tstep: duration of epoch interval if creating fixed length events as no events present in data. If epoching around
#          events, tstep should be None

def epoch(data, process_params):
    if len(data.events) != 0: # events in data, epoch around these
        epochs = mne.Epochs(data, events=data.events, tmin=process_params["tmin"], tmax=process_params["tmax"])
    else: # no events in data
        events = mne.make_fixed_length_events(data, duration=process_params["tstep"])
        epochs = mne.Epochs(data, events=events, tmin=0.0, tmax=process_params["tstep"], baseline=(0, 0))
    return epochs


# This function takes an MNE Epochs data object, uses the Autoreject package to create a threshold for rejection of
# bad epochs, then creates epochs in the same way as in the epoch function above, but passes the thresholds to the MNE
# epoch class constructor so that bad epochs are dropped during the epoch creation process. The epochs (with the bad
# epochs dropped) are then returned

def drop_bad_epochs(data, process_params):

    include = []
    picks = mne.pick_types(data.info, meg=True, eeg=True, stim=False,
                           eog=True, include=include, exclude='bads')

    if len(data.events) != 0: # events in data

        # Create recommended epochs from which to find global rejection thresholds as advised in the autoreject docs
        # (Note that detrending is applied and bads are excluded)
        # http://autoreject.github.io/auto_examples/plot_estimate_global_reject.html#sphx-glr-auto-examples-plot-estimate-global-reject-py
        # Last accessed 10/09/20
        threshold_epochs = mne.Epochs(data, events=data.events, tmin=process_params["tmin"],
                                      tmax=process_params["tmax"],
                                      picks=picks, baseline=(None, 0), preload=True,
                                      reject=None, verbose=True, detrend=1)

        # create actual epochs, from which the bad epochs will be dropped later
        epochs = mne.Epochs(data, events=data.events, tmin=process_params["tmin"], tmax=process_params["tmax"])


    else: # no events in data

        # create fixed-length events in order to create epochs
        events = mne.make_fixed_length_events(data, duration=process_params["tstep"])

        # Create recommended epochs from which to find global rejection thresholds as advised in the autoreject docs
        threshold_epochs = mne.Epochs(data, events=events, tmin=0.0,
                                      tmax=process_params["tstep"],
                                      picks=picks, baseline=(0, 0), preload=True,
                                      reject=None, verbose=True, detrend=1)

        # create actual epochs, from which the bad epochs will be dropped later
        epochs = mne.Epochs(data, events=events, tmin=0.0, tmax=process_params["tstep"], baseline=(0, 0))

    # At this stage, for both data with and without events two sets of epochs have been created- a recommended set
    # from which to get a rejection threshold, and an actual set from which bad epochs will be dropped

    # get rejection thresholds based on recommended epochs (bad channels excluded)
    reject = get_rejection_threshold(threshold_epochs)  # removed decim=2 as RuntimeWarning: could cause aliasing artifacts

    # apply rejection thresholds to actual epochs to drop bad epochs
    epochs_drop_bad = epochs.copy().drop_bad(reject=reject)

    return epochs_drop_bad
