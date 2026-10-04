# Provenance and numerical conventions

## Authority and scope

The reference is the final manuscript snapshot dated 2026-10-03, revision 3.
Manuscript SHA-256:
`5e7b69d85968cdd4e8e95a1855be29424af55d2bd9db52771ad4c63f61b85f30`.
The corresponding article PDF SHA-256 is
`320d3101df4dde0d0f022d3e1171c659945d57552f9b7c9dd21ca5d3b2392e76`.

The released numerical inputs were exported from saved production products.
They do not expose the stellar solver, private source-tree paths, research
logs, machine accounts, credentials, or old Git history. The two canonical
mode profiles were exported at the recorded background and frequencies;
no production parameter grid was rerun for this package.

`reference/input_manifest.json` checks every HDF5 input and numerical table
fixture. `reference/table_cells.json` is an independent transcription of the
active manuscript tables for comparison only; it is not used to generate
their numerical values. `reference/paper_figures/` contains the frozen
figure PDFs for visual comparison only. Their hashes and the source-product
hashes are recorded in `reference/source_provenance.json`.

## Tables I and II

Table I is recomputed from saved core/reference curves. Canonical quantities
use linear interpolation at 1.4 solar masses, without extrapolation. Nineteen
EOS support all four canonical fractions; the two RMF_m60 hyperonic models
lack a 1.4-solar-mass model at 20%. The resulting four canonical mode entries
and radius are unavailable rather than zero.

For a 1% DM-led core sequence whose endpoint lifetime exceeds 10,000 s, the
daggered table value is the highest-mass saved point with lifetime at most
10,000 s. The true endpoint frequency remains the endpoint frequency. The
stored data and Figure 3 remain uncapped. The displayed RMF_m70_L50_N F1
cap uses three significant figures: 8485.1346769 s is printed as 8490 s.
Other Table I values use the article's four-significant-figure convention.

Table II combines the archived halo structure/frequency summaries with the
certified damping catalogue. Frequencies in the original thirteen-model
summary were rounded before the common four-decimal display layout; these
published precision choices are preserved. The DD2Y F1 radius 11.485 km is
displayed using decimal half-up rounding, as 11.49 km. No underlying
numerical value is changed by these formatting conventions.

Four endpoint frequencies use the recovered/refined complex roots:
RMF_m55_L50_NY and RMF_m55_L60_NY at 1%, and RMF_m75_L40_N and
RMF_m75_L50_N at 10%. Other frequency entries retain the published
sequence/interpolation values; refined canonical QNM values are available
separately in the catalogue. The largest lifetime is printed as
`1.20 x 10^6 s`, not with unjustified extra digits.

A frequency dagger in Table II means the highest-mass resolved frequency,
not a solved frequency exactly at maximum mass. `fDMmax_evaluation_mass_Msun`
records that mass. Eleven maximum-mass geometries are cores; the halo damping
column is therefore blank for them, not a failed halo lifetime calculation.

## Table III and Figure 6

The halo accessibility study uses the stated 13-EOS subset, with 52 canonical
models. The full-sequence Roche calculation uses 1527 halo rows and 1301
companion masses: 1,986,627 pairs. These counts are recomputed from the data.
The corrected DD2Y/SLy4 inputs are retained. The raw-grid selection is not
the same as the visually retained halo frequency curves.

The formulas use `G=6.67430e-11`, `c=299792458`, and
`M_sun=1.98892e30` in SI units, a 12-km core-test companion, the circular
point-mass chirp, and the paper's 0.1 weak-response threshold. They reproduce
the contact, energy, L1, and corotating Roche diagnostics.

One NM-led maximum-mass model at companion mass 2.3 solar masses is formally
outside contact and below the energy threshold. Its recomputed
`omega*t_res ~ 4.4` and summed-radii/separation ratio `~0.956` reproduce
the article's failure of the required asymptotic scale separation. The
physical assessment is stored transparently in `validity_decisions.json`.
The package deliberately does not invent a universal numerical cutoff for
the qualitative `much greater than` / `much less than` requirements. The
Table III zero-pass conclusion is conditional on the published prescriptions.

## Figures and reproducibility limits

Figures 4-6 reuse the archived data-only plotting recipe. Figures 7-8 use
the saved normalized profiles and the archived layout. The layouts of
Figures 1-3 and 9-12 are reconstructed from saved numerical curves because
the exact final coauthor renderers were not present in the archive. Figure 9
uses shape-preserving cubic interpolation of radius against mass through
the saved points; this reconstructed plotting interpolation agrees with the
archived curve geometry to within 0.02 PDF points. No
stellar curve has been obtained by tracing or copying a finished figure.
Typography and whitespace need not be byte-identical to the original PDFs.

The halo renderer respects the original sample indices. It does not join
curves across unresolved gaps; single retained halo points are marked
explicitly. Core points on the halo-study sequences retain their geometry
flags. The cleaned published octupolar grids, not the superseded grids,
are used in Figure 12. There is no fitting that changes the saved points,
interpolation across unresolved mode gaps, or new root selection.

Only the observational **display contours** were extracted from the frozen
Figure 1. Their transformed physical coordinates reproduce the shading in
Figures 1 and 9. They are not presented as a posterior-data release and must
not be used for parameter inference. The original observational studies
remain the authoritative statistical sources; bibliography entries are in
`reference/observational_references.bib`. Attribution and rights remain with
the respective sources; no ownership of the original observational products
is claimed. See the repository's rights notice.

## Interpretation limits

Reproducing this repository demonstrates that the released data, table
selection/formatting, and plotting pipeline are internally consistent with
the frozen article. It is not an independent implementation of the full-GR
solver and does not reproduce its computation from EOS input alone. Solver
source code remains private. Radiative damping is not a detector forecast,
and the binary applicability checks do not establish general nondetectability.
