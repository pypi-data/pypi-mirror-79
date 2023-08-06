
from mne.io.pick import get_channel_type_constants, channel_type

# Takes an MNE object data and a list of required channel types eg ["MEG", "ECG"]
# Returns True if all specified channel types are present in the data object
# Otherwise returns False

def check_for_ch_type(data, required_chs):

    # get all possible MNE channel types
    all_channel_types = [key.upper() for key in get_channel_type_constants().keys()]

    # create a list of all channel types that exist in data
    ch_types_in_data = []
    for index, ch in enumerate(data.info["chs"]):
        ch_type = channel_type(data.info, index).upper()
        if ch_type not in ch_types_in_data:
            ch_types_in_data.append(ch_type)

    # if all specified channel types are present in the list:
    if all(ch_type in all_channel_types for ch_type in required_chs):
        return True
    else:
        return False