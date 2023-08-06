import mne


def get_preset_pipeline(pipeline_name, data):
    # This function takes a name of a pre-set pipeline and returns a list containing the processes and parameters for
    # that pre-set pipeline, which is used to replace/repopulate main_window.pipeline.

    # num_chs is the number of data channels in the data
    # used for the pipelines that require number of ICA components to be determined by number of channels instead of
    # variance explained.
    picks = mne.pick_types(data.info, meg=True, eeg=True, eog=False, ecg=False)
    num_chs = len(picks)

    # === lists containing the processes and parameters for the preset pipelines ====================================

    gramfort_pipeline = [["", {}],  # Empty step at the start for optional step to be applied before pipeline is run
                         ["filter", {"l_freq": 0, "h_freq": 40, "method": "fir"}],
                         ["channels", {"interpolate": True}],
                         ["ICA", {"n_comps": 0.99,
                                  "ica_method": "fastica",
                                  "extended": False,
                                  "autoreject": True,
                                  "rejection_method": "ecg_eog"}],
                         ["epoch", {"tmin": -0.2, "tmax": 0.5, "tstep": None, "autoreject": True}],
                         ["baseline", {"interval": (-0.2, 0)}],
                         ["", {}],
                         ["", {}],
                         ["", {}],
                         ["", {}]
                         ]

    makoto_pipeline = [["filter", {"l_freq": 1, "h_freq": None, "method": "fir"}],
                       ["resample", {"sfreq": 250}],
                       ["channels", {"interpolate": True}],
                       ["set_reference", {"ref_channels": "average"}],
                       ["line_noise", {"freqs": (50), "method": "fir"}],
                       ["epoch", {"tmin": -0.2, "tmax": 0.5, "tstep": None, "autoreject": True}],
                       ["ICA", {"n_comps": num_chs,
                                "ica_method": "infomax",
                                "extended": False,
                                "autoreject": False,
                                "rejection_method": "manual"}],
                       ["", {}],
                       ["", {}],
                       ["", {}]
                       ]

    luck_pipeline = [["", {}],  # Empty step at the start for optional step to be applied before pipeline is run
                     ["filter", {"l_freq": 0.1, "h_freq": None, "method": "fir"}],
                     ["line_noise", {"freqs": (50), "method": "fir"}],
                     ["channels", {"interpolate": True}],
                     ["ICA", {"n_comps": num_chs,
                              "ica_method": "fastica",
                              "extended": False,
                              "autoreject": False,
                              "rejection_method": "manual"}],
                     ["set_reference", {"ref_channels": "average"}],
                     ["epoch", {"tmin": -0.2, "tmax": 0.5, "tstep": None, "autoreject": True}],
                     ["baseline", {"interval": (-0.2, 0)}],
                     ["", {}],
                     ["", {}]
                     ]

    resting_state_pipeline = [["filter", {"l_freq": 1, "h_freq": 100, "method": "iir"}],
                              ["line_noise", {"freqs": (50, 100), "method": "iir"}],
                              ["ICA", {"n_comps": num_chs,
                                       "ica_method": "fastica",
                                       "extended": False,
                                       "autoreject": False,
                                       "rejection_method": "manual"}],
                              ["resample", {"sfreq": 256}],
                              ["epoch", {"tmin": None, "tmax": None, "tstep": 30, "autoreject": True}],
                              ["", {}],
                              ["", {}],
                              ["", {}],
                              ["", {}],
                              ["", {}]
                              ]

    # === logic to return the correct preset pipeline list ===========================================================

    if pipeline_name == "gramfort":
        return gramfort_pipeline
    if pipeline_name == "makoto":
        return makoto_pipeline
    elif pipeline_name == "luck":
        return luck_pipeline
    elif pipeline_name == "resting":
        return resting_state_pipeline
