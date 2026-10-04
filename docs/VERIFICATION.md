# Verification record

Date: 2026-10-04. Status: **PASS for data-only reproduction. Public release authorized by the project owner.**

## Clean-environment tests

- Linux, Python 3.11.7: isolated environment, pinned dependency installation,
  complete generation, numerical checks, and eight regression tests passed.
- A second independent Linux desktop, Python 3.12.3: downloaded the archive
  through a private loopback-only connection, checked its checksum, extracted
  into a fresh directory, and ran with an empty HOME and cleared environment.
  `bash reproduce.sh` installed all dependencies and completed successfully.
  No stellar solver, original source tree, or project credentials were transferred.
- After the final table-format correction, the final execution content was
  downloaded and extracted again into a new directory. It passed the same
  full command and all eight tests using the just-installed isolated
  third-party environment. Imports were confirmed to come from the newly
  extracted package, not the earlier working tree.
- The twelve generated PDFs and six generated table files were byte-identical
  between Python 3.11.7 and Python 3.12.3 in these tests.
- `pip check` reported no broken dependencies. `--verify-only` passed.

Execution-content SHA-256:
`c2cb76a660f12d8dabd9678defc8012bbd725773be6369cd441e261d50abbf19`.
This hashes the sorted relative-file SHA-256 map for code, data, reference
fixtures, tests, workflow, installer, Makefile, dependency lock and ignore
rules. It excludes README, citation/rights metadata and documentation, so
the completed verification record can be appended without changing the
tested execution content. The final archive checksum is supplied separately.

## Numerical checks

- All 1,365 Table I cells and 756 Table II cells match the frozen manuscript,
  including unavailable values, dagger conventions, and published rounding.
- All five Table III rows reproduce the stated counts. The full Roche grid
  contains 1,527 stellar rows and 1,301 companions per row.
- All 157 certified halo rows satisfy the frequency/damping convention
  identities; all 11 excluded maximum-mass targets are nonhalo geometries.
- Regression tests cover interpolation without extrapolation, capped
  lifetimes without frequency replacement, preserved halo gaps, geometry
  exclusions, tidal arithmetic, input integrity, and LaTeX scientific notation.
- All 26 input/reference manifest entries passed SHA-256 verification.
- All generated LaTeX rows were compiled together successfully in a separate
  test document. LaTeX is not required to run this repository.

## Figure checks

All twelve generated PDFs were rendered and visually inspected. Original
paper files remain unchanged. Independent readback of the frozen paper's
curve geometry confirms the exported core curves to within 0.003 PDF points.
The reconstructed Figure 9 interpolation matches its archived geometry to
within 0.02 PDF points. The frequency/damping self-coupling curves and cleaned
octupolar grids were also checked against the archived plots.

The regenerated layouts are not advertised as byte-identical to the original
paper PDFs. That is distinct from the byte-identical outputs obtained across
the two tested reproduction environments. Reference PDFs are never used as
inputs to the figure-generation functions.

## Distribution boundary

The allowlisted archive contains no private solver imports, credentials,
private-machine paths, internal notes, or disallowed identifiers. Text,
filenames, HDF5 string metadata, PDF text/metadata and links were checked.
Numerical data occupy approximately 9.2 MB before ZIP compression.

This verifies reproduction from saved data, not a new independent full-GR
solver implementation. The observational outlines remain display products,
not posterior samples. The project owner authorized public access to the
data/reproduction repository on 2026-10-04. No additional reuse license has
been selected; the solver source remains excluded and private.
