#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 21 10:13:36 2022

@author: ben
"""

import h5py
from pathlib import Path

directory = Path(r"/home/ben/sims/swift/monofonic_tests/DB4_256_100/")
file = h5py.File(directory / "ics_DB4_256_100_nan_test_40tasks.hdf5", "r") 

# directory = Path(r"/home/ben/monofonic-experimental/")
# file = h5py.File(directory / "ics_DB4_256_100.hdf5", "r")

for key in file.keys():
    print(key) #for finding all header entries, which are:
    
Header = file["Header"]
ICs_parameters = file["ICs_parameters"]
PartType1 = file["PartType1"]
Units = file["Units"]

print(PartType1['Coordinates'][0:10])