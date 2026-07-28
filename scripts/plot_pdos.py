#!/usr/bin/env python3
"""Regenerate the PDOS figures from Quantum ESPRESSO projwfc.x output.

Reads gqd.pdos_tot / s_gqd_1.pdos_tot and reproduces:
  - pristine_pdos.png
  - sulphur_doped_pdos.png
  - comparision.png

Usage:
    python scripts/plot_pdos.py
"""

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
PRISTINE_PDOS = ROOT / "pristine" / "gqd.pdos_tot"
SDOPED_PDOS = ROOT / "s_doped" / "s_gqd_1.pdos_tot"


def load_pdos_tot(path: Path) -> tuple[np.ndarray, np.ndarray]:
    energy, pdos = np.loadtxt(path, comments="#", usecols=(0, 2), unpack=True)
    return energy, pdos


def plot_single(energy: np.ndarray, pdos: np.ndarray, label: str, out_path: Path) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(energy, pdos, color="tab:blue", linewidth=1.2)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8, label="$E_F$")
    ax.set_xlabel("Energy (eV)")
    ax.set_ylabel("PDOS (states/eV)")
    ax.set_title(label)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_comparison(
    e_pristine: np.ndarray,
    pdos_pristine: np.ndarray,
    e_sdoped: np.ndarray,
    pdos_sdoped: np.ndarray,
    out_path: Path,
) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(e_pristine, pdos_pristine, label="Pristine GQD", color="tab:blue", linewidth=1.2)
    ax.plot(e_sdoped, pdos_sdoped, label="Sulphur-doped GQD", color="tab:red", linewidth=1.2)
    ax.axvline(0, color="black", linestyle="--", linewidth=0.8, label="$E_F$")
    ax.set_xlabel("Energy (eV)")
    ax.set_ylabel("PDOS (states/eV)")
    ax.set_title("Pristine vs. Sulphur-Doped GQD")
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--outdir", type=Path, default=ROOT, help="Directory to write PNGs into")
    args = parser.parse_args()

    e_pristine, pdos_pristine = load_pdos_tot(PRISTINE_PDOS)
    e_sdoped, pdos_sdoped = load_pdos_tot(SDOPED_PDOS)

    plot_single(e_pristine, pdos_pristine, "Pristine Graphene Quantum Dot", args.outdir / "pristine_pdos.png")
    plot_single(e_sdoped, pdos_sdoped, "Sulphur-Doped Graphene Quantum Dot", args.outdir / "sulphur_doped_pdos.png")
    plot_comparison(e_pristine, pdos_pristine, e_sdoped, pdos_sdoped, args.outdir / "comparision.png")


if __name__ == "__main__":
    main()
