package Aircraft {
  requirement def Requirement_REQ_Profile { doc /* Match F-16 Fighting Falcon geometry: ≈15 m length, 10 m wingspan, single-seat cockpit. */ }
  requirement def Requirement_REQ_Performance { doc /* Provide Mach 2 dash capability with sustained 9 g maneuver envelope. */ }
  requirement def Requirement_REQ_Propulsion { doc /* Integrate an F100/F110 class augmented turbofan with afterburner throttle control. */ }
  requirement def Requirement_REQ_Fuel { doc /* Carry at least 3,100 kg of internal fuel with 8% reserve margin for recovery. */ }
  requirement def Requirement_REQ_Control { doc /* Provide full HOTAS pilot controls, digital fly-by-wire channels, and autopilot hold modes. */ }
  requirement def Requirement_REQ_Mission { doc /* Support multirole loadouts across nine hardpoints with mission computer stores management. */ }
  requirement def Requirement_REQ_FlyByWire { doc /* It should be an unstable aircraft, the control loop should compensate for this. */ }
  requirement def Requirement_REQ_Waypoints_1 { doc /* It should support loading a number of waypoints that it should fy to in order */ }
}
