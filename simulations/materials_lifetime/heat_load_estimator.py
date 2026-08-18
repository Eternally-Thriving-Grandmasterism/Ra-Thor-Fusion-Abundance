#!/usr/bin/env python3
"""
Ra-Thor-Fusion-Abundance — First-wall / Divertor Heat Load & Lifetime Scaffold
PATSAGi / TOLC 8 — Phase 2 Preparation

Purpose:
  Simple steady-state and transient heat-load estimates to frame materials challenges.

Truth Gate:
  Real lifetime depends on neutron damage (dpa), sputtering, thermal fatigue,
  and off-normal events. This scaffold only addresses thermal loading order-of-magnitude.
"""

from dataclasses import dataclass


@dataclass
class WallParams:
    major_radius_m: float
    minor_radius_m: float
    elongation: float
    P_exhaust_MW: float          # power to be exhausted
    wetted_fraction: float       # fraction of wall that sees the load
    pulse_length_s: float
    cycles_per_year: float


def approximate_wall_area(p: WallParams) -> float:
    # Rough plasma surface area for elongated plasma
    a = p.minor_radius_m
    R = p.major_radius_m
    kappa = p.elongation
    return 4 * 3.1416 * R * a * ((1 + kappa**2) / 2)**0.5   # m^2 approx


def average_heat_flux(p: WallParams) -> float:
    area = approximate_wall_area(p) * p.wetted_fraction
    if area <= 0:
        return 0.0
    return p.P_exhaust_MW / area   # MW/m^2


def rough_cycles_to_fatigue(heat_flux_MWm2: float, base_cycles: float = 1e5) -> float:
    """
    Extremely crude fatigue scaling — higher flux → fewer allowable cycles.
    Real fatigue life requires material-specific curves and temperature.
    """
    if heat_flux_MWm2 < 0.5:
        return base_cycles
    return base_cycles * (0.5 / heat_flux_MWm2)**1.5


if __name__ == "__main__":
    print("=== Illustrative first-wall heat load (NOT a design calculation) ===")
    p = WallParams(
        major_radius_m=1.8,
        minor_radius_m=0.55,
        elongation=1.8,
        P_exhaust_MW=20.0,
        wetted_fraction=0.25,
        pulse_length_s=10.0,
        cycles_per_year=5000,
    )
    flux = average_heat_flux(p)
    cycles = rough_cycles_to_fatigue(flux)
    print(f"  Approximate average heat flux: {flux:.2f} MW/m²")
    print(f"  Crude fatigue cycle estimate:  {cycles:.0f}")
    print("\nReplace with proper thermal-hydraulic and materials models.")
