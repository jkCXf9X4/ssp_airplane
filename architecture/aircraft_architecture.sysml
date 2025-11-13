package WingmanDrone {
  doc /* Loyal-wingman autonomous drone modeled after MQ-28 and Hellsing CA-1 Europa with conventional aviation propulsion. */
  attribute system_name = "DroneSystem";
  attribute author = "Codex Agent";
  attribute language = "SysML v2";

  comment Requirement_REQ_Profile /* Maintain MQ-28 class geometry (~11.7 m length, 7.3 m wingspan) for loyal wingman compatibility. */
  comment Requirement_REQ_Propulsion /* Use conventional turbofan propulsion with aviation fuel. */
  comment Requirement_REQ_Control /* Expose pilot-style inputs (stick, throttle, mode select) while keeping autopilot authority in the loop. */
  comment Requirement_REQ_Mission /* Support range, loiter, and escort scenario optimization for collaborative missions. */
}
