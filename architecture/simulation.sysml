
// Document simulation specific requirements and choices

package Aircraft {
  comment Requirement_REQ_Simulation_1 /* The system should be packaged and simulated as a SSP (system structure and parameterization) artifact */
  comment Requirement_REQ_Simulation_2 /* All models should be packaged as FMUs */

  // --- Solution specific choices ---

  comment location_orientation /* 
  Location is described in a local x/y/z grid in kilometers (x=North, y=East, z=Up)
  Absolute orientation is described in euler angles, North = 360° / 000°, East = 090°, South = 180°, West = 270 
  changes in orientation are described in +/- x for euler angles, pitch, yaw, roll, based upon absolute orientation 
  */

  comment waypoint_solutions /* 
  The waypoints should be injected into the simulation by utilizing SSP parameter set
  */

  comment visualization_and_io_solution /*
  The recommended interactive solution keeps ssp4sim as the simulation master and connects
  the packaged aircraft SSP to FlightGear through a dedicated bridge/adapter component.
  FlightGear is used as the visual frontend and pilot I/O frontend.
  Generic socket communication is preferred for the first implementation because it keeps the
  exchanged signals explicit and easier to debug than a larger native protocol mapping.
  */


}
