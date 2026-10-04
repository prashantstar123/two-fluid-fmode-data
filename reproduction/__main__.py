"""One-command reproduction and checks from the released numerical data."""
import argparse
import importlib.metadata
import json
import platform
import time
from pathlib import Path
from .data import ROOT
from . import figures,halo_figures,profiles,tables,tidal,verify

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=ROOT/'output')
    p.add_argument('--verify-only',action='store_true',help='Verify inputs, numbers and an existing complete output')
    args=p.parse_args();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    start=time.monotonic()
    print('Checking input hashes and published table cells...',flush=True)
    count=verify.verify_inputs();checks=verify.numerical_checks()
    if not args.verify_only:
        folder=out/'tables'
        for name,cols,rows,formatter in (('table1_core',tables.CORE_COLUMNS,tables.core_rows(),tables.core_cells),
                ('table2_halo',tables.HALO_COLUMNS,tables.halo_rows(),tables.halo_cells)):
            tables.write_table(name,cols,rows,formatter(rows),folder)
        table,diagnostics=tidal.calculate()
        cells=[[r['criterion'],rf"${r['N_star']}\times{r['N_companion']}$" if 'N_star' in r else str(r['N_eval']),str(r['N_pass'])] for r in table]
        tables.write_table('table3_accessibility',('criterion','N_eval','N_pass'),table,cells,folder)
        (folder/'tidal_diagnostics.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
        figout=out/'figures';figout.mkdir(parents=True,exist_ok=True)
        for label,fn in (('Figures 1-3',figures.render_core),('Figures 4-6',halo_figures.render),
                         ('Figure 7',profiles.render_radial),('Figure 8',profiles.render_metric),
                         ('Figures 9-11',figures.render_coupling),('Figure 12',figures.render_multipoles)):
            print(f'Rendering {label}...',flush=True);fn(figout)
    output_hashes=verify.verify_outputs(out)
    if args.verify_only:
        previous=json.loads((out/'verification.json').read_text())
        if previous['outputs']!=output_hashes:
            raise ValueError('Output hash mismatch relative to the recorded completed run.')
    report=dict(status='PASS',scope='Released data and rendering reproduction, not a rerun of the private stellar solver',
                input_files_checked=count,numerical_checks=checks,outputs=output_hashes,
                python=platform.python_version(),platform=platform.system(),
                packages={line.split('==')[0]:importlib.metadata.version(line.split('==')[0])
                          for line in (ROOT/'requirements.lock').read_text().splitlines() if '==' in line},
                elapsed_seconds=round(time.monotonic()-start,3))
    (out/'verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'PASS: 12 figures, 3 tables, all numerical reference checks. Output: {out}',flush=True)

if __name__=='__main__':main()
