import pynwb
from pynwb.form.backends.hdf5 import HDF5IO
from pynwb.ecephys import ElectrodeTable, ElectrodeTableRegion, ElectricalSeries
from pynwb.behavior import SpatialSeries


# Create a new .nwb file
def newfile(params):
    f = pynwb.NWBFile(
        params['title'],
        params['session_description'],
        params['identifier'],
        params['session_start_time'],
        experimenter=params['experimenter'],
        lab=params['lab'],
        institution=params['institution'],
        experiment_description=params['experiment_description'],
        session_id=params['session_id'])

    return f


def writefile(nwbfile, filename):
    io = HDF5IO(filename, manager=pynwb.get_manager(), mode='w')
    io.write(nwbfile)
    io.close()

def readfile(filename):
    io = HDF5IO(filename, manager=pynwb.get_manager(), mode='r')
    nwbfile = io.read()
    io.close()
    return nwbfile


def getprojectparams(nwbfile):
    params = {}
    params['name'] = 'aaaaaa'
    params['session_description'] = nwbfile.session_description
    params['identifier'] = nwbfile.identifier
    params['experimenter'] = nwbfile.experimenter
    params['lab'] = nwbfile.lab
    params['institution'] = nwbfile.institution
    params['experiment_description'] = nwbfile.experiment_description
    params['session_id'] = nwbfile.session_id
    params['session_start_time'] = nwbfile.session_start_time
    return params


def create_device(nwbfile, param):
    return nwbfile.create_device(name=param["name"], source=param["source"])


def create_electrode_group(nwbfile, param, device):
    return nwbfile.create_electrode_group(param["electrode_name"],
                                               source=param["source"],
                                               description=param["description"],
                                               location=param["location"],
                                               device=device)

def create_electrode_table(param):
    return ElectrodeTable(param["name"])


def add_electrode(param, electrode_group, electrode_table):
    electrode_table.add_row(param["id"],
                            x=param["x"],
                            y=param["y"],
                            z=param["z"],
                            imp=param["impedance"],
                            location=param["location"],
                            filtering=param["filtering"],
                            description=param["description"],
                            group=electrode_group)

def create_electrode_table_region(param, electrode_table, region):
    return ElectrodeTableRegion(electrode_table, region, param["description"])


def create_electrical_series(nwbfile, param, ephys_data, ephys_timestamps, electrode_table_region, epoch_list):
    ephys_ts = ElectricalSeries(param["name"],
                                param["source"],
                                ephys_data,
                                electrode_table_region,
                                timestamps=ephys_timestamps,
                                # Alternatively, could specify starting_time and rate as follows
                                # starting_time=ephys_timestamps[0],
                                # rate=rate,
                                resolution=param["resolution"],
                                comments=param["comments"],
                                description=param["description"])
    nwbfile.add_acquisition(ephys_ts, epoch_list)
    return ephys_ts


def create_spatial_series(nwbfile, param, spatial_data, spatial_timestamps, epoch_list):
    spatial_ts = SpatialSeries(param["name"],
                               param["source"],
                               spatial_data,
                               param["reference_frame"],
                               timestamps=spatial_timestamps,
                               resolution=param["resolution"],
                               comments=param["comments"],
                               description=param["description"])
    nwbfile.add_acquisition(spatial_ts, epoch_list)
    return spatial_ts
