# Reliability and Infrastructure Implications of Electric Cooking Adoption in Semi-Arid Rural Mini-Grids: A Sudan Case Study

## Overview

This project presents a deterministic techno-economic stress test of electric cooking adoption in a representative rural solar mini-grid system in semi-arid Sudan.

The objective is to evaluate how increasing electric cooking adoption affects:

- System reliability
- Peak demand escalation
- Battery stress
- Infrastructure scaling requirements

The model integrates:

- NASA POWER solar irradiance data
- Synthetic but normalized rural load profiles
- Deterministic battery state-of-charge simulation
- Scenario-based adoption analysis (0%, 20%, 40%)

## Research Scope

The study uses modelled demand profiles and deterministic assumptions rather than observed household adoption behaviour. Results describe simulated system adequacy, not measured field performance.

## Key Findings

- At 20% adoption, reliability degradation is modest and can be restored with minor battery scaling.
- At 40% adoption, unmet energy increases nonlinearly.
- Storage scaling alone is insufficient at higher adoption levels.
- Combined PV and storage scaling is required beyond a transition threshold.

## Repository Structure

- `/src` — Model scripts
- `/data` — Input and generated datasets
- `/figures` — Generated plots
- `/report` — Final technical brief (PDF)

## Disclaimer

This analysis evaluates system-level capacity adequacy under deterministic resource and demand assumptions. It does not model stochastic equipment failures or distribution-level contingency events.