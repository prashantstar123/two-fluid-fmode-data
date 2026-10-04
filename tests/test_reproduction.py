"""Regression tests for numerical selection, conventions and outputs."""
import unittest
import tempfile
from pathlib import Path
import numpy as np
from reproduction import verify
from reproduction.tables import core_rows,halo_rows,halo_cells,write_table,HALO_COLUMNS
from reproduction.data import open_data,segments,interpolate
from reproduction.tidal import calculate,binary_diagnostics

class ReproductionTests(unittest.TestCase):
    def test_latex_scientific_notation(self):
        rows=halo_rows()
        with tempfile.TemporaryDirectory() as tmp:
            write_table('halo',HALO_COLUMNS,rows,halo_cells(rows),Path(tmp))
            text=(Path(tmp)/'halo.tex').read_text()
            self.assertIn(r'$1.20\!\times\!10^{6}$',text)
            self.assertNotIn('†',text)

    def test_input_integrity(self):
        self.assertGreaterEqual(verify.verify_inputs(),11)

    def test_published_cells_and_modes(self):
        report=verify.numerical_checks()
        self.assertEqual(report['core_table_cells'],105*13)
        self.assertEqual(report['halo_table_cells'],84*9)

    def test_caps_do_not_replace_endpoint_frequency(self):
        with open_data('core_sequences.h5') as f:
            for row in core_rows():
                if row['tauDMmax_capped']:
                    g=f[row['eos']]['F1']['DM']
                    self.assertGreater(g['tau'][-1],10000)
                    self.assertLessEqual(row['tauDMmax_s'],10000)
                    self.assertEqual(row['fDMmax_kHz'],g['f'][-1])

    def test_no_extrapolation(self):
        self.assertTrue(np.isnan(interpolate([1.,1.3],[2.,3.],1.4)))
        rows=[r for r in core_rows() if r['fraction_percent']==20 and np.isnan(r['R14_km'])]
        self.assertEqual({r['eos'] for r in rows},{'RMF_m60_L50_NY','RMF_m60_L60_NY'})

    def test_halo_dashes_are_geometry(self):
        rows=halo_rows();missing=[r for r in rows if np.isnan(r['tauDMmax_s'])]
        self.assertEqual(len(missing),11)
        self.assertTrue(all(r['endpoint_geometry']=='core' for r in missing))

    def test_gap_retained(self):
        with open_data('halo_sequences.h5') as f:
            g=f['RMF_m55_L60_NY/F1/frequency']
            chunks=segments(g,g['halo'][:]==1)
            self.assertEqual(len(chunks[-1]),1)
            self.assertEqual(int(g['source_index'][chunks[-1][0]]),16)
            self.assertNotIn(15,g['source_index'][:])

    def test_tidal_arithmetic(self):
        table,diagnostics=calculate()
        self.assertEqual([r['N_pass'] for r in table],[0]*5)
        self.assertEqual(table[1]['N_eval'],1527*1301)
        self.assertAlmostEqual(diagnostics['L1_mean'],1.6793835338816834,places=12)
        # Independent algebraic separation check.
        g=6.67430e-11;msun=1.98892e30
        d=(g*2.8*msun/(np.pi*140.)**2)**(1/3)/1000
        self.assertAlmostEqual(binary_diagnostics(1.4,88,.140,1.,1.4,88)['D_res_km'],d,places=10)

if __name__=='__main__':unittest.main()
