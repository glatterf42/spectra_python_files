#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:00:49 2022

@author: ben
"""

from sys import argv
from pathlib import Path
from write_spectra_jobs import write_spectra_jobs_agora
from directories import monofonic_tests_basedir, agora_test_basedir

def main(scale_factor: int, Nres1: int, Nres2: int):
    a = [0.166666, 0.333333, 0.5, 0.666666, 1.0]
    print(f"Chose scale factor a = {a[scale_factor]} (index {scale_factor} / {len(a) - 1})")
    
    write_spectra_jobs_agora(scale_factor, Nres1, Nres2, 
        output_basedir=agora_test_basedir / "spectra/")
    
    
    
    
if __name__ == "__main__":    
    scale_factor = int(argv[1])
    Nres1 = int(argv[2])
    Nres2 = int(argv[3])
    
    main(
        scale_factor=scale_factor,
        Nres1=Nres1,
        Nres2=Nres2
        )

