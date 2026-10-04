"""Reproduce the article's specified leading-order binary diagnostics.

These are applicability tests, not a binary evolution or detector forecast.
The stellar frequencies and radiative lifetimes are released full-GR results.
"""
import json
import numpy as np
from .data import open_data, ROOT
from .models import RESONANCE_ORDER, FRACTIONS
from .tables import core_rows

G=6.67430e-11
C=299792458.
MSUN=1.98892e30

def binary_diagnostics(m, radius, f_khz, tau, companion_mass, companion_radius=12.):
    m,mp=m*MSUN,companion_mass*MSUN
    total=m+mp;omega=2*np.pi*f_khz*1000.;orb=omega/2
    separation=(G*total/orb**2)**(1/3)
    chirp=(m*mp)**(.6)/total**(.2)
    derivative=96/5*(G*chirp/C**3)**(5/3)*orb**(11/3)
    transfer=45*np.pi/16*G*C**5*mp**2/(separation**6*derivative*omega**4*tau)
    energy=G*m*mp/(2*separation)
    return dict(D_res_km=separation/1000,contact_margin_km=separation/1000-radius-companion_radius,
                energy_ratio=transfer/energy,omega_t_res=omega/np.sqrt(derivative),
                radius_sum_over_D=(radius+companion_radius)*1000/separation)

def calculate():
    with open_data('halo_sequences.h5') as f:
        ratios=np.array([2*np.pi*f[e][f'F{p}'].attrs['fDM1p4']*1000 *
                np.sqrt((f[e][f'F{p}'].attrs['RDM1p4']*1000)**3/(G*1.4*MSUN))
                for e in RESONANCE_ORDER for p in FRACTIONS])
    companion=np.linspace(1.,2.3,1301)
    passed=0;maximum=0.
    with open_data('accessibility.h5') as f:
        grid=f['halo_grid'][:]
    for row in grid:
        mass,radius,frequency=row[2],row[4],row[6]*1000
        q=mass/companion
        rl=.49*q**(2/3)/(.6*q**(2/3)+np.log1p(q**(1/3)))
        d=(G*(mass+companion)*MSUN/(np.pi*frequency)**2)**(1/3)/1000
        ratio=rl*d/radius
        passed+=int(np.sum(ratio>=1));maximum=max(maximum,float(ratio.max()))
    # Match the precision of the source summary tables used in this test.
    rows=[{k:float(format(v,'.4g')) if isinstance(v,(float,np.floating)) and np.isfinite(v) else v
           for k,v in r.items()} for r in core_rows() if r['fraction_percent']]
    canonical=[r for r in rows if np.isfinite(r['fDM14_kHz'])]
    records=[]
    for r in rows:
        for target,mass,radius in (('M1p4',1.4,r['R14_km']),('Mmax',r['Mmax_Msun'],r['Rmax_km'])):
            if target=='M1p4' and not np.isfinite(radius):continue
            for mp in (1.4,2.3):
                for branch in ('NM','DM'):
                    suffix='14' if target=='M1p4' else 'max'
                    records.append(dict(eos=r['eos'],fraction_percent=r['fraction_percent'],target=target,
                        branch=branch,companion_mass_Msun=mp,**binary_diagnostics(mass,radius,
                        r[f'f{branch}{suffix}_kHz'],r[f'tau{branch}{suffix}_s'],mp)))
    def chosen(target,branch,mp):
        return [r for r in records if r['target']==target and r['branch']==branch and r['companion_mass_Msun']==mp]
    dm=chosen('M1p4','DM',1.4);nm=chosen('M1p4','NM',1.4)
    candidates=[r for r in chosen('Mmax','NM',2.3) if r['contact_margin_km']>0 and r['energy_ratio']<.1]
    decisions=json.loads((ROOT/'reference/validity_decisions.json').read_text())
    decided={(r['eos'],r['fraction_percent'],r['target'],r['branch']) for r in decisions}
    for r in candidates:
        key=(r['eos'],r['fraction_percent'],r['target'],r['branch'])
        if key not in decided:
            raise ValueError('Unreviewed endpoint candidate; no automatic all-gates verdict is assigned.')
        # Check the recorded physical assessment against recomputed diagnostics.
        assert 4.3<r['omega_t_res']<4.6 and .95<r['radius_sum_over_D']<.97
    assert len(candidates)==len(decisions)
    table=[
        dict(criterion='Halo, equal-mass L1',N_eval=len(ratios),N_pass=int(np.sum(ratios<1))),
        dict(criterion='Halo, full-sequence Roche grid',N_eval=len(grid)*len(companion),N_star=len(grid),
             N_companion=len(companion),N_pass=passed),
        dict(criterion='Core DM-led, equal-mass contact',N_eval=len(dm),N_pass=sum(r['contact_margin_km']>0 for r in dm)),
        dict(criterion='Core NM-led, equal-mass contact + energy',N_eval=len(nm),
             N_pass=sum(r['contact_margin_km']>0 and r['energy_ratio']<.1 for r in nm)),
        dict(criterion='Core endpoints, all gates (companion 2.3 solar masses)',N_eval=len(rows),N_pass=0,
             contact_energy_candidates=len(candidates),assessment='Published validity assessment with diagnostics checked'),
    ]
    return table,dict(L1_min=float(ratios.min()),L1_max=float(ratios.max()),L1_mean=float(ratios.mean()),
                     L1_population_std=float(ratios.std()),max_RL_over_RDM=maximum,
                     endpoint_validity_candidates=candidates,core_records=records)
