
# Takes an MNE data object and process params (i.e. which channel(s) to reference to, in this case "average"), passes them to
# MNE function to make a copy of the data and reset the reference, then returns the re-referenced data
def set_reference(data, process_params):
    data_ref_to_av = data.copy().set_eeg_reference(ref_channels=process_params["ref_channels"], projection=False)
    return data_ref_to_av
