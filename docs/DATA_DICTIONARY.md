# Data dictionary

Masses are gravitational masses in solar-mass units; radii are in km.
Frequencies named `f` are in kHz unless explicitly labelled Hz. Radiative
amplitude-damping times are in seconds. `F1`, `F5`, `F10`, and `F20` mean
dark-matter mass fractions 0.01, 0.05, 0.10, and 0.20.

## `core_sequences.h5`

Twenty-one EOS groups. Each contains:

- `pure_nm/{M,R,f,tau}`: pure normal-matter reference, not an effective
  one-fluid dark-matter model.
- `F*/structure/{M,R}`: equilibrium sequence; `R` is the NM outer radius.
- `F*/NM/{M,f,tau}` and `F*/DM/{M,f,tau}`: mode-specific mass grids and
  full-GR quadrupolar results.

Data retain the saved sequence precision and order. The figure display
starts at 0.5 solar masses. A sub-0.5-mass ordering reversal in the saved
EOS6 F10 DM grid is retained; it is not used in the displayed range or the
canonical interpolation. No damping-time cap is applied to the stored curves.

## `halo_sequences.h5`

Each EOS has pure-NM radius and frequency references plus four fraction groups.

- `mr/{M,R,halo,source_index}`: `R` is always the dark-component radius;
  it is the outer radius only when `halo=1`.
- `frequency/{M,f,halo,source_index}`: retained DM-led mode points.
- Attributes `Mmax`, `RDMmax`, `RDM1p4`, `fDM1p4`, `fDMmax`,
  `fDMmax_mass`, `fDMmax_capped`, `config_at_Mmax`: equilibrium summary
  and original endpoint-frequency selection. The table renderer applies
  the four certified recovered/refined endpoint frequencies from `halo_modes.h5`.

`source_index` is the original sequence index. Nonconsecutive indices must
not be joined across an unresolved gap. A single retained halo point is
plotted as a filled circle. Crosses mark core geometries, not failed modes.

## `halo_modes.h5`

168 target groups: 21 EOS times four fractions times two targets.
`target=M1p4` or `Mmax`; metadata identify EOS, fraction, geometry, and
certification. There are 157 certified halo modes and 11 nonhalo endpoints.

Numerical fields, where available:

- `f_QNM_Hz`, `tau_GW_s`: outgoing-wave QNM frequency and radiative lifetime.
- `omega_real_per_m`, `omega_imag_per_m`: complex frequency components
  in inverse metres, with time dependence `exp(i omega t)`.
- `M_Msun`, `R_NM_km`, `R_DM_km`: refined target background.
- `raw_M_Msun`, `raw_R_NM_km`, `raw_R_DM_km`, `f_seed_kHz`:
  original sequence/interpolation values; these are not silently replaced
  by the refined target values when reproducing the published table.
- `n_DM`, `n_NM`: radial displacement node counts.
- `amplitude_ratio_NM_to_DM`: relative displacement peak amplitude.
- `R_Q`: `abs(Q_N+Q_D)/(abs(Q_N)+abs(Q_D))`.
- `complex128_*_relative`, `spatial_*_relative`: stored fractional
  cross-implementation/refinement differences where available.
- `tau_overlap_s`, `tau_overlap_over_qnm`: leading-quadrupole diagnostic,
  distinct from the full-GR QNM lifetime.

The code checks `f = c Re(omega)/(2 pi)` and
`tau = 1/(c Im(omega))` with `c=299792458 m/s`. Missing fields remain
missing; no nonhalo damping time is invented.

## `self_coupling.h5`

EOS1, boson mass 500 MeV; groups `0.5pi`, `pi`, `1.5pi`, `2pi` give
lambda. Each fraction contains `branch` (equilibrium `M,R_NM,R_DM`) and
`NM`, `DM` mode arrays (`M,f,tau`, and associated fields where saved).
An empty DM branch is an unresolved/absent saved sequence, not a zero mode.

## `higher_multipoles.h5`

Cleaned published EOS1 octupolar (`ell=3`) grids, grouped by fraction and
NM/DM branch. Arrays are `M` and `f`. Quadrupolar comparison curves come
from `core_sequences.h5`. No `ell=4` claim is made by this release.

## Representative eigenfunctions

`eigenfunctions_0501.h5` contains the radial grid, four displacement
profiles, component radii, frequencies, mass, fraction, and node counts.
Each fluid was normalized independently to its own signed extremum. Plotted
peak heights therefore do not measure relative fluid amplitudes. One unused
terminal guard sample from the saved displacement arrays is not exported.

`eigenfunctions_1400.h5` contains separate NM and DM radial supports and
the two mode groups. `WI,WO,VI,VO` denote inner/outer displacements;
`H0,H1,K` are shared metric amplitudes. Within each W, V, or metric panel
group a common signed maximum is used. The profiles are evaluated at the
real-frequency estimates used by the published figure, not a new parameter scan.

## `accessibility.h5`

`halo_grid` is a 1527-row matrix with named columns in its attribute:
EOS index, fraction percent, M, R_NM, R_DM, predicted frequency,
retained raw DM frequency, and halo flag. EOS index refers to the stored
13-model list. Selection: raw halo flag positive and DM frequency positive,
without a mass cut or truncation at maximum mass. This is deliberately
different from the plotted retained-curve sample. The companion grid has
1301 uniformly spaced masses from 1.0 to 2.3 solar masses.

## `observational_display.h5`

Archived display paths in physical `(radius_km, mass_Msun)` coordinates,
with path codes, colour, opacity, and outline width. Extracted only from the
observational shading of the frozen mass-radius figure. These paths reproduce
the displayed regions; they contain neither posterior weights nor independent
information about confidence calibration. Do not use them as a likelihood
or as substitutes for the cited original observational data.
