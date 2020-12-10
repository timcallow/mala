'''
Collects / calculates SNAP descriptors and LDOS data from a DFT calculation.
Uses LAMMPS, so make sure it is available.
'''
from .handler_base import handler_base
import numpy as np

class handler_qeout_cube(handler_base):
    """Data handler for qe.out and ldos.cube files."""
    def __init__(self, p, descriptor_calculator, target_parser):
        super(handler_qeout_cube,self).__init__(p)
        self.fingerprint_length = 0
        self.descriptor_calculator = descriptor_calculator
        self.target_parser = target_parser

    def add_snapshot(self, qe_out_file, qe_out_directory, cube_naming_scheme, cube_directory):
        """Adds a snapshot to data handler. For this type of data,
        a QuantumEspresso outfile, an outfile from the LDOS calculation and
        a directory containing the cube files"""
        self.parameters.snapshot_directories_list.append([qe_out_file, qe_out_directory, cube_naming_scheme, cube_directory])

    def load_data(self):
        """Loads data and transforms it into SNAP/LDOS data on the grid.
        At the end of this function we have two pytorch tensors holding the input and the output data."""

        # Load from every snapshot directory.
        for snapshot in self.parameters.snapshot_directories_list:
            ##############
            # Input data.
            # Calculate the SNAP descriptors from the QE calculation.
            ##############

            # print("Calculating descriptors for snapshot ", snapshot[0], "at ", snapshot[1])
            # print(np.shape(self.descriptor_calculator.calculate_from_qe_out(snapshot[0], snapshot[1])))

            ##############
            # Output data.
            # Read the LDOS data.
            ##############

            print("Reading targets for snapshot ", snapshot[2], "at ", snapshot[3])
            self.target_parser.read_from_cube(snapshot[2], snapshot[3])


            # Here, raw_input only contains the file name given by ASE and the dimensions of the grd.
            # These are the input parameters we need for LAMMPS.
            # self.raw_input.append(self.get_atoms_from_qe(self.parameters.directory+sub))





    # def prepare_data(self):
    #     """Cuts input/output data into training, validation and test set.
    #     then adds the training, validation and test data to pytorch datahandlers
    #     to be used by the network."""



    def get_input_dimension(self):
        if (self.descriptor_calculator.fingerprint_length != 0):
            return self.descriptor_calculator.fingerprint_length
        else:
            raise Exception("No descriptors were calculated, cannot give input dimension.")

    def get_output_dimension(self):
        if (self.parameters.ldos_gridsize != 0):
            return self.target_parser.target_length
        else:
            raise Exception("No targets were read, cannot give output dimension.")


if __name__ == "__main__":
    raise Exception(
        "data_snap_ldos.py - test of basic functions not yet implemented.")