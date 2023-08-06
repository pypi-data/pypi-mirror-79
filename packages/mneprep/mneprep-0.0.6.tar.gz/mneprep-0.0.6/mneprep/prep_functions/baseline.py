

# Takes an MNE Epochs data object and process params (i.e. the time interval to apply baseline correction), passes them
# to MNE function to make a copy of the data and apply the baseline to it, then returns the baselined data
def baseline(data, process_params):
    epochs_baselined = data.copy().apply_baseline(process_params["interval"])
    return epochs_baselined
