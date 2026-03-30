
// Document simulation specific requirements and choices

package Aircraft {
  requirement def Requirement_REQ_Simulation_1 { doc /* The system should be packaged and simulated as a SSP (system structure and parameterization) artifact */ }
  requirement def Requirement_REQ_Simulation_2 { doc /* All models should be packaged as FMUs */ }

  // --- Solution specific choices ---

  // Location is described in a local x/y/z grid in kilometers (x=North, y=East, z=Up).
  // Absolute orientation is described in Euler angles:
  // North = 360° / 000°, East = 090°, South = 180°, West = 270°.
  // Changes in orientation are described in +/- x for Euler angles, pitch, yaw, roll.

  // Waypoints should be injected into the simulation through an SSP parameter set.

  // The recommended interactive solution keeps ssp4sim as the simulation master and connects
  // the packaged aircraft SSP to FlightGear through a dedicated bridge/adapter component.
  // FlightGear is used as the visual frontend and pilot I/O frontend.
  // Generic socket communication is preferred for the first implementation because it keeps the
  // exchanged signals explicit and easier to debug than a larger native protocol mapping.
  // The first timing solution should use the existing ssp4sim realtime execution option.
  // A future Python API doStep(t) method and external package synchronization support are planned,
  // but should not be introduced in the initial integration.
}
