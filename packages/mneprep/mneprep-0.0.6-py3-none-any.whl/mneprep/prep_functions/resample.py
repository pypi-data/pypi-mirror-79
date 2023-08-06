
# Takes an MNE data object and process params (i.e. new sampling frequency), passes them to MNE function to create a copy of the data
# and resample it, then returns the resampled data
def resample_data(data, process_params):
    data_resampled = data.copy().resample(sfreq=process_params["sfreq"])
    return data_resampled

# Takes an MNE data object data and process params (i.e. new sampling frequency), passes them to MNE function to create a copy of the data
# and resample the data and the events, then returns the resampled data and events
def resample_data_and_events_func(data, process_params):
    data_resampled, events_resampled = data.copy().resample(sfreq=process_params["sfreq"], events=data.events)
    return data_resampled, events_resampled

