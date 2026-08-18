#!/usr/bin/env python3
"""
Ra-Thor-Fusion-Abundance — Plasma Power Balance Scaffold
PATSAGi / TOLC 8 — Phase 2 Preparation

Purpose:
  Transparent, educational, and scientifically grounded starting point for
  exploring the conditions required for net power in a magnetic confinement device.

Important Truth Gate notice:
  This is NOT a predictive reactor design code.
  It uses highly simplified 0-D power balance relations common in fusion education
  and early scoping studies. Real devices require full MHD, transport, and
  engineering models (TRANSP, ASTRA, TokaMaker, etc.).

  All results must be treated as illustrative until replaced with validated physics.
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class PlasmaParams:
    # Volume-averaged quantities (highly idealized)
    n_e: float          # electron density [10^20 m^-3]
    T_i: float          # ion temperature [keV]
    T_e: float          # electron temperature [keV]
    tau_E: float        # energy confinement time [s]
    volume: float       # plasma volume [m^3]
    P_aux: float        # auxiliary heating power [MW]


def fusion_power_density_dt(n_i: float, T_i: float) -> float:
    """
    Very rough D-T fusion power density [MW/m^3].
    Uses a simple approximation of <sigma-v> near the 10–20 keV range.
    Real calculations need proper reactivity tables.
    """
    # Extremely simplified reactivity scaling (illustrative only)
    # Peak reactivity around 60–70 keV; this is a crude fit for scoping
    if T_i < 5.0:
        return 0.0
    sigma_v_approx = 1.1e-24 * (T_i ** 2) * (1 - 0.01 * T_i)  # m^3/s, rough
    # n_i in 10^20 m^-3 → convert
    n = n_i * 1e20
    # Power density ~ (1/4) n^2 <sv> * E_fusion (E ≈ 17.6 MeV)
    E_J = 17.6e6 * 1.602e-19
    p_wm3 = 0.25 * n * n * sigma_v_approx * E_J
    return p_wm3 / 1e6  # MW/m^3


def power_balance(params: PlasmaParams) -> Dict[str, float]:
    """
    0-D power balance:
      P_fusion + P_aux = P_loss + P_radiation (simplified)
    """
    n_i = params.n_e  # assume quasi-neutrality, pure D-T 50/50 for simplicity
    p_fus_density = fusion_power_density_dt(n_i, params.T_i)
    P_fusion = p_fus_density * params.volume  # MW

    # Loss power ≈ 3 n T V / tau_E  (very rough)
    # Convert keV to Joules, etc.
    energy_density_J = 1.5 * (params.n_e * 1e20) * (params.T_i + params.T_e) * 1e3 * 1.602e-19
    P_loss = (energy_density_J * params.volume) / params.tau_E / 1e6  # MW

    # Net power (thermal) before conversion
    P_net_thermal = P_fusion + params.P_aux - P_loss

    # Q = P_fusion / P_aux  (scientific gain)
    Q = P_fusion / params.P_aux if params.P_aux > 0 else float("inf")

    return {
        "P_fusion_MW": round(P_fusion, 3),
        "P_loss_MW": round(P_loss, 3),
        "P_net_thermal_MW": round(P_net_thermal, 3),
        "Q_scientific": round(Q, 3),
        "fusion_power_density_MWm3": round(p_fus_density, 4),
    }


def example_sparc_like() -> None:
    """Illustrative point roughly inspired by published SPARC-class parameters (not a prediction)."""
    print("=== Illustrative SPARC-class-like 0-D point (NOT a prediction) ===")
    p = PlasmaParams(
        n_e=3.0,       # 10^20 m^-3
        T_i=12.0,      # keV
        T_e=12.0,
        tau_E=0.6,     # s (optimistic for compact high-field)
        volume=20.0,   # m^3 (order of magnitude for compact device)
        P_aux=25.0,    # MW
    )
    result = power_balance(p)
    for k, v in result.items():
        print(f"  {k}: {v}")
    print("\nReplace reactivity, confinement scaling, and profiles with validated models.")


if __name__ == "__main__":
    example_sparc_like()
