import numpy as np
from datetime import datetime
from src import pynwb_helper


# Generate random data
rate = 10.0
np.random.seed(1234)
data_len = 1000
ephys_data = np.random.rand(data_len)
ephys_timestamps = np.arange(data_len) / rate
spatial_timestamps = ephys_timestamps[::10]
spatial_data = np.cumsum(np.random.normal(size=(2, len(spatial_timestamps))), axis=-1).T

# CreateParams
filename = "example.h5"
params = {
    'title'                     : 'the PyNWB tutorial',
    'session_description'       : 'my first synthetic recording',
    'identifier'                : 'EXAMPLE_ID',
    'session_start_time'        : datetime.now(),
    'experimenter'              : 'Dr. Bilbo Baggins',
    'lab'                       : 'Bag End Laboratory',
    'institution'               : 'University of Middle Earth at the Shire',
    'experiment_description'    : 'I went on an adventure with thirteen dwarves to reclaim vast treasures.',
    'session_id'                : 'LONELYMTN'
}

nwbfile = pynwb_helper.newfile(filename, params)

device = nwbfile.create_device(name='trodes_rig123', source="a source")

epoch_tags = ('example_epoch',)
ep1 = nwbfile.create_epoch(source='an hypothetical source', name='epoch1', start=0.0, stop=1.0,
                     tags=epoch_tags,
                     description="the first test epoch")

ep2 = nwbfile.create_epoch(source='an hypothetical source', name='epoch2', start=0.0, stop=1.0,
                     tags=epoch_tags,
                     description="the second test epoch")

pynwb_helper.writefile(nwbfile, filename)