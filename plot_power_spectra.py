#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 15:12:21 2022

@author: ben
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

basedir = Path("/home/ben/sims/swift/monofonic_tests/spectra/")

#choose waveform and Lbox:
waveform = "shannon"  #DB2, DB4, DB8 or shannon
Lbox = 100.0  #only option as of now
Nres1 = 128
Nres2 = 256
k0 = 2 * 3.14159265358979323846264338327950 / Lbox
knyquist1 = Nres1 * k0
knyquist2 = Nres2 * k0
a = [0.166666, 0.333333, 0.5, 0.666666, 1.0]
scale_factor = 4       # give index of a list above

filename = basedir / f"{waveform}_{Lbox:.0f}/{waveform}_{Lbox:.0f}_a{scale_factor}_cross_spectrum"
# filename = basedir / f"{waveform}_{Lbox:.0f}/{waveform}_{Lbox:.0f}_ics_vsc_cross_spectrum" # for ICs
# savedir = Path(f"/home/ben/Pictures/swift/monofonic_tests/spectra/power_{waveform}_{Lbox:.0f}_ics_vsc") # for ICs
# plt.title(f"Power Spectra {waveform} L={Lbox:.0f} a=0.02 vsc") # for ICs

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


# Plot the power spectra:
plt.loglog(k, p1, label="P1")
plt.loglog(k, p2, label="P2")

plt.title(f"Power Spectra {waveform} L={Lbox:.0f} a={a[scale_factor]}")
savedir = Path(f"/home/ben/Pictures/swift/monofonic_tests/spectra/power_{waveform}_{Lbox:.0f}_a{scale_factor}")

plt.xlabel("k [Mpc]")
plt.ylabel("P")
plt.vlines(knyquist1, ymin=min(p1), ymax=max(p1), color="black", linestyles="dashed", label=f"{Nres1}")
plt.vlines(knyquist2, ymin=min(p2), ymax=max(p2), color="black", linestyles="dashed", label=f"{Nres2}")
plt.legend()

plt.savefig(f"{savedir}.png")




