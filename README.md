# Electric Cooking and Solar Mini-Grid Reliability in Sudan

**Energy systems | Scenario modelling | Infrastructure adequacy**

## Overview

A deterministic simulation study exploring how electric-cooking adoption could affect the capacity adequacy of a representative rural solar mini-grid in semi-arid Sudan.

The analysis compares adoption scenarios of **0%, 20% and 40%**, examining changes in demand, unmet energy and potential PV and battery scaling requirements.

## Modelling Approach

- NASA POWER solar-resource inputs
- Synthetic, normalized hourly electricity demand profiles
- Electric-cooking demand scenarios
- Battery state-of-charge simulation
- Comparative system-sizing and reliability analysis

## Main Observations

- At 20% adoption, simulated reliability deterioration is comparatively modest.
- At 40% adoption, unmet energy rises substantially under the baseline configuration.
- Expanding storage alone does not fully address higher-demand scenarios.
- Coordinated PV and battery expansion provides a more effective adequacy response in the model.

These are **model-based findings**, not measured household adoption or field performance.

## Repository Structure

| Path | Contents |
| --- | --- |
| `src/` | Solar, load, cooking-demand and battery simulation scripts |
| `data/` | Input series and generated scenario outputs |
| `figures/` | Analysis figures |
| `README.md` | Study overview |

## Limitations

Results depend on deterministic solar and demand assumptions. The analysis does not establish causal effects on fuel choice, observed household behaviour, equipment failure rates or distribution-network contingencies.

## Author

Shamseldin Abdelrahim
