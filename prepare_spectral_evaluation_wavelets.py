#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:00:49 2022

@author: ben
"""

from sys import argv
from pathlib import Path
from write_spectra_jobs import write_spectra_jobs
from directories import monofonic_tests_basedir

def main(scale_factor: int, Nres1: int, Nres2: int, Lbox: float, waveforms: list):
    a = [0.166666, 0.333333, 0.5, 0.666666, 1.0]
    print(f"Chose scale factor a = {a[scale_factor]} (index {scale_factor} / {len(a) - 1})")
    
    for wave in waveforms:
        write_spectra_jobs(scale_factor, Nres1, Nres2, Lbox, wave, 
            output_basedir=monofonic_tests_basedir / "spectra/")
    
    
    
    
if __name__ == "__main__":
    if argv[5] == "all":
        waveforms = ["DB2", "DB4", "DB6", "DB8", "DB10", "shannon"]
    else:
        waveforms = argv[5:len(argv)]
        
    assert len(waveforms) <= 6
    
    scale_factor = int(argv[1])
    Nres1 = int(argv[2])
    Nres2 = int(argv[3])
    Lbox = float(argv[4])
    
    main(
        scale_factor=scale_factor,
        Nres1=Nres1,
        Nres2=Nres2,
        Lbox=Lbox,
        waveforms=waveforms
        )

