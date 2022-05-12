#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 01 14:57:45 2022

@author: ben
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np

basedir = Path("/home/ben/sims/data_swift/monofonic_tests/spectra/")

#choose Nres and Lbox:
waveforms = ['DB2', "DB4", "DB8", "shannon"]  #DB2, DB4, DB8, shannon are all we have right now
Lbox = 100.0  #only option as of now
Nres1 = 128      #Nres1 should always be smaller than Nres2
Nres2 = 256      #128, 256 and 512 exist for now
Nres3 = 512
k0 = 2 * 3.14159265358979323846264338327950 / Lbox
knyquist = Nres3 * k0   #Not used at the moment anyway except for upper limit, for which we need the larger Nres
a = [0.166666, 0.333333, 0.5, 0.666666, 1.0]
scale_factor = 4       # give index of a list above


def get_pcross_values(waveform: str, Lbox: float, Nres1: int, Nres2: int, scale_factor: int):
    # filename = basedir / f"{waveform}_{Lbox:.0f}/{wave}_{Lbox:.0f}_a{scale_factor}_{Nres1}_{Nres2}_cross_spectrum"
    filename = basedir / f"{wave}_{Lbox:.0f}/{wave}_{Lbox:.0f}_ics_{Nres1}_{Nres2}_cross_spectrum" # for ICs
    
    #find columns in file manually
    #is k really in Mpc? Swift doesn't use /h internally at least.
    columns = ["k [Mpc]", "Pcross", "P1", "err. P1", "P2", "err. P2", "P2-1", "err. P2-1", "modes in bin"]
    
    df = pd.read_csv(f"{filename}.txt", sep=" ", skipinitialspace=True, header=None, names=columns, skiprows=1)
    
    #only consider rows above resolution limit
    df = df[df["k [Mpc]"] >= k0]
    
    k = df["k [Mpc]"]
    pcross = df["Pcross"]
    
    return k, pcross


for i, wave in enumerate(waveforms):
    k_128_256, pcross_128_256 = get_pcross_values(wave, Lbox, Nres1, Nres2, scale_factor)
    k_128_512, pcross_128_512 = get_pcross_values(wave, Lbox, Nres1, Nres3, scale_factor)
    k_256_512, pcross_256_512 = get_pcross_values(wave, Lbox, Nres2, Nres3, scale_factor)


    # Plot the Cross Correlation:
    plt.plot(k_128_256, pcross_128_256, label=f'{wave} {Nres1} {Nres2}', linestyle=':', color=f'C{i}')
    plt.plot(k_128_512, pcross_128_512, label=f"{wave} {Nres1} {Nres3}", linestyle='--', color=f'C{i}')
    plt.plot(k_256_512, pcross_256_512, label=f'{wave} {Nres2} {Nres3}', linestyle='-', color=f'C{i}')

# savedir = Path(f"/home/ben/Pictures/swift/monofonic_tests/spectra/cross_{Nres1}_{Nres2}_{Lbox:.0f}_ics_local") # for ICs
# plt.title(f"Cross correlation N=({Nres1}, {Nres2}) L={Lbox:.0f} a=0.02") # for ICs

savedir = Path(f"/home/ben/Pictures/swift/monofonic_tests/spectra/cross_comparison_{Lbox:.0f}_a{scale_factor}")
plt.title(f"Cross correlation comparison L={Lbox:.0f} a={a[scale_factor]}")

plt.xscale("log")
plt.xlabel(r"k [$\mathrm{Mpc}^{-1}$]")
plt.ylabel("C = Pcross")
plt.ylim(0.8, 1.0)
plt.xlim(k_128_512[0], knyquist)
# plt.vlines(knyquist, ymin=min(p1), ymax=max(p1), color="black", linestyles="dashed", label=f"{Nres}")
plt.legend()

plt.savefig(f"{savedir}.png")
plt.show()
