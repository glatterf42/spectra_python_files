#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 12:04:15 2022

@author: ben

This currently only evaluates the last snapshot.
"""

from sys import argv
from pathlib import Path
from directories import spectra_basedir, monofonic_tests_basedir, agora_test_basedir
import os 
import stat

def write_spectra_jobs(scale_factor: int, Nres1: int, Nres2: int, Lbox: float, form: str, output_basedir: Path):
    Nres_max = max(Nres1, Nres2)
    input_dir_1 = str(monofonic_tests_basedir) + f"/{form}_{Nres1}_{Lbox:.0f}"
    input_dir_2 = str(monofonic_tests_basedir) + f"/{form}_{Nres2}_{Lbox:.0f}" 
    output_dir = output_basedir / f"{form}_{Lbox:.0f}"
    output_dir_string = str(output_dir)
    if output_dir.exists():
        print(output_dir, "already exists. Skipping...")
    else:
        print("creating", output_dir)
        output_dir.mkdir()
    
    
    script = f"""#!/bin/bash
set -u

{spectra_basedir}/build/spectra --format=3 --output={output_dir_string}/{form}_{Lbox:.0f}_a{scale_factor} --ngrid={2 * Nres_max} --input={input_dir_1}/output_000{scale_factor}.hdf5 --input={input_dir_2}/output_000{scale_factor}.hdf5
    """
    
    filename = output_dir / "generate_final_spectra.sh"
    with (filename).open("w") as f:
        f.write(script)

    permissions = os.stat(filename)
    os.chmod(filename, permissions.st_mode | stat.S_IEXEC)



def write_spectra_jobs_agora(scale_factor: int, Nres1: int, Nres2: int, output_basedir: Path):
    Nres_max = max(Nres1, Nres2)
    input_dir = str(agora_test_basedir) 
    output_dir = output_basedir
    output_dir_string = str(output_dir)
    if output_dir.exists():
        print(output_dir, "already exists. Skipping...")
    else:
        print("creating", output_dir)
        output_dir.mkdir()
    
    script = f"""#!/bin/bash
set -u

{spectra_basedir}/build/spectra --format=3 --output={output_dir_string}/agora_a{scale_factor} --ngrid={2 * Nres_max} --input={input_dir}/output_000{scale_factor}.hdf5 --input={input_dir}/output_000{scale_factor}.hdf5
    """
    
    filename = output_dir / "generate_final_spectra.sh"
    with (filename).open("w") as f:
        f.write(script)

    permissions = os.stat(filename)
    os.chmod(filename, permissions.st_mode | stat.S_IEXEC)
    

    
if __name__ == "__main__": 
    if argv[5] == "all":
        waveforms = ["DB2", "DB4", "DB6", "DB8", "DB10", "shannon"]
    else:
        waveforms = argv[5:len(argv)]
        
    assert len(waveforms) <= 6
    
    for form in waveforms:
        write_spectra_jobs(
            scale_factor = int(argv[1]),
            Nres1 = int(argv[2]),
            Nres2 = int(argv[3]),
            Lbox = float(argv[4]),
            form = form,
            output_dir = monofonic_tests_basedir / "spectra/"
            )    