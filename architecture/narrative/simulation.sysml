
// Document simulation specific requirements and choices

package SimulationRequirements {
  requirement def Requirement_REQ_Simulation_1 {
    doc /* The system should be packaged and simulated as a SSP (system structure and parameterization) artifact */
  }
  requirement def Requirement_REQ_Simulation_2 {
    doc /* All models should be packaged as FMUs */
  }

  // --- Solution specific choices ---

  // Location is described in a local x/y/z grid in kilometers (x=North, y=East, z=Up).
  // Absolute orientation is described in Euler angles:
  // North = 360° / 000°, East = 090°, South = 180°, West = 270°.
  // Changes in orientation are described in +/- x for Euler angles, pitch, yaw, roll.

  // Waypoints should be injected into the simulation through an SSP parameter set.

  // The aircraft broadcasts its entity state one-way: a state-source FMU converts the local
  // ENU/orientation state into the flat RPR entity-state leaves, and the generic RPR entity
  // FMU publishes them. The aircraft consumes no inbound pilot command over that wire.
  // The first timing solution should use the existing ssp4sim realtime execution option.
  // A future Python API doStep(t) method and external package synchronization support are planned,
  // but should not be introduced in the initial integration.
}
