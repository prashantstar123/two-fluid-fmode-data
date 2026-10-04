"""Portable numerical and output integrity checks."""
import hashlib
import json
from pathlib import Path
import numpy as np
from .data import ROOT,DATA,open_data
from .models import TABLE_ORDER,FRACTIONS,FIGURE_NAMES
from .tables import core_rows,core_cells,halo_rows,halo_cells
from .tidal import calculate,C

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def verify_inputs():
    manifest=json.loads((ROOT/'reference/input_manifest.json').read_text())
    for relative,expected in manifest.items():
        p=ROOT/relative
        if not p.is_file() or digest(p)!=expected:
            raise ValueError(f'Input integrity failure: {relative}')
    return len(manifest)

def compare_rows(actual,expected):
    keyed={(r[0],r[1]):r for r in expected}
    assert len(keyed)==len(actual)
    differences=[]
    for r in actual:
        e=keyed[(r[0],r[1])]
        for j,(a,b) in enumerate(zip(r,e)):
            if a!=b:differences.append(dict(eos=r[0],fraction=r[1],column=j,actual=a,expected=b))
    if differences:raise ValueError(f'Table mismatch: {differences}')
    return sum(map(len,actual))

def numerical_checks():
    golden=json.loads((ROOT/'reference/table_cells.json').read_text())
    core=compare_rows(core_cells(core_rows()),golden['table1'])
    halo=compare_rows(halo_cells(halo_rows()),golden['table2'])
    with open_data('halo_modes.h5') as f:
        certified=0;nonhalo=0
        for g in f.values():
            if g.attrs['certification']=='CERTIFIED':
                certified+=1
                assert g.attrs['geometry']=='halo'
                np.testing.assert_allclose(g['f_QNM_Hz'][()],C*g['omega_real_per_m'][()]/(2*np.pi),rtol=1e-13)
                np.testing.assert_allclose(g['tau_GW_s'][()],1/(C*g['omega_imag_per_m'][()]),rtol=1e-13)
                assert g['n_DM'][()]==0
                assert g['amplitude_ratio_NM_to_DM'][()]<.2
            else:
                nonhalo+=1
                assert g.attrs['geometry']=='core'
        assert (certified,nonhalo)==(157,11)
    with open_data('core_sequences.h5') as f:
        assert set(f)==set(TABLE_ORDER)
        for eos in TABLE_ORDER:
            for p in FRACTIONS:
                for branch in ('NM','DM'):
                    g=f[eos][f'F{p}'][branch]
                    assert len(g['M'])==len(g['f'])==len(g['tau'])
                    mass=g['M'][:]
                    # The publication's displayed core sequences start at 0.5.
                    # Saved sub-0.5 samples are retained without rewriting them.
                    assert np.all(np.diff(mass[mass>=.5])>0)
                    assert np.all(g['tau'][:]>0)
    table,diagnostics=calculate()
    assert [r['N_eval'] for r in table]==[52,1986627,82,82,84]
    assert [r['N_pass'] for r in table]==[0]*5
    assert abs(diagnostics['max_RL_over_RDM']-.9060312836202808)<1e-12
    return dict(core_table_cells=core,halo_table_cells=halo,halo_certified=certified,
                nonhalo_endpoints=nonhalo,accessibility_rows=5)

def verify_outputs(out):
    products=[]
    for stem in FIGURE_NAMES.values():
        p=out/'figures'/f'{stem}.pdf'
        if not p.is_file() or not p.read_bytes().startswith(b'%PDF-') or p.stat().st_size<3000:
            raise ValueError(f'Missing or malformed figure: {p.name}')
        products.append(p)
    for name in ('table1_core','table2_halo','table3_accessibility'):
        for extension in ('tex','json'):
            p=out/'tables'/f'{name}.{extension}'
            if not p.is_file() or not p.stat().st_size:raise ValueError(f'Missing table: {p.name}')
            products.append(p)
    return {str(p.relative_to(out)):digest(p) for p in products}
