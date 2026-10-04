"""Recompute the published table summaries from released numerical records."""
from __future__ import annotations
import json
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import numpy as np
from .data import open_data, array, interpolate
from .models import TABLE_ORDER, FRACTIONS, RESONANCE_ORDER

CORE_COLUMNS = (
    "eos","fraction_percent","Mmax_Msun","Rmax_km","R14_km",
    "fNM14_kHz","fDM14_kHz","fNMmax_kHz","fDMmax_kHz",
    "tauNM14_s","tauDM14_s","tauNMmax_s","tauDMmax_s",
)
HALO_COLUMNS = (
    "eos","fraction_percent","Mmax_Msun","RDMmax_km","RDM14_km",
    "fDM14_kHz","fDMmax_kHz","tauDM14_s","tauDMmax_s",
)

def core_rows():
    rows=[]
    with open_data("core_sequences.h5") as f:
        for eos in TABLE_ORDER:
            base=f[eos]["pure_nm"]
            m,r,fr,t=(array(base,n) for n in ("M","R","f","tau"))
            rows.append(dict(zip(CORE_COLUMNS,[
                eos,0,m[-1],r[-1],interpolate(m,r),interpolate(m,fr),
                np.nan,fr[-1],np.nan,interpolate(m,t),np.nan,t[-1],np.nan
            ]),tauDMmax_capped=False))
            for percent in FRACTIONS:
                g=f[eos][f"F{percent}"]
                m,r=(array(g["structure"],n) for n in ("M","R"))
                values={}
                capped=False
                for mode in ("NM","DM"):
                    mm,ff,tt=(array(g[mode],n) for n in ("M","f","tau"))
                    endpoint_tau=tt[-1]
                    if mode=="DM" and percent==1 and endpoint_tau>1.e4:
                        accepted=np.flatnonzero(np.isfinite(tt)&(tt>0)&(tt<=1.e4))
                        if len(accepted):
                            endpoint_tau=tt[accepted[-1]]
                            capped=True
                    values[mode]=(interpolate(mm,ff),interpolate(mm,tt),ff[-1],endpoint_tau)
                n,d=values["NM"],values["DM"]
                rows.append(dict(zip(CORE_COLUMNS,[
                    eos,percent,m[-1],r[-1],interpolate(m,r),
                    n[0],d[0],n[2],d[2],n[1],d[1],n[3],d[3]
                ]),tauDMmax_capped=capped))
    return rows

def core_cells(rows):
    out=[]
    for row in rows:
        cells=[]
        for col in CORE_COLUMNS:
            value=row[col]
            if col=="eos":
                cell=value
            elif col=="fraction_percent":
                cell="NM" if value==0 else str(value)
            else:
                cell="--" if not np.isfinite(value) else format(value,".4g")
                if col=="tauDMmax_s" and row["tauDMmax_capped"]:
                    # This published capped cell uses three significant figures.
                    if row["eos"]=="RMF_m70_L50_N" and row["fraction_percent"]==1:
                        cell=f"{float(format(value,'.3g')):.0f}"
                    cell+="†"
            cells.append(cell)
        out.append(cells)
    return out

RECOVERED_ENDPOINTS={
    ("RMF_m55_L50_NY",1),("RMF_m55_L60_NY",1),
    ("RMF_m75_L40_N",10),("RMF_m75_L50_N",10),
}

def halo_rows():
    rows=[]
    with open_data("halo_sequences.h5") as curves, open_data("halo_modes.h5") as modes:
        index={(g.attrs["eos"],int(g.attrs["fraction_percent"]),g.attrs["target"]):g
               for g in modes.values()}
        for eos in TABLE_ORDER:
            for p in FRACTIONS:
                g=curves[eos][f"F{p}"]
                c=index[eos,p,"M1p4"];e=index[eos,p,"Mmax"]
                recovered=(eos,p) in RECOVERED_ENDPOINTS
                fmax=float(e["f_QNM_Hz"][()])/1000 if recovered else g.attrs["fDMmax"]
                tau=float(e["tau_GW_s"][()]) if e.attrs["geometry"]=="halo" else np.nan
                rows.append(dict(zip(HALO_COLUMNS,[eos,p,g.attrs["Mmax"],g.attrs["RDMmax"],
                    g.attrs["RDM1p4"],g.attrs["fDM1p4"],fmax,float(c["tau_GW_s"][()]),tau]),
                    fDMmax_capped=bool(g.attrs["fDMmax_capped"]) and not recovered,
                    fDMmax_evaluation_mass_Msun=g.attrs["Mmax"] if recovered else g.attrs["fDMmax_mass"],
                    endpoint_geometry=g.attrs["config_at_Mmax"]))
    return rows

def significant_fixed(x,n=4):
    return f"{x:.{max(0,n-1-int(np.floor(np.log10(abs(x)))))}f}" if x else "0"

def halo_cells(rows):
    out=[]
    for r in rows:
        cells=[r["eos"],str(r["fraction_percent"]),f'{r["Mmax_Msun"]:.3f}',
               f'{r["RDMmax_km"]:.2f}',f'{r["RDM14_km"]:.2f}']
        # Published DD2Y F1 radius uses decimal half-up rounding of 11.485 km.
        if r['eos']=='DD2Y' and r['fraction_percent']==1:
            cells[3]=str(Decimal(str(r['RDMmax_km'])).quantize(Decimal('.01'),rounding=ROUND_HALF_UP))
        # Original thirteen-model entries were rounded to four significant
        # figures before the common four-decimal-place table layout.
        legacy=r["eos"] in RESONANCE_ORDER and r["eos"] not in ("DD2Y","SLy4")
        for key in ("fDM14_kHz","fDMmax_kHz"):
            x=r[key]
            if legacy:x=float(format(x,".4g"))
            cells.append(f"{x:.4f}"+("†" if key=="fDMmax_kHz" and r["fDMmax_capped"] else ""))
        for key in ("tauDM14_s","tauDMmax_s"):
            x=r[key]
            if not np.isfinite(x):s="--"
            elif x>=1e4:
                exponent=int(np.floor(np.log10(x)))
                s=rf"{x/10**exponent:.2f}\!\times\!10^{{{exponent}}}"
            else:s=significant_fixed(x)
            cells.append(s)
        out.append(cells)
    return out

def write_table(name, columns, rows, cells, directory):
    directory.mkdir(parents=True,exist_ok=True)
    clean=[]
    for row in rows:
        clean.append({k:(None if isinstance(v,(float,np.floating)) and not np.isfinite(v)
                         else v.item() if isinstance(v,np.generic) else v)
                      for k,v in row.items()})
    (directory/f"{name}.json").write_text(json.dumps({"columns":columns,"rows":clean},indent=2,allow_nan=False)+"\n")
    tex=[]
    for row in cells:
        escaped=[str(x).replace("_",r"\_").replace("†",r"$^{\dagger}$") for x in row]
        escaped=[('$'+x+'$') if r'\times' in x and not x.startswith('$') else x for x in escaped]
        tex.append(" & ".join(escaped)+r" \\")
    (directory/f"{name}.tex").write_text("\n".join(tex)+"\n")
    return cells
