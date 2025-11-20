---
marp: true
theme: left-panel
paginate: true
---

![bg](./gripen-e-up-1160x773.jpg)
<div class="first">


# SSP Simulation platform
Erik Rosenlund
Linköping University, Saab Aeronautics

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Overview
- Evaluating workflows compatible with complex CPS development
- Digital thread from Architecture, Models, Simulation and Requirement fulfillment
- Develop and evaluate SSP4SIM for simulation validation
  - Utilizing open model standards such as FMUs, and SSP
- Automated toolchain wraps artifact generation, verification, and simulation steps

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Goals

- Create a simple mockup system for complex CPS development, 
  - Single-seat multirole fighter reference project
- SysMLv2 packages as definition for architecture
  - Sub-systems, interfaces, connections, requirements
- Create a workflow that would enable CI/CD

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Model Development Workflow

- Model interfaces generated and verified from architecture
- Package every subsystem as a ready-to-deploy FMU 
- Utilize parameter sets for simulation customization.
- Package sub-systems and parameter sets as a traceable SSP bundle for simulation.

</div>

---

![bg](./gripen-e-up-1160x773.jpg)

<div class="cols">

  <div class="col-left content-panel">

  ## Analysis Architecture

  - F16 inspired airframe and propulsion, HOTAS cockpit
  - Requirements cover performance, fuel, control, mission, and propulsion
  - Mission computer, flight controls, autopilot exposes evaluation data and telemetry

  </div>

  <div class="col-right">
    <img src="graphviz.png" alt="Architecture graph" />
  </div>

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Mission Use Case Evaluations
Each scenario enforces requirement coverage and enables reproducible CI validation.

1. High-altitude intercept
2. Deep strike penetration
3. Close air support patrol

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Simulation Engine - SSP4SIM

- Determinism
- Customizability
- Config
- Logging 

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Results & Next Steps


</div>


---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Results & Next Steps


</div>


---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Results & Next Steps


</div>
