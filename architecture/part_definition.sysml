package Aircraft
 {
  package Subsystems {
    doc /* Reconfigured to model an F-16 Fighting Falcon multirole fighter with single-engine propulsion and manned cockpit. */

    import ScalarValues::*;
    import Collections::*;
    import Aircraft::Interfaces::*;

    part def ControlInterface {
      doc /* F-16 HOTAS + side-stick interface for pilot inputs and trim switches. */
      attribute input_scheme : String = "HOTAS";
      attribute telemetry_rate_hz : Integer = 120;
      attribute useBridgeInput : Boolean = false;

      in port bridgeInput : PilotCommand {
        doc /* External pilot command provided by an interactive bridge/frontend adapter. */
      }

      out port pilotCommand : PilotCommand {
        doc /* HOTAS-control bundle forwarded for mission computer sensor fusion. */
      }
    }

    part def FlightGearBridge {
      doc /* Adapter component for ROS 2 visualization/control coupling via a UDP companion runtime. */
      attribute transport : String = "Ros2UdpBridge";
      attribute reference_latitude_deg : Real = 0.0;
      attribute reference_longitude_deg : Real = 0.0;
      attribute reference_altitude_m : Real = 0.0;
      attribute remote_host : String = "127.0.0.1";
      attribute telemetry_port : Integer = 5501;
      attribute control_port : Integer = 5502;

      in port statePosition : PositionXYZ {
        doc /* Aircraft position from the simulated environment. */
      }

      in port stateOrientation : OrientationEuler {
        doc /* Aircraft attitude from the simulated environment. */
      }

      in port flightStatus : FlightStatusPacket {
        doc /* Flight status exported for ROS 2 telemetry and diagnostics. */
      }

      in port missionStatus : MissionStatus {
        doc /* Mission/autopilot status exported for ROS 2 telemetry and diagnostics. */
      }

      out port pilotCommand : PilotCommand {
        doc /* Pilot command returned from the ROS 2 control frontend into the vehicle control path. */
      }
    }

    part def AutopilotModule {
      doc /* F-16 autopilot, takes in sensor data and translates it into a equivalent hotas command. */

      comment /* Autopilot parameter-set comment used by the parser test. */
      attribute waypointCount : Integer = 10;
      attribute waypointProximity_km : Real = 10;
      //attribute waypointX_km : Array<Real> = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
      //attribute waypointY_km : Array<Real> = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
      //attribute waypointZ_km : Array<Real> = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

      in port feedbackBus : FlightStatusPacket {
        doc /* Mission-computer flight status back into autopilot. */
      }

      in port currentLocation : PositionXYZ {
        doc /* Current local position from sensors */
      }

      in port currentOrientation : OrientationEuler {
        doc /* Current attitude from sensors. */
      }

      out port autopilotCmd : PilotCommand {
        doc /* HOTAS-equivalent command stream for mission computer blending. */
      }

      out port missionStatus : MissionStatus {
        doc /* Waypoint progression for logging and verification. */
      }
    }

    part def CompositeAirframe {
      doc /* F-16 aluminum/composite fuselage sized for high-supersonic operations with dorsal spine for avionics. */
      attribute length_m : Real = 15.0;
      attribute fuselage_width_m : Real = 3.0;
      attribute wingspan_m : Real = 10.0;
      attribute empty_weight_kg : Real = 8573;
      attribute payload_capacity_kg : Real = 7700;
      attribute hardpoint_count : Integer = 9;

    }

    part def TurbofanPropulsion {
      doc /* Pratt & Whitney F100 / GE F110 class augmented turbofan powering the F-16. */
      attribute max_thrust_kn : Real = 129.7;
      attribute dry_thrust_kn : Real = 79.0;
      attribute specific_fuel_consumption : Real = 0.76;
      attribute fuel_capacity_kg : Real = 3160;
      attribute generator_output_kw : Real = 80;

      in port throttleCmd : ThrottleCommand {
        doc /* Mission computer throttle + afterburner command input. */
      }

      out port thrustOut : ThrustState {
        doc /* Propulsion thrust telemetry exported to airframe. */
      }

      out port fuel_consumption : FuelConsumptionRate {
        doc /* Mass flow telemetry */
      }
    }

    part def MissionComputer {
      doc /* F-16C/D mission computer blending pilot HOTAS inputs with fly-by-wire control laws and stores management. */

      in port manualInput : PilotCommand {
        doc /* Manual HOTAS command bundle from cockpit controls. */
      }

      in port autopilotInput : PilotCommand {
        doc /* Autopilot command bundle using same HOTAS signal structure. */
      }

      in port fuelStatus : FuelLevelState {
        doc /* Fuel telemetry used for command blending and power limiting. */
      }

      out port engineThrottle : ThrottleCommand {
        doc /* Structured throttle/fuel enable command to propulsion. */
      }

      out port direction_command : OrientationEuler {
        doc /* Command how to alter the current velocity vector, pith, yaw, roll */
      }
    }

    part def FuelSystem {
      doc /* Internal + conformal fuel storage management with transfer pumps feeding engine feed tanks. */
      attribute fuel_capacity_kg : Real = 3160;
      attribute reserve_fraction : Real = 0.08;

      in port fuel_consumption_rate : FuelConsumptionRate {
        doc /* Propulsion-requested fuel mass flow entering storage manager. */
      }

      out port fuelState : FuelLevelState {
        doc /* Telemetry describing remaining fuel mass/normalized level. */
      }
    }

    part def AdaptiveWingSystem {
      doc /* Leading-edge strake and cropped-delta wing sized to F-16 Block 50 geometry with 9g capability. This model includes the control system */
      attribute reference_area_m2 : Real = 28.0;
      attribute span_m : Real = 10.0;
      attribute aspect_ratio : Real = 3.6;
      attribute control_authority_deg : Real = 25;
      attribute load_factor_limit_g : Integer = 9;

      in port direction_command : OrientationEuler {
        doc /* Mission-computer command bus input. Desired change in speed vector */
      }

      in port flight_speed : FlightStatusPacket;

      out port actuation_command : SurfaceActuationCommand {
        doc /* Actuation commands, sent to environment to track and calculate new position */
      }

      out port liftInterface : LiftState {
        doc /* Tracking of lift, drag */
      }
    }

    part def Environment {
      doc /* Tracking position and velocities of the aircraft and feeds the sensors */

      in port actuation_command : SurfaceActuationCommand {
        doc /* Reads the actuation and thrust commands to calculate the position, rotation and velocities */
      }
      in port direction_command : OrientationEuler;
      in port lift : LiftState;
      in port thrust_in : ThrustState;

      out port orientation : OrientationEuler {
        doc /* Feedback for simulated sensors */
      }
      out port location : PositionXYZ;
      out port flight_status : FlightStatusPacket;

    }

    part def InputOutput {
      doc /* Simulation sink for debugging and recording mission/autopilot telemetry. */
      in port locationXYZ : PositionXYZ;
      in port orientation : OrientationEuler;
      in port autopilotCmd : PilotCommand;
      in port flightStatus : FlightStatusPacket;
      in port missionStatus : MissionStatus;
    }
  }
}
