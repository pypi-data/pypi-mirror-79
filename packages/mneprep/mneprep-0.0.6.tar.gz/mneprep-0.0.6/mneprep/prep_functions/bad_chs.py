
# Passes an MNE data object to MNE function to make a copy of the data and interpolate the bad channels, then returns
# copy of the data with the channels interpolated
def interp_bad_chs(data):
    print("Channels to interpolate: ", data.info["bads"]) # console output to follow pipeline progress in console
    data_bads_interp = data.copy().interpolate_bads(reset_bads=True, verbose=True) # channels no longer marked as bad
    # once they have been interpolated, ie data_bads_interp.info["bads"] is now an empty list.
    return data_bads_interp
