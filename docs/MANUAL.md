# Reproduction manual

## 1. Requirements

Use Linux and Python 3.11 or 3.12 with `venv` and `pip`. The supported entry
point is Bash. Windows users can use WSL; native Windows and macOS have not
been certified in this candidate. Leave at least 1 GB free for the archive,
isolated environment, package downloads, and output. The released numerical
data are under 10 MB; no large solver cache is required.

The package uses NumPy, SciPy, h5py, and Matplotlib. `requirements.lock` also pins
their plotting and parsing dependencies. Fonts are supplied by Matplotlib;
there is no dependence on a system TeX installation or proprietary fonts.

## 2. First run

Extract the archive into a new directory. Do not overlay it on an existing
research project. From the extracted directory run:

```bash
bash reproduce.sh
```

If a different Python executable is needed:

```bash
PYTHON=python3.12 bash reproduce.sh
```

The command checks Python, creates `.venv` if absent, installs the locked
packages from the configured package index, verifies the SHA-256 input
manifest, regenerates the tables and figures, and writes the verification
report. An error exits with a nonzero status; do not interpret partial
outputs from a failed run as a verified release.

## 3. Subsequent and offline runs

After the dependencies have been installed, no network is needed:

```bash
.venv/bin/python -m reproduction
.venv/bin/python -m reproduction --verify-only
.venv/bin/python -m unittest discover -s tests -v
```

The first command rebuilds outputs; the second checks the existing complete
output and numerical references; the third runs regression tests.

To keep an earlier output directory intact:

```bash
.venv/bin/python -m reproduction --output output_comparison
```

Only the selected output directory and local software/cache directories are
written. Input HDF5 files are opened read-only. Never edit an input file to
silence a failed integrity check.

## 4. Output map

| Paper figure | Generated file | Input |
| --- | --- | --- |
| 1 | `core_MR.pdf` | core sequences and observational display contours |
| 2 | `core_freq.pdf` | core frequency sequences |
| 3 | `core_tau.pdf` | uncapped core damping curves |
| 4 | `halo_mass.pdf` | halo-study mass-radius curves |
| 5 | `halo_frequency.pdf` | retained halo/core frequency points |
| 6 | `resonance_access.pdf` | 52 canonical halo radius-frequency pairs |
| 7 | `fig01_core_eigenfunctions.pdf` | representative 0.501-solar-mass profiles |
| 8 | `fig02_core_edge.pdf` | representative 1.4-solar-mass profiles |
| 9 | `MR_lam.pdf` | EOS1 self-coupling scan |
| 10 | `freq_mass_lam.pdf` | EOS1 self-coupling frequency scan |
| 11 | `tau_mass_lam.pdf` | EOS1 self-coupling damping scan |
| 12 | `higher_l_modes.pdf` | EOS1 quadrupolar and octupolar frequencies |

The generated table files are `table1_core`, `table2_halo`, and
`table3_accessibility`, each in JSON and LaTeX. JSON preserves numerical
precision, column names, and flags; unavailable values are `null`. LaTeX
files contain rows for insertion into a suitable `tabular` or `longtable`.
They reproduce the numerical table content, not journal pagination.
Column names and units are specified in the JSON and data dictionary.
Keep the dagger explanations from the provenance document with any reused
table. Do not quote a capped damping time as the true endpoint lifetime.

## 5. Reading the data directly

```python
import h5py
with h5py.File("data/core_sequences.h5", "r") as f:
    mass = f["EOS1/F1/DM/M"][:]
    frequency_khz = f["EOS1/F1/DM/f"][:]
    damping_seconds = f["EOS1/F1/DM/tau"][:]
```

The HDF5 files use lossless gzip compression and shuffle. No reduced-precision
quantization was applied. Independent mode arrays can have different mass
grids; do not combine entries merely because their row indices coincide.

## 6. Reproduction versus new calculations

The package evaluates interpolation, plotting, table formatting, and the
explicit leading-order binary criteria. It contains no TOV integrator,
full-GR perturbation solver, QNM root search, or EOS-generation implementation.
Changing model parameters in a plot label does not generate a new model.
New parameter points require new stellar calculations outside this release.

The full-GR radiative lifetimes describe isolated ideal-fluid stellar modes.
The binary criteria do not simulate mass transfer, contact, or detector
response. The endpoint stationary-phase assessment is a recorded physical
validity decision checked against its numerical diagnostics; it is not
converted into an invented universal numerical threshold.

## 7. Troubleshooting

- `No module named venv` or `ensurepip`: install the matching Python venv
  support using your operating system's normal package manager.
- Package download failure: check internet access or the package index;
  no project credentials are required. The first installation must finish
  before offline commands will work.
- Python outside 3.11-3.12: select a supported interpreter using `PYTHON=...`.
- Input hash mismatch: extract a fresh archive and compare its checksum.
- Missing output: rerun the full command; `--verify-only` does not generate files.
- Different PDF hashes across systems: numerical checks must still pass.
  Backend/font differences can change PDF encoding; consult the verification
  record for the tested environments and comparisons.

For an issue report, include the command, Python version, error text, and
`output/verification.json` if it exists. Do not send credentials or private
research directories.
