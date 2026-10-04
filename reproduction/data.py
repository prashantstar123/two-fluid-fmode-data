"""Portable, read-only access to the released numerical records."""
from pathlib import Path
import h5py
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

def open_data(name):
    return h5py.File(DATA / name, "r")

def array(group, name):
    return np.asarray(group[name], dtype=float)

def interpolate(mass, values, target=1.4):
    mass, values = np.asarray(mass), np.asarray(values)
    if len(mass) < 2 or target < mass.min() or target > mass.max():
        return float("nan")
    return float(np.interp(target, mass, values))

def segments(group, mask=None):
    indexes = np.asarray(group["source_index"], dtype=int)
    keep = np.ones(len(indexes), dtype=bool) if mask is None else np.asarray(mask, bool)
    selected = np.flatnonzero(keep)
    if not len(selected):
        return []
    breaks = np.flatnonzero(np.diff(indexes[selected]) != 1) + 1
    return np.split(selected, breaks)
