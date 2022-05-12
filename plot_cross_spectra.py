#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 15:12:21 2022

@author: ben
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

basedir = Path("/home/ben/sims/data_swift/monofonic_tests/spectra/")

#choose Nres and Lbox:
waveforms = ['DB2', "DB4", "DB8", "shannon"]  #DB2, DB4, DB8, shannon are all we have right now
Lbox = 100.0  #only option as of now
Nres1 = 128      #Nres1 should always be smaller than Nres2
Nres2 = 256      #128, 256 and 512 exist for now
k0 = 2 * 3.14159265358979323846264338327950 / Lbox
knyquist = Nres2 * k0   #Not used at the moment anyway except for upper limit, for which we need the larger Nres
a = [0.166666, 0.333333, 0.5, 0.666666, 1.0]
scale_factor = 4       # give index of a list above


for wave in waveforms:
    # filename = basedir / f"{wave}_{Lbox:.0f}/{wave}_{Lbox:.0f}_a{scale_factor}_{Nres1}_{Nres2}_cross_spectrum"
    filename = basedir / f"{wave}_{Lbox:.0f}/{wave}_{Lbox:.0f}_ics_{Nres1}_{Nres2}_cross_spectrum" # for ICs
    
    #find columns in file manually
    #is k really in Mpc? Swift doesn't use /h internally at least.
    columns = ["k [Mpc]", "Pcross", "P1", "err. P1", "P2", "err. P2", "P2-1", "err. P2-1", "modes in bin"]
    
    df = pd.read_csv(f"{filename}.txt", sep=" ", skipinitialspace=True, header=None, names=columns, skiprows=1)
    
    #only consider rows above resolution limit
    df = df[df["k [Mpc]"] >= k0]
    
    k = df["k [Mpc]"]
    p1 = df["P1"]
    p1_error = df["err. P1"]
    p2 = df["P2"]
    p2_error = df["err. P2"]
    pcross = df["Pcross"]
    
    
    # Plot the Cross Correlation:
    plt.plot(k, pcross, label=f"{wave}")

savedir = Path(f"/home/ben/Pictures/swift/monofonic_tests/spectra/cross_{Nres1}_{Nres2}_{Lbox:.0f}_ics") # for ICs
plt.title(f"Cross correlation N=({Nres1}, {Nres2}) L={Lbox:.0f} a=0.02") # for ICs

# savedir = Path(f"/home/ben/Pictures/swift/monofonic_tests/spectra/cross_{Nres1}_{Nres2}_{Lbox:.0f}_a{scale_factor}")
# plt.title(f"Cross correlation N=({Nres1}, {Nres2}) L={Lbox:.0f} a={a[scale_factor]}")

plt.xscale("log")
plt.xlabel(r"k [$\mathrm{Mpc}^{-1}$]")
plt.ylabel("C = Pcross")
plt.ylim(0.8, 1.0)
plt.xlim(k[0], knyquist)
# plt.vlines(knyquist, ymin=min(p1), ymax=max(p1), color="black", linestyles="dashed", label=f"{Nres}")
plt.legend()

plt.savefig(f"{savedir}.png")




