# Takes an MNE data object and process params (i.e. the high and low frequency cutoffs of the filter and the
# filtering method - FIR or IIR), passes them to MNE function to create a copy of the data
# and apply the filter to it, then returns the filtered data

def apply_filter(data, process_params):
    data_filtered = data.copy().filter(l_freq=process_params["l_freq"],
                                       h_freq=process_params["h_freq"],
                                       method=process_params["method"])
    return data_filtered


# Takes an MNE Raw data object and process params (i.e. the frequency(s) at which to apply a notch filter)
# passes them to MNE function to create a copy of the data and apply the notch filter(s) to it, then returns the
# filtered data.
# The frequencies parameter can include one or more integer values, and works with or without commas for single values
# e.g. (50), (50,), are both fine. If including multiple frequencies eg due to line noise harmonics, must be informat (50, 100)

def apply_notch_filter(data, process_params):
        data_notched = data.copy().notch_filter(freqs=process_params["freqs"])
        return data_notched

