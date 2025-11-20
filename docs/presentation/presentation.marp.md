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
<!-- comments:  -->
![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Goal

- Develop and evaluate experimental simulation engine supporting complex CPS development
  - Experimental orchestration
  - Efficient and deterministic

</div>

---

<!-- comments:  -->
![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Overview
- Integration into simulation workflows compatible with continuous complex CPS development
- Utilizing digital threads between: 
  Architecture, Models, Simulation and Requirements

- Utilizing open model standards such as FMUs and SSP

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Method

- Create and evaluate a simple mockup system for complex CPS development (multirole fighter)

- Machine readable definition for architecture (SysMLv2)

  - Sub-systems, interfaces, connections, requirements

</div>

---


![bg](./gripen-e-up-1160x773.jpg)

<div class="cols">

  <div class="col-left content-panel">

  ## Analysis Architecture

  - F16 inspired airframe and propulsion, HOTAS cockpit
  - Requirements cover performance, fuel, control, mission, and propulsion
  - Mission computer, flight controls, autopilot exposes evaluation data and telemetry from simulation

  </div>

  <div class="col-right">
    <img src="graphviz.png" alt="Architecture graph" />
  </div>

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Mission Use Case Evaluations

- Scenarios enables integration testing and top level requirement coverage

- Utilize parameter sets for simulation customization.

- Example scenarios: High-altitude intercept, Deep strike penetration,  Close air support patrol

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Sub-system Development Workflow

Iterate:
- Update architecture
- Sub-system interfaces generated from architecture
- Develop sub-system
- Package sub-system as a ready-to-deploy FMU
- Package sub-systems and parameter sets as a traceable SSP for simulation
- Simulate and evaluate

</div>


---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

# - SSP4SIM -


- Enabling complex cyber-physical systems development 
- Sole focus on Co-Simulation 
- SSP/FMI Compatible

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Key aspects

- Determinism
- Customizability
- Config
- Logging 

</div>


---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Determinism


</div>


---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Customizability

- 

</div>

---

![bg](./gripen-e-up-1160x773.jpg)
<div class="content-panel">

## Logging

- JSON, local or remote
- OTel extendable


</div>

