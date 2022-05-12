#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 15:12:21 2022

@author: ben
"""

from matplotlib import scale
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import scipy.special as sf
import numpy as np

def Dplus( lambda0, a ):
	return a * np.sqrt(1.0+lambda0*a**3) * sf.hyp2f1(3.0/2.0, 5.0/6.0, 11.0/6.0, -lambda0 * a**3 )

basedir = Path("/home/ben/sims/swiftsim/examples/agora/")
# basedir = Path("/home/ben/sims/gadget4/examples/agora_test/output/spectra/")

#choose waveform and Lbox:
Lbox = 85.47 # 60 #only option as of now
Nres1 = 512
# Nres2 = 256
k0 = 2 * 3.14159265358979323846264338327950 / Lbox
knyquist1 = Nres1 * k0
# knyquist2 = Nres2 * k0
# #This is for 128 particles with fewer output times
# times = [0.01, 0.02, 0.04, 0.08, 0.166666, 0.333333, 0.5, 0.666666, 1.0]
# times = [0.01, 0.02, 0.04, 0.08, 0.1]
# times = [0.01, 0.02]
# scale_factor = 0       # give index of a list above

#This is for 512 particles with more output times:
time_file = basedir / 'snap_times_agora1024'
df_times = pd.read_csv(f'{time_file}.txt', sep='  ', skipinitialspace=True, header=0, engine='python')

output_numbers = [0, 1, 2, 4, 8, 16, 32]
redshifts = df_times.loc[output_numbers]


Omega_m  = 0.272
Omega_L  = 0.728
lambda_0 = Omega_L / Omega_m

# print(Dplus(lambda_0, 1.0))

#find columns in file manually
#is k really in Mpc? Swift doesn't use /h internally at least.
columns = ["k [Mpc]", "Pcross", "P1", "err. P1", "P2", "err. P2", "P2-1", "err. P2-1", "modes in bin"]

zstart = 100 # 99.09174098173423
a_ics = 1 / (1 + zstart)
filename_ics = basedir / f'spectra/{Lbox}mpc_{Nres1}/agora_ics_cross_spectrum'

# #just as a test for normalising wrt to the first snapshot
# zstart = 12.0
# a_ics = 1 / (1 + zstart)
# filename_ics = basedir / f'spectra/{Lbox}mpc_{Nres1}/agora_0000_cross_spectrum'

# filename_ics = basedir / 'agora_a0_cross_spectrum'
df_ics = pd.read_csv(f'{filename_ics}.txt', sep=' ', skipinitialspace=True, header=None, names=columns, skiprows=1)
#only consider rows above resolution limit
df_ics = df_ics[df_ics['k [Mpc]'] >= k0]
k_ics = df_ics['k [Mpc]']
p1_ics = df_ics['P1']
Dplus0 = Dplus(lambda0=lambda_0, a=a_ics)
D_squared_ics = Dplus0 ** 2
p1_ics_noramlised = p1_ics / D_squared_ics

print(D_squared_ics)

# p1_ics_ic_normalised = p1_ics_noramlised / p1_ics_noramlised 
# plt.loglog(k_ics, p1_ics_ic_normalised, label='ICs')

# #This is for 128 particles with fewer output times:
# for scale_factor in range(len(times)):
#     filename = basedir / f"{Lbox}mpc/agora_a{scale_factor}_cross_spectrum"
    # filename = basedir / f"agora_a{scale_factor}_small_dt_cross_spectrum"
    # filename = basedir / f'agora_a{scale_factor}_cross_spectrum'
# filename = basedir / f"{waveform}_{Lbox:.0f}/{waveform}_{Lbox:.0f}_ics_vsc_cross_spectrum" # for ICs
# savedir = Path(f"/home/ben/Pictures/swift/monofonic_tests/spectra/power_{waveform}_{Lbox:.0f}_ics_vsc") # for ICs
# plt.title(f"Power Spectra {waveform} L={Lbox:.0f} a=0.02 vsc") # for ICs

#This is for 512 particles with more output times:
for k in range(len(output_numbers)):
    output_number = output_numbers[k]
    redshift = float(redshifts.loc[output_number])
    scale_factor = 1 / (1 + redshift)
    filename = basedir / f'spectra/{Lbox}mpc_{Nres1}/agora_{output_number:04d}_cross_spectrum'

    df = pd.read_csv(f"{filename}.txt", sep=" ", skipinitialspace=True, header=None, names=columns, skiprows=1)

    #only consider rows above resolution limit
    df = df[df["k [Mpc]"] >= k0]

    k = df["k [Mpc]"]
    p1 = df["P1"]
    p1_error = df["err. P1"]

    # p2 = df["P2"]
    # p2_error = df["err. P2"]
    # pcross = df["Pcross"]

    # D_squared = Dplus(lambda0=lambda_0, a=times[scale_factor]) ** 2
    D_squared = Dplus(lambda0=lambda_0, a=scale_factor) ** 2

    p1_normalised = p1 / D_squared
    p1_ic_normalised = p1_normalised / p1_ics_noramlised

    print(D_squared)

    # Plot the power spectra:
    # plt.loglog(k, p1_ic_normalised, label=f"{times[scale_factor]}")
    plt.loglog(k, p1_ic_normalised, label=f"{scale_factor}")
    # plt.loglog(k, p2, label="P2")

plt.title(f"Power Spectra Agora {Nres1}")
savedir = Path(f"/home/ben/Pictures/swift/agora/spectra/{Lbox}mpc_{Nres1}")

plt.xlabel(r"k [$\mathrm{Mpc}^{-1}$]")
plt.ylabel("P")
plt.vlines(knyquist1, ymin=min(p1_ic_normalised), ymax=max(p1_ic_normalised), color="black", linestyles="dashed", label=f"k_ny {Nres1}")
# plt.vlines(knyquist2, ymin=min(p2), ymax=max(p2), color="black", linestyles="dashed", label=f"{Nres2}")
plt.legend()
# plt.ylim(1, 3)

plt.savefig(f"{savedir}/agora_{Nres1}_power.png")

plt.show()




